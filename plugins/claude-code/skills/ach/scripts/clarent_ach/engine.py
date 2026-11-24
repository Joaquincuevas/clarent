"""ACH scoring engine. Pure and deterministic: same input -> same output.

Principles taken from Heuer, *Psychology of Intelligence Analysis* (CIA/CSI, 1999):
  1. INconsistency is scored; consistent evidence does not "add up" because it is
     usually consistent with several hypotheses at once.
  2. Evidence that treats every hypothesis the same does not discriminate.
  3. Sensitivity is tested: does the conclusion change if a key item is wrong?
  4. The result is a ranking, NOT a probability.
The numeric weights (I=1, II=2, weight = credibility x relevance, refutation threshold)
are Clarent's own parametrization; they do not come from Heuer.
"""
from __future__ import annotations

from dataclasses import dataclass

from .i18n import t
from .model import COST_VALUE, Analysis, Evidence


def _penalty(value: int) -> int:
    """Only inconsistency is penalized: I -> 1, II -> 2, everything else 0."""
    return max(0, -value)


@dataclass(frozen=True)
class HypothesisScore:
    id: str
    text: str
    inconsistency: int
    rank: int
    refuted: bool
    catch_all: bool
    contradicted_by: tuple[str, ...]   # evidence ids rated I/II, heaviest first
    supported_by: int                  # how many items are C/CC (informational, NOT scored)


@dataclass(frozen=True)
class EvidenceDiagnostic:
    id: str
    weight: int
    spread: int            # penalty difference across hypotheses (0 = does not discriminate)
    weighted: int
    kind: str              # "diagnostic" | "supports-only" | "non-diagnostic"


@dataclass(frozen=True)
class Sensitivity:
    evidence_id: str
    leaders_without: tuple[str, ...]
    changes_leader: bool


@dataclass(frozen=True)
class NextTest:
    id: str
    text: str
    contenders_spread: int
    priority: float
    separates: tuple[str, ...]   # hypotheses the test predicts as "consistent" (C/CC)
    against: tuple[str, ...]     # hypotheses the test predicts as "inconsistent" (I/II)


@dataclass(frozen=True)
class Result:
    verdict: str                   # no-discrimination | single-leader | tied-leaders
    fragile: bool
    margin: int | None             # inconsistency(2nd) - inconsistency(leader)
    leaders: tuple[str, ...]
    scores: tuple[HypothesisScore, ...]
    diagnostics: tuple[EvidenceDiagnostic, ...]
    sensitivity: tuple[Sensitivity, ...]
    next_tests: tuple[NextTest, ...]
    warnings: tuple[str, ...]


def _inconsistency(an: Analysis, hid: str, skip: str | None = None) -> int:
    return sum(
        e.weight * _penalty(e.value(hid)) for e in an.observed if e.id != skip
    )


def _specific(an: Analysis):
    return [h for h in an.hypotheses if not h.catch_all]


def _leaders(an: Analysis, skip: str | None = None) -> tuple[str, ...]:
    """Leaders among specific hypotheses (the catch-all never leads)."""
    totals = {h.id: _inconsistency(an, h.id, skip) for h in _specific(an)}
    best = min(totals.values())
    return tuple(h.id for h in _specific(an) if totals[h.id] == best)


def score(an: Analysis) -> Result:
    hyp_ids = [h.id for h in an.hypotheses]
    totals = {hid: _inconsistency(an, hid) for hid in hyp_ids}
    spec_ids = [h.id for h in _specific(an)]
    distinct = sorted({totals[i] for i in spec_ids})
    rank_of = {v: i + 1 for i, v in enumerate(sorted(set(totals.values())))}

    scores = []
    for h in an.hypotheses:
        contra = sorted(
            (e for e in an.observed if _penalty(e.value(h.id)) > 0),
            key=lambda e: (-e.weight * _penalty(e.value(h.id)), e.id),
        )
        scores.append(
            HypothesisScore(
                id=h.id,
                text=h.text,
                inconsistency=totals[h.id],
                rank=rank_of[totals[h.id]],
                refuted=totals[h.id] >= an.refute_threshold,
                catch_all=h.catch_all,
                contradicted_by=tuple(e.id for e in contra),
                supported_by=sum(1 for e in an.observed if e.value(h.id) > 0),
            )
        )
    scores.sort(key=lambda s: (s.inconsistency, s.id))

    leaders = _leaders(an)
    margin = None
    if len(distinct) > 1:
        margin = distinct[1] - distinct[0]

    if len(distinct) == 1:
        verdict = "no-discrimination"
    elif len(leaders) == 1:
        verdict = "single-leader"
    else:
        verdict = "tied-leaders"

    diags = []
    for e in an.observed:
        pens = [_penalty(e.value(hid)) for hid in hyp_ids]
        vals = [e.value(hid) for hid in hyp_ids]
        spread = max(pens) - min(pens)
        if spread > 0:
            kind = "diagnostic"
        elif max(vals) != min(vals):
            kind = "supports-only"   # separates C from CC, but ACH does not score consistency
        else:
            kind = "non-diagnostic"
        diags.append(EvidenceDiagnostic(e.id, e.weight, spread, spread * e.weight, kind))
    diags.sort(key=lambda d: (-d.weighted, d.id))

    sens = []
    for e in an.observed:
        without = _leaders(an, skip=e.id)
        sens.append(Sensitivity(e.id, without, set(without) != set(leaders)))
    fragile = any(s.changes_leader for s in sens) and verdict != "no-discrimination"

    warnings = list(an.warnings)
    for h in an.hypotheses:
        if h.catch_all and totals[h.id] <= distinct[0]:
            warnings.append(t("w_catch_all_alive", id=h.id))
    if verdict == "no-discrimination":
        warnings.append(t("w_no_discrim"))
    if fragile:
        crit = ", ".join(s.evidence_id for s in sens if s.changes_leader)
        warnings.append(t("w_fragile", crit=crit))
    if all(s.refuted for s in scores if not s.catch_all):
        warnings.append(t("w_all_refuted"))

    return Result(
        verdict=verdict,
        fragile=fragile,
        margin=margin,
        leaders=leaders,
        scores=tuple(scores),
        diagnostics=tuple(diags),
        sensitivity=tuple(sens),
        next_tests=next_tests(an, scores),
        warnings=tuple(warnings),
    )


def _contenders(scores: list[HypothesisScore]) -> list[str]:
    spec = [s for s in scores if not s.catch_all]
    live = [s.id for s in spec if not s.refuted]
    return live if len(live) >= 2 else [s.id for s in spec]


def next_tests(an: Analysis, scores: list[HypothesisScore]) -> tuple[NextTest, ...]:
    """Rank proposed tests by how well they separate the hypotheses still alive.

    spread = max(rating) - min(rating) among contenders (the test is informative
    whether the outcome is 'yes' or 'no'). priority = spread * weight / cost.
    """
    contenders = _contenders(scores)
    out = []
    for e in an.proposed:
        vals = {hid: e.value(hid) for hid in contenders}
        spread = max(vals.values()) - min(vals.values())
        if spread == 0:
            continue
        out.append(
            NextTest(
                id=e.id,
                text=e.text,
                contenders_spread=spread,
                priority=round(spread * e.weight / COST_VALUE[e.cost], 3),
                separates=tuple(h for h, v in vals.items() if v > 0),
                against=tuple(h for h, v in vals.items() if v < 0),
            )
        )
    out.sort(key=lambda x: (-x.priority, x.id))
    return tuple(out)


def to_dict(r: Result) -> dict:
    """Stable serialization for --format json."""
    from dataclasses import asdict

    return asdict(r)
