"""Data model, input validation and target indexing for the red team method.

Stdlib only. Input: JSON (see examples/). Two kinds of problem are kept apart on purpose:

* **Malformed input** (not an object, unknown class, duplicate id, a rating of 9, an attack on an assumption that does
  not exist, a target file that cannot be read) raises `RedTeamError`: the file cannot be analysed at all (exit 2).
* **A finding that cannot be backed** (a quote that is not in the target, evidence that points at a line that does not
  exist, "verified" with nothing behind it) is not an error: the engine *rejects that finding*, says why, and goes on.

Everything the model writes about the target is checked against the target's own text: that is the point of the method.
"""
from __future__ import annotations

import bisect
import re
from dataclasses import dataclass, field
from pathlib import Path

from .catalog import CLASSES
from .i18n import t

SCHEMA = "clarent.redteam/1"
KINDS = ("design", "pr")
STATUSES = ("verified", "unverified", "contradicted")
MIN_QUOTE_CHARS = 12          # Clarent's constant: shorter quotes anchor nothing ("the", "retry")
MAX_FILE_BYTES = 2 * 1024 * 1024

_REF_RE = re.compile(r"^(?P<path>[^\s:][^\s:]*\.[A-Za-z0-9_+-]+):(?P<a>\d+)(?:-(?P<b>\d+))?$")


class RedTeamError(ValueError):
    """Invalid input (reported to the user without a traceback)."""


@dataclass(frozen=True)
class Evidence:
    ref: str
    observation: str


@dataclass(frozen=True)
class Assumption:
    id: str
    text: str
    status: str
    quote: str
    evidence: tuple[Evidence, ...]
    check: str


@dataclass(frozen=True)
class Attack:
    id: str
    class_id: str
    assumption: str
    quote: str
    text: str
    impact: int
    plausibility: int
    check: str
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class Skipped:
    class_id: str
    reason: str


@dataclass(frozen=True)
class TargetFile:
    name: str                       # as shown in reports (relative to the root when possible)
    text: str
    is_diff: bool

    @property
    def lines(self) -> list[str]:
        return self.text.splitlines()


@dataclass(frozen=True)
class Findings:
    title: str
    kind: str
    root: Path
    files: tuple[TargetFile, ...]
    assumptions: tuple[Assumption, ...]
    attacks: tuple[Attack, ...]
    skipped: tuple[Skipped, ...]
    warnings: tuple[str, ...] = field(default_factory=tuple)


# ------------------------------------------------------------------ helpers
def _need(d: dict, key: str, where: str):
    if not isinstance(d, dict) or key not in d or d[key] in ("", None):
        raise RedTeamError(t("missing_field", where=where, key=key))
    return d[key]


def _rating(d: dict, key: str, where: str) -> int:
    v = _need(d, key, where)
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5:
        raise RedTeamError(t("bad_rating", where=where, key=key, v=v))
    return v


def _evidence(d: dict, where: str) -> tuple[Evidence, ...]:
    raw = d.get("evidence", [])
    if not isinstance(raw, list):
        raise RedTeamError(t("evidence_not_list", where=where))
    out = []
    for i, e in enumerate(raw):
        if not isinstance(e, dict):
            raise RedTeamError(t("not_object", where=f"{where}.evidence[{i}]"))
        out.append(Evidence(str(e.get("ref", "")).strip(), str(e.get("observation", "")).strip()))
    return tuple(out)


def _inside(root: Path, rel: str) -> Path | None:
    """Resolve `rel` under `root`; None if it escapes (absolute paths and '..' are not allowed in the file)."""
    p = (root / rel).resolve()
    try:
        p.relative_to(root.resolve())
    except ValueError:
        return None
    return p


