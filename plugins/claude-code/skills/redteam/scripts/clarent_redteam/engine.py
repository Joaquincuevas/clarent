"""The deterministic core: reject what cannot be backed, score what can, and list what to verify next.

What the engine does, in order (no LLM involved anywhere):

1. **Anchor.** Every assumption and every attack must quote a passage that appears *literally* in the target
   (whitespace is ignored, nothing else). No quote, a quote that is too short, or a quote that is not there: rejected.
2. **Back the status.** `verified` and `contradicted` need at least one evidence item. A `file:line` ref must point at
   a line that exists. Anything else a model wrote is free text (a command, a log excerpt) and is only required to be
   non-empty: the engine cannot run it, and the report says so.
3. **Cascade and de-duplicate.** An attack on a rejected assumption is rejected. Two attacks of the same class on the
   same assumption with near-identical text count once.
4. **Score.** `risk = impact x effective plausibility`, both on 1..5. The assumption's status moves plausibility:
   `contradicted` -> 5 (the premise is already false); `verified` -> at most 2 (the premise holds); `unverified` -> as rated.
   Severity bands S1..S4 and every constant are Clarent's parametrization.
5. **Report.** Assumption matrix (assumption x attack class), the top 3 attacks, what to verify next, class coverage.

The engine never judges whether an attack is *right*; it judges whether it is *anchored and backed*.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .catalog import CATALOG, CLASSES, SEVERITY_ORDER, severity
from .i18n import t
from .model import MIN_QUOTE_CHARS, Assumption, Attack, Findings, check_ref, find_quote

TOP_N = 3
DUPLICATE_JACCARD = 0.8
FEW_ASSUMPTIONS = 3


@dataclass(frozen=True)
class Rejection:
    kind: str                       # 'assumption' | 'attack'
    id: str
    code: str
    detail: str


@dataclass(frozen=True)
class AssumptionRow:
    id: str
    text: str
    status: str
    where: str                      # file:line of the anchoring quote
    evidence: tuple[tuple[str, str], ...]
    attacks_by_class: dict[str, tuple[str, ...]]
    max_risk: int
    check: str


@dataclass(frozen=True)
class AttackRow:
    rank: int
    id: str
    class_id: str
    assumption: str
    assumption_status: str
    impact: int
    plausibility: int
    effective_plausibility: int
    risk: int
    severity: str
    where: str
    quote: str
    text: str
    check: str
    evidence_count: int


@dataclass(frozen=True)
class Coverage:
    class_id: str
    attack_ids: tuple[str, ...]
    skipped_reason: str             # '' if not skipped


@dataclass(frozen=True)
class VerifyNext:
    assumption: str
    text: str
    max_risk: int
    check: str


@dataclass
class Result:
    assumptions: list[AssumptionRow] = field(default_factory=list)
    attacks: list[AttackRow] = field(default_factory=list)
    top: list[AttackRow] = field(default_factory=list)
    rejections: list[Rejection] = field(default_factory=list)
    coverage: list[Coverage] = field(default_factory=list)
    verify_next: list[VerifyNext] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def worst_severity(self) -> str | None:
        return min((a.severity for a in self.attacks), key=SEVERITY_ORDER.index, default=None)

    def status_counts(self) -> dict[str, int]:
        c = {"verified": 0, "unverified": 0, "contradicted": 0}
        for a in self.assumptions:
            c[a.status] += 1
        return c


# ------------------------------------------------------------------ helpers
def effective_plausibility(plausibility: int, status: str) -> int:
    """Move plausibility with the assumption's status (Clarent's rule, see module docstring)."""
    if status == "contradicted":
        return 5
    if status == "verified":
        return min(plausibility, 2)
    return plausibility


def _words(s: str) -> set[str]:
    return set(re.findall(r"\w+", s.lower()))


def _jaccard(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    return len(wa & wb) / len(wa | wb) if wa | wb else 0.0


def _ref_problem(refs, root) -> str | None:
    """None if every evidence item is usable, else the reason (translated)."""
    for e in refs:
        if not e.ref or not e.observation:
            return t("r_ref_invalid", ref=e.ref or "—", why=t("why_empty"))
        ok, why = check_ref(e.ref, root)
        if not ok:
            key, _, n = why.partition(":")
            return t("r_ref_invalid", ref=e.ref, why=t(key, n=n) if n else t(key))
    return None


def _anchor(quote: str, f: Findings) -> tuple[str, str]:
    """Return (where, '') if the quote anchors in the target, else ('', rejection code)."""
    if not quote:
        return "", "quote_missing"
    if len(" ".join(quote.split())) < MIN_QUOTE_CHARS:
        return "", "quote_short"
    hit = find_quote(f.files, quote)
    if hit is None:
        return "", "quote_not_found"
    return f"{hit[0]}:{hit[1]}", ""


def _reject_msg(code: str, quote: str) -> str:
    if code == "quote_short":
        return t("r_quote_short", n=len(" ".join(quote.split())), min=MIN_QUOTE_CHARS)
    return t("r_" + code)


# ------------------------------------------------------------------ analysis
def analyze(f: Findings) -> Result:
    res = Result()
    rej = res.rejections

    # 1-2. assumptions
    good_a: dict[str, tuple[Assumption, str]] = {}
    for a in f.assumptions:
        where, code = _anchor(a.quote, f)
        if code:
            rej.append(Rejection("assumption", a.id, code, _reject_msg(code, a.quote)))
            continue
        problem = _ref_problem(a.evidence, f.root)
        if problem:
            rej.append(Rejection("assumption", a.id, "ref_invalid", problem))
            continue
        if a.status in ("verified", "contradicted") and not a.evidence:
            rej.append(Rejection("assumption", a.id, "no_evidence", t("r_no_evidence", status=a.status)))
            continue
        good_a[a.id] = (a, where)

    # 1-3. attacks
    accepted: list[Attack] = []
    where_of: dict[str, str] = {}
    for x in f.attacks:
        if x.assumption not in good_a:
            rej.append(Rejection("attack", x.id, "assumption_rejected", t("r_assumption_rejected", aid=x.assumption)))
            continue
        where, code = _anchor(x.quote, f)
        if code:
            rej.append(Rejection("attack", x.id, code, _reject_msg(code, x.quote)))
            continue
        problem = _ref_problem(x.evidence, f.root)
        if problem:
            rej.append(Rejection("attack", x.id, "ref_invalid", problem))
            continue
        if not x.check:
            rej.append(Rejection("attack", x.id, "check_missing", t("r_check_missing")))
            continue
        twin = next((y for y in accepted if y.class_id == x.class_id and y.assumption == x.assumption
                     and _jaccard(y.text, x.text) >= DUPLICATE_JACCARD), None)
        if twin is not None:
            rej.append(Rejection("attack", x.id, "duplicate", t("r_duplicate", other=twin.id)))
            continue
        accepted.append(x)
        where_of[x.id] = where

    # 4. score
    scored = []
    for x in accepted:
        a, _ = good_a[x.assumption]
        eff = effective_plausibility(x.plausibility, a.status)
        risk = x.impact * eff
        scored.append((x, a.status, eff, risk))
    scored.sort(key=lambda s: (-s[3], -s[0].impact, -len(s[0].evidence), s[0].id))
    for i, (x, status, eff, risk) in enumerate(scored, 1):
        res.attacks.append(AttackRow(i, x.id, x.class_id, x.assumption, status, x.impact, x.plausibility, eff, risk,
                                     severity(risk), where_of[x.id], x.quote, x.text, x.check, len(x.evidence)))
    res.top = res.attacks[:TOP_N]

    # 5. matrix, coverage, verify-next
    for a in f.assumptions:
        if a.id not in good_a:
            continue
        _, where = good_a[a.id]
        mine = [r for r in res.attacks if r.assumption == a.id]
        by_class = {c: tuple(r.id for r in mine if r.class_id == c) for c in CLASSES}
        res.assumptions.append(AssumptionRow(a.id, a.text, a.status, where, tuple((e.ref, e.observation) for e in a.evidence),
                                             by_class, max((r.risk for r in mine), default=0), a.check))
    skipped = {s.class_id: s.reason for s in f.skipped}
    for c in CLASSES:
        ids = tuple(r.id for r in res.attacks if r.class_id == c)
        res.coverage.append(Coverage(c, ids, skipped.get(c, "")))
    for row in sorted((r for r in res.assumptions if r.status == "unverified" and r.max_risk),
                      key=lambda r: (-r.max_risk, r.id)):
        res.verify_next.append(VerifyNext(row.id, row.text, row.max_risk, row.check))

    _warnings(f, res)
    return res


def _warnings(f: Findings, res: Result) -> None:
    w = res.warnings
    w.extend(f.warnings)
    lang_name = lambda c: _name(c)
    for cov in res.coverage:
        if not cov.attack_ids and not cov.skipped_reason:
            w.append(t("w_class_uncovered", name=lang_name(cov.class_id)))
        if cov.attack_ids and cov.skipped_reason:
            w.append(t("w_skip_and_attacks", name=lang_name(cov.class_id)))
    for a in res.assumptions:
        if not any(a.attacks_by_class.values()):
            w.append(t("w_unattacked", aid=a.id))
        if a.status == "unverified" and not a.check:
            w.append(t("w_unverified_no_check", aid=a.id))
    if len(res.assumptions) < FEW_ASSUMPTIONS:
        w.append(t("w_few_assumptions", n=len(res.assumptions)))
    if len(res.attacks) < TOP_N:
        w.append(t("w_few_attacks", n=len(res.attacks)))
    shaky = sorted({r.assumption for r in res.top if r.assumption_status == "unverified"})
    if shaky:
        w.append(t("w_top_unverified", ids=", ".join(shaky)))


def _name(class_id: str) -> str:
    from .i18n import get_lang
    return CATALOG[class_id][get_lang()]["name"]


def to_dict(res: Result, title: str = "") -> dict:
    """Stable JSON form (schema clarent.redteam.report/1)."""
    return {
        "schema": "clarent.redteam.report/1",
        "title": title,
        "counts": {**res.status_counts(), "attacks": len(res.attacks), "rejected": len(res.rejections)},
        "worst_severity": res.worst_severity,
        "top": [r.id for r in res.top],
        "attacks": [vars(r) for r in res.attacks],
        "assumptions": [{**vars(r), "evidence": [list(e) for e in r.evidence]} for r in res.assumptions],
        "coverage": [{"class": c.class_id, "attacks": list(c.attack_ids), "skipped_reason": c.skipped_reason}
                     for c in res.coverage],
        "verify_next": [vars(v) for v in res.verify_next],
        "rejected": [vars(r) for r in res.rejections],
        "warnings": list(res.warnings),
    }
