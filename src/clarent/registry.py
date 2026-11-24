"""Method discovery and validation.

A *method* is a self-contained folder `methods/<id>/` with:
  method.toml   manifest (see methods/ach/method.toml)
  CARD.md       methodology card (sections listed in CARD_SECTIONS)
  <module>/     importable Python package exposing main(argv) -> int
  skill/        optional SKILL.md for Claude Code
  tests/        unittest tests      examples/   runnable examples
"""
from __future__ import annotations

import datetime as _dt
import importlib
import os
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

REQUIRED_KEYS = ("id", "name", "version", "family", "status", "summary")
FAMILIES = ("military", "lean", "soviet", "systems", "decision", "extra")
STATUSES = ("spec", "beta", "stable", "reference")
VERIFICATION = ("read", "exists", "blocked", "unverified")
NOVELTY = ("none", "exists-but-weak", "exists-but-abandoned", "well-covered")
SURFACES = ("cli", "skill", "agent", "hook", "mcp", "action")
CARD_SECTIONS = (
    "Origin", "Sources", "Problem it solves", "When to use / when NOT to use",
    "How it maps to software work", "Inputs and outputs", "Algorithm (what is deterministic)",
    "Limitations", "Prior art (GitHub scan)", "Worked example", "Evaluation",
)
NOVELTY_MAX_AGE_DAYS = 90
SKILL_DESCRIPTION_MAX = 300


@dataclass(frozen=True)
class Method:
    id: str
    dir: Path
    manifest: dict

    @property
    def module(self) -> str:
        return self.manifest.get("python", {}).get("module", "")


def methods_dir() -> Path:
    """$CLARENT_METHODS_DIR, else <repo>/methods (editable install), else packaged copy."""
    env = os.environ.get("CLARENT_METHODS_DIR")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for cand in (here.parents[2] / "methods", here.parent / "_methods"):
        if cand.is_dir():
            return cand
    return here.parents[2] / "methods"


def load_manifest(path: Path) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


def discover(base: Path | None = None) -> list[Method]:
    base = base or methods_dir()
    out = []
    if base.is_dir():
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            mf = d / "method.toml"
            if mf.is_file():
                m = load_manifest(mf)
                out.append(Method(str(m.get("id", d.name)), d, m))
    return out


def get_main(method: Method):
    """Import the method's package (lazily) and return its main(argv)."""
    p = str(method.dir)
    if p not in sys.path:
        sys.path.insert(0, p)
    return importlib.import_module(method.module).main


# ---------------------------------------------------------------- doctor
def _frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def stale_claims(method: Method, today: _dt.date | None = None) -> list[str]:
    """Novelty claims older than NOVELTY_MAX_AGE_DAYS. A warning, not a failure (see `doctor --fail-on-stale`)."""
    today = today or _dt.date.today()
    try:
        age = (today - _dt.date.fromisoformat(str(method.manifest.get("novelty", {}).get("checked_on")))).days
    except ValueError:
        return []
    if age > NOVELTY_MAX_AGE_DAYS:
        return [f"novelty claim is {age} days old (> {NOVELTY_MAX_AGE_DAYS}): re-run tools/github_scan2.py and update method.toml"]
    return []


def doctor(method: Method) -> list[str]:
    """Return a list of problems (empty = healthy). Pure: reads files, never writes."""
    m, d, problems = method.manifest, method.dir, []

    for k in REQUIRED_KEYS:
        if not m.get(k):
            problems.append(f"manifest: missing '{k}'")
    if m.get("id") and m["id"] != d.name:
        problems.append(f"manifest: id {m['id']!r} must equal folder name {d.name!r}")
    if m.get("family") and m["family"] not in FAMILIES:
        problems.append(f"manifest: family must be one of {FAMILIES}")
    if m.get("status") and m["status"] not in STATUSES:
        problems.append(f"manifest: status must be one of {STATUSES}")

    sources = m.get("sources", [])
    if not sources:
        problems.append("manifest: at least one [[sources]] entry is required")
    for i, s in enumerate(sources):
        if s.get("verification") not in VERIFICATION:
            problems.append(f"sources[{i}]: verification must be one of {VERIFICATION}")
        if s.get("verification") in ("read", "blocked") and not s.get("url"):
            problems.append(f"sources[{i}]: '{s.get('verification')}' requires a url")
        if s.get("verification") != "unverified" and not (s.get("url") or s.get("citation")):
            problems.append(f"sources[{i}]: needs a url or a citation")

    nov = m.get("novelty", {})
    if nov.get("status") not in NOVELTY:
        problems.append(f"novelty: status must be one of {NOVELTY}")
    try:
        _dt.date.fromisoformat(str(nov.get("checked_on")))
    except ValueError:
        problems.append("novelty: checked_on must be an ISO date (YYYY-MM-DD)")

    card = d / "CARD.md"
    if not card.is_file():
        problems.append("CARD.md is missing (copy templates/methodology-card.md)")
    else:
        heads = {h.strip().lower() for h in re.findall(r"^##\s+(.+)$", card.read_text(encoding="utf-8"), re.M)}
        for sec in CARD_SECTIONS:
            if sec.lower() not in heads:
                problems.append(f"CARD.md: missing section '## {sec}'")

    surfaces = m.get("surfaces", {})
    for k in surfaces:
        if k not in SURFACES:
            problems.append(f"surfaces: unknown surface {k!r}")
    if surfaces.get("cli"):
        if not method.module or not (d / method.module).is_dir():
            problems.append("surfaces.cli: [python].module must be a package folder inside the method")
    if surfaces.get("skill"):
        sk = d / "skill" / "SKILL.md"
        if not sk.is_file():
            problems.append("surfaces.skill: skill/SKILL.md is missing")
        else:
            fm = _frontmatter(sk.read_text(encoding="utf-8"))
            if not fm.get("name") or not fm.get("description"):
                problems.append("SKILL.md: frontmatter needs 'name' and 'description'")
            elif len(fm["description"]) > SKILL_DESCRIPTION_MAX:
                problems.append(f"SKILL.md: description is {len(fm['description'])} chars (max {SKILL_DESCRIPTION_MAX}); "
                                "descriptions cost context tokens in every session")
    if not any((d / "tests").glob("test_*.py")):
        problems.append("tests/: at least one test_*.py is required")
    if not (d / "examples").is_dir() or not any((d / "examples").iterdir()):
        problems.append("examples/: at least one runnable example is required")
    return problems