def _read(path: Path, shown: str) -> str:
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            raise RedTeamError(t("target_big", path=shown, mb=MAX_FILE_BYTES // (1024 * 1024)))
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        raise RedTeamError(t("target_missing", path=shown))
    except OSError as e:
        raise RedTeamError(t("target_unreadable", path=shown, e=e))


def _looks_like_diff(name: str, text: str) -> bool:
    if name.lower().endswith((".diff", ".patch")):
        return True
    return any(l.startswith("diff --git ") or l.startswith("@@ ") for l in text.splitlines()[:400])


# ------------------------------------------------------------------ parse
def parse(data: dict, base_dir: Path, *, root: Path | None = None, targets: list[str] | None = None) -> Findings:
    """Validate `data` and read the target. `base_dir` is the folder of the findings file.

    The root is where target files and `file:line` refs are resolved: `root` if given, else the file's own `"root"`
    (relative to `base_dir`, default "."). Paths written *inside the file* cannot leave the root; paths given with
    `targets` (the --target option) are the user's own and are read as given.
    """
    if not isinstance(data, dict):
        raise RedTeamError(t("root_not_object"))
    if "schema" in data and data["schema"] != SCHEMA:
        raise RedTeamError(t("bad_schema", got=data["schema"]))
    warnings: list[str] = []

    root_dir = (root if root is not None else base_dir / str(data.get("root", "."))).resolve()
    tgt = data.get("target", {})
    if not isinstance(tgt, dict):
        raise RedTeamError(t("not_object", where="target"))
    kind = str(tgt.get("kind", "design")).lower()
    if kind not in KINDS:
        raise RedTeamError(t("bad_kind", v=kind))

    files: list[TargetFile] = []
    if targets:
        for tp in targets:
            p = Path(tp)
            files.append(_make_file(tp, _read(p, tp)))
    else:
        raw = tgt.get("files")
        if raw is None:
            raise RedTeamError(t("no_target"))
        if not isinstance(raw, list) or not raw or not all(isinstance(x, str) and x for x in raw):
            raise RedTeamError(t("target_not_list"))
        for rel in raw:
            p = _inside(root_dir, rel)
            if p is None:
                raise RedTeamError(t("target_outside", path=rel, root=root_dir))
            files.append(_make_file(rel.replace("\\", "/"), _read(p, rel)))

    raw_a = data.get("assumptions")
    if not isinstance(raw_a, list) or not raw_a:
        raise RedTeamError(t("need_list", key="assumptions"))
    assumptions: list[Assumption] = []
    for i, a in enumerate(raw_a):
        where = f"assumptions[{i}]"
        if not isinstance(a, dict):
            raise RedTeamError(t("not_object", where=where))
        aid = str(_need(a, "id", where))
        if any(x.id == aid for x in assumptions):
            raise RedTeamError(t("dup_id", where=where, id=aid))
        status = str(a.get("status", "unverified")).lower()
        if status not in STATUSES:
            raise RedTeamError(t("bad_status", where=where, allowed=STATUSES, v=status))
        assumptions.append(Assumption(aid, str(_need(a, "text", where)), status, str(a.get("quote", "")).strip(),
                                      _evidence(a, where), str(a.get("check", "")).strip()))
    aids = {a.id for a in assumptions}

    raw_x = data.get("attacks")
    if not isinstance(raw_x, list) or not raw_x:
        raise RedTeamError(t("need_list", key="attacks"))
    attacks: list[Attack] = []
    for i, x in enumerate(raw_x):
        where = f"attacks[{i}]"
        if not isinstance(x, dict):
            raise RedTeamError(t("not_object", where=where))
        xid = str(_need(x, "id", where))
        if any(y.id == xid for y in attacks):
            raise RedTeamError(t("dup_id", where=where, id=xid))
        cls = str(_need(x, "class", where))
        if cls not in CLASSES:
            raise RedTeamError(t("bad_class", where=where, allowed=CLASSES, v=cls))
        aref = str(_need(x, "assumption", where))
        if aref not in aids:
            raise RedTeamError(t("unknown_assumption", where=where, aid=aref))
        attacks.append(Attack(xid, cls, aref, str(x.get("quote", "")).strip(), str(_need(x, "attack", where)),
                              _rating(x, "impact", where), _rating(x, "plausibility", where),
                              str(x.get("check", "")).strip(), _evidence(x, where)))

    skipped: list[Skipped] = []
    raw_s = data.get("skipped_classes", [])
    if not isinstance(raw_s, list):
        raise RedTeamError(t("need_list", key="skipped_classes"))
    for i, s in enumerate(raw_s):
        where = f"skipped_classes[{i}]"
        if not isinstance(s, dict):
            raise RedTeamError(t("not_object", where=where))
        cls = str(_need(s, "class", where))
        if cls not in CLASSES:
            raise RedTeamError(t("bad_class", where=where, allowed=CLASSES, v=cls))
        reason = str(s.get("reason", "")).strip()
        if not reason:
            warnings.append(t("w_skip_no_reason", name=cls))
            continue
        skipped.append(Skipped(cls, reason))

    return Findings(str(data.get("title", "Red team")), kind, root_dir, tuple(files), tuple(assumptions),
                    tuple(attacks), tuple(skipped), tuple(warnings))


def _make_file(name: str, text: str) -> TargetFile:
    return TargetFile(name, text, _looks_like_diff(name, text))


# ------------------------------------------------------------------ anchoring
def _views(f: TargetFile) -> list[list[tuple[str, int]]]:
    """Token streams (token, 1-based line) in which a quote may be found.

    View 1 is the file as written. For a diff, view 2 drops the leading '+', '-' or ' ' of each hunk line, so a quote
    copied from the code (without the diff markers) still anchors to the line it came from.
    """
    raw = [(tok, n) for n, line in enumerate(f.lines, 1) for tok in line.split()]
    views = [raw]
    if f.is_diff:
        body, in_hunk = [], False
        for n, line in enumerate(f.lines, 1):
            if line.startswith("@@"):
                in_hunk = True
                continue
            if line.startswith("diff --git"):
                in_hunk = False
                continue
            if in_hunk and line[:1] in ("+", "-", " ") and not line.startswith(("+++ ", "--- ")):
                body.extend((tok, n) for tok in line[1:].split())
        views.append(body)
    return views


def find_quote(files: tuple[TargetFile, ...], quote: str) -> tuple[str, int] | None:
    """Locate `quote` literally in the target. Returns (file name, first line) or None.

    "Literally" means character by character, case included; the only normalization is that any run of whitespace
    (spaces, tabs, line breaks) counts as one space, so a quote can span a line break of the original.
    """
    q = " ".join(quote.split())
    if not q:
        return None
    for f in files:
        for view in _views(f):
            if not view:
                continue
            text = " ".join(tok for tok, _ in view)
            pos = text.find(q)
            if pos < 0:
                continue
            starts, off = [], 0
            for tok, _ in view:
                starts.append(off)
                off += len(tok) + 1
            return f.name, view[bisect.bisect_right(starts, pos) - 1][1]
    return None


def check_ref(ref: str, root: Path) -> tuple[bool, str]:
    """Validate an evidence ref. `file:line` or `file:a-b` must exist under `root`; anything else is free text
    (a command, a log excerpt) that the engine cannot check and therefore only requires to be non-empty.
    Returns (ok, why) where `why` is an i18n key suffix when not ok."""
    if not ref.strip():
        return False, "why_empty"
    m = _REF_RE.match(ref.strip())
    if not m:
        return True, ""
    p = _inside(root, m.group("path"))
    if p is None:
        return False, "why_outside"
    if not p.is_file():
        return False, "why_not_found"
    try:
        n = len(_read(p, m.group("path")).splitlines())
    except RedTeamError:
        return False, "why_not_found"
    a = int(m.group("a"))
    b = int(m.group("b") or a)
    if not 1 <= a <= b <= n:
        return False, f"why_line:{n}"
    return True, ""
