"""Matrix lookup and principle ranking. Pure and deterministic: same input and data -> same output.

This engine does NOT generate solutions. It returns the principles the classical matrix associates with a pair of
parameters, tells you how far the cell can be trusted, and ranks principles across several contradictions.
"""
from __future__ import annotations

from dataclasses import dataclass

from .model import Cell, Matrix, Param, Principle, resolve


@dataclass(frozen=True)
class Lookup:
    improving: Param
    worsening: Param
    how: tuple[str, str]                       # how each query was resolved: id | name | software
    kind: str                                  # principles | empty | same-parameter
    principles: tuple[Principle, ...]
    status: str | None                         # verified | contested | consensus (None if no cell)
    agree: int | None
    alt: tuple[Principle, ...] | None          # the 1973 table's reading when contested
    reverse: tuple[Principle, ...]             # principles of the reverse cell (worsen, improve)


@dataclass(frozen=True)
class RankedPrinciple:
    principle: Principle
    count: int
    pairs: tuple[int, ...]                     # 1-based indexes of the contradictions that list it
    mean_position: float
    contested: bool


@dataclass(frozen=True)
class Analysis:
    lookups: tuple[Lookup, ...]
    ranking: tuple[RankedPrinciple, ...]


def _cell(m: Matrix, i: int, j: int) -> Cell | None:
    return m.cells.get((i, j))


def lookup(m: Matrix, improving: str, worsening: str) -> Lookup:
    pi, hi = resolve(m, improving)
    pw, hw = resolve(m, worsening)
    if pi.id == pw.id:
        return Lookup(pi, pw, (hi, hw), "same-parameter", (), None, None, None, ())
    cell = _cell(m, pi.id, pw.id)
    back = _cell(m, pw.id, pi.id)
    reverse = tuple(m.principles[x] for x in back.principles) if back else ()
    if cell is None or not cell.principles:
        # A contested empty cell can still carry a 1973 reading in `alt`.
        alt = tuple(m.principles[x] for x in cell.alt) if cell and cell.alt else None
        return Lookup(pi, pw, (hi, hw), "empty", (), cell.status if cell else None, cell.agree if cell else None, alt, reverse)
    alt = tuple(m.principles[x] for x in cell.alt) if cell.alt is not None else None
    return Lookup(pi, pw, (hi, hw), "principles", tuple(m.principles[x] for x in cell.principles),
                  cell.status, cell.agree, alt, reverse)


def rank(m: Matrix, pairs: list[tuple[str, str]]) -> Analysis:
    """Look up every pair and rank principles by how many contradictions list them (then by mean position)."""
    lookups = tuple(lookup(m, a, b) for a, b in pairs)
    seen: dict[int, list[tuple[int, int, bool]]] = {}
    for n, lk in enumerate(lookups, start=1):
        for pos, pr in enumerate(lk.principles, start=1):
            seen.setdefault(pr.id, []).append((n, pos, lk.status == "contested"))
    ranked = [
        RankedPrinciple(m.principles[pid], len(v), tuple(n for n, _, _ in v),
                        round(sum(p for _, p, _ in v) / len(v), 2), any(c for _, _, c in v))
        for pid, v in seen.items()
    ]
    ranked.sort(key=lambda r: (-r.count, r.mean_position, r.principle.id))
    return Analysis(lookups, tuple(ranked))


# ---------------------------------------------------------------- stable serialization
def principle_dict(p: Principle) -> dict:
    return {"id": p.id, "name": p.name(), "description": p.description(), "software_example": p.example()}


def lookup_dict(lk: Lookup) -> dict:
    return {
        "improving": {"id": lk.improving.id, "name": lk.improving.name(), "software_reading": lk.improving.software(),
                      "resolved_by": lk.how[0]},
        "worsening": {"id": lk.worsening.id, "name": lk.worsening.name(), "software_reading": lk.worsening.software(),
                      "resolved_by": lk.how[1]},
        "kind": lk.kind,
        "status": lk.status,
        "sources_agreeing": lk.agree,
        "principles": [principle_dict(p) for p in lk.principles],
        "alternative_1973": [principle_dict(p) for p in lk.alt] if lk.alt is not None else None,
        "reverse_cell": [p.id for p in lk.reverse],
    }


def analysis_dict(a: Analysis) -> dict:
    return {
        "contradictions": [lookup_dict(lk) for lk in a.lookups],
        "ranking": [{"principle": principle_dict(r.principle), "count": r.count, "contradictions": list(r.pairs),
                     "mean_position": r.mean_position, "contested": r.contested} for r in a.ranking],
    }
