"""Data model and validation for ACH (Analysis of Competing Hypotheses).

Stdlib only. Input format: JSON (see examples/flaky-test.json).

Key semantics
-------------
* Each *evidence* item is an observable statement ("the test fails only with -n 4").
* `ratings[h]` says how consistent that statement is with hypothesis h:
    CC very consistent | C consistent | N neutral/not applicable | I inconsistent | II very inconsistent
* status="observed": already observed (enters the score).
* status="proposed": not observed yet; `ratings` are *predictions*
  (which hypothesis predicts we would see this?). Only feeds `next`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .i18n import t

RATING_VALUE = {"CC": 2, "C": 1, "N": 0, "I": -1, "II": -2}
LEVEL_VALUE = {"low": 1, "medium": 2, "high": 3}
COST_VALUE = {"low": 1, "medium": 2, "high": 3}
STATUSES = ("observed", "proposed")

DEFAULT_REFUTE_THRESHOLD = 6


class ACHError(ValueError):
    """Invalid input (reported to the user without a traceback)."""


@dataclass(frozen=True)
class Hypothesis:
    id: str
    text: str
    catch_all: bool = False   # "something else": never leads and is not used to separate tests


@dataclass(frozen=True)
class Evidence:
    id: str
    text: str
    status: str
    credibility: str
    relevance: str
    cost: str
    ref: str
    ratings: dict[str, str] = field(default_factory=dict)

    @property
    def weight(self) -> int:
        """credibility x relevance, 1..9. Clarent's own parametrization."""
        return LEVEL_VALUE[self.credibility] * LEVEL_VALUE[self.relevance]

    def value(self, hid: str) -> int:
        return RATING_VALUE[self.ratings.get(hid, "N")]


@dataclass(frozen=True)
class Analysis:
    title: str
    question: str
    hypotheses: tuple[Hypothesis, ...]
    evidence: tuple[Evidence, ...]
    refute_threshold: int
    warnings: tuple[str, ...]

    @property
    def observed(self) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence if e.status == "observed")

    @property
    def proposed(self) -> tuple[Evidence, ...]:
        return tuple(e for e in self.evidence if e.status == "proposed")


def _need(d: dict, key: str, where: str) -> object:
    if not isinstance(d, dict) or key not in d or d[key] in ("", None):
        raise ACHError(t("missing_field", where=where, key=key))
    return d[key]


def _level(d: dict, key: str, default: str, where: str, table: dict) -> str:
    v = str(d.get(key, default)).lower()
    if v not in table:
        raise ACHError(t("bad_level", where=where, key=key, allowed=sorted(table), v=v))
    return v


def parse(data: dict, *, strict: bool = False) -> Analysis:
    """Validate `data` and return an Analysis. In strict mode warnings become errors."""
    if not isinstance(data, dict):
        raise ACHError(t("root_not_object"))
    warnings: list[str] = []

    raw_h = data.get("hypotheses")
    if not isinstance(raw_h, list) or len(raw_h) < 2:
        raise ACHError(t("need_2_hyp"))
    hyps: list[Hypothesis] = []
    for i, h in enumerate(raw_h):
        where = f"hypotheses[{i}]"
        hid = str(_need(h, "id", where))
        if any(x.id == hid for x in hyps):
            raise ACHError(t("dup_id", where=where, id=hid))
        hyps.append(Hypothesis(hid, str(_need(h, "text", where)), bool(h.get("catch_all", False))))
    hids = {h.id for h in hyps}

    raw_e = data.get("evidence")
    if not isinstance(raw_e, list) or not raw_e:
        raise ACHError(t("need_1_ev"))
    evs: list[Evidence] = []
    for i, e in enumerate(raw_e):
        where = f"evidence[{i}]"
        eid = str(_need(e, "id", where))
        if any(x.id == eid for x in evs):
            raise ACHError(t("dup_id", where=where, id=eid))
        status = str(e.get("status", "observed")).lower()
        if status not in STATUSES:
            raise ACHError(t("bad_status", where=where, allowed=STATUSES))
        ratings_raw = e.get("ratings", {})
        if not isinstance(ratings_raw, dict):
            raise ACHError(t("ratings_not_obj", where=where))
        ratings: dict[str, str] = {}
        for hid, r in ratings_raw.items():
            if hid not in hids:
                raise ACHError(t("unknown_hyp", where=where, hid=hid))
            r = str(r).upper()
            if r not in RATING_VALUE:
                raise ACHError(t("bad_rating", where=where, r=r, allowed=list(RATING_VALUE)))
            ratings[hid] = r
        missing = sorted(hids - set(ratings))
        if missing:
            warnings.append(t("w_missing_rating", eid=eid, ids=", ".join(missing)))
        ref = str(e.get("ref", "")).strip()
        if status == "observed" and not ref:
            warnings.append(t("w_uncited", eid=eid))
        evs.append(
            Evidence(
                id=eid,
                text=str(_need(e, "text", where)),
                status=status,
                credibility=_level(e, "credibility", "medium", where, LEVEL_VALUE),
                relevance=_level(e, "relevance", "medium", where, LEVEL_VALUE),
                cost=_level(e, "cost", "medium", where, COST_VALUE),
                ref=ref,
                ratings=ratings,
            )
        )

    if all(h.catch_all for h in hyps):
        raise ACHError(t("all_catch_all"))
    if len(hyps) < 3:
        warnings.append(t("w_two_hyp"))
    elif not any(h.catch_all for h in hyps):
        warnings.append(t("w_no_catch_all"))
    observed = [e for e in evs if e.status == "observed"]
    if 0 < len(observed) < 4:
        warnings.append(t("w_few_obs", n=len(observed)))
    if observed and not any(
        e.ratings.get(h.id) in ("I", "II") for e in observed for h in hyps
    ):
        warnings.append(t("w_only_confirms"))

    threshold = int(data.get("refute_threshold", DEFAULT_REFUTE_THRESHOLD))
    if strict and warnings:
        raise ACHError(t("strict_fail") + "\n  - " + "\n  - ".join(warnings))
    return Analysis(
        title=str(data.get("title", "ACH analysis")),
        question=str(data.get("question", "")),
        hypotheses=tuple(hyps),
        evidence=tuple(evs),
        refute_threshold=threshold,
        warnings=tuple(warnings),
    )
