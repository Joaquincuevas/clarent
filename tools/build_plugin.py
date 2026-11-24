"""Assemble the Claude Code plugin from methods/*.

    python tools/build_plugin.py            # (re)generate plugins/claude-code/
    python tools/build_plugin.py --check    # exit 1 if the committed plugin is out of date (used in CI)

For every method that ships a skill, the plugin gets:
    skills/<id>/SKILL.md
    skills/<id>/scripts/<module>/...   (a copy of the stdlib-only engine)
    skills/<id>/scripts/run.py         (entry point the skill calls; no pip install needed)
"""
from __future__ import annotations

import filecmp
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from clarent import __version__, registry  # noqa: E402

OUT = ROOT / "plugins" / "claude-code"
RUN_PY = '''"""Entry point called by the skill. Stdlib only; no installation required."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from {module} import main  # noqa: E402

sys.exit(main())
'''


def build(out: Path) -> list[str]:
    if out.exists():
        shutil.rmtree(out)
    (out / ".claude-plugin").mkdir(parents=True)
    included = []
    for m in registry.discover(ROOT / "methods"):
        if not m.manifest.get("surfaces", {}).get("skill"):
            continue
        sdir = out / "skills" / m.id
        (sdir / "scripts").mkdir(parents=True)
        shutil.copy2(m.dir / "skill" / "SKILL.md", sdir / "SKILL.md")
        shutil.copytree(m.dir / m.module, sdir / "scripts" / m.module,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (sdir / "scripts" / "run.py").write_text(RUN_PY.format(module=m.module), encoding="utf-8", newline="\n")
        included.append(m.id)
    manifest = {
        "name": "clarent-methods",
        "version": __version__,
        "description": "Classic decision and engineering methodologies as executable tools: " + ", ".join(included),
        "author": {"name": "Clarent contributors"},
        "license": "Apache-2.0",
        "keywords": ["methodology", "debugging", "root-cause-analysis", "structured-analytic-techniques"],
    }
    (out / ".claude-plugin" / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return included


def _same(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(_same(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    if "--check" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "claude-code"
            build(fresh)
            if OUT.is_dir() and _same(fresh, OUT):
                print("plugin is up to date")
                return 0
        print("plugins/claude-code is out of date: run `python tools/build_plugin.py` and commit", file=sys.stderr)
        return 1
    print("built plugin with skills:", ", ".join(build(OUT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
