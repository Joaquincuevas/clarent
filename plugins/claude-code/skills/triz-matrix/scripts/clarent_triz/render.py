"""Markdown rendering for the TRIZ matrix tool (meant to be pasted into an ADR, issue or PR)."""
from __future__ import annotations

from .engine import Analysis, Lookup
from .i18n import t
from .model import Matrix


def _cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def _ids(ps) -> str:
    return ", ".join(str(p.id) for p in ps) if ps else t("st_contested_empty")


def _resolved(lk: Lookup, queries: tuple[str, str] | None) -> list[str]:
    if not queries:
        return []
    out = []
    for q, p, how in ((queries[0], lk.improving, lk.how[0]), (queries[1], lk.worsening, lk.how[1])):
        if how != "id" and q.strip().lower() not in (p.en.lower(), p.es.lower()):
            out.append("- " + t("interpreted", q=q, id=p.id, name=p.name(), how=t("how_" + how)))
    return out


def lookup_body(lk: Lookup, queries: tuple[str, str] | None = None, level: str = "##") -> list[str]:
    L = [f"- **{t('improving')}:** {lk.improving.id}. {lk.improving.name()} — _{t('sw_reading')}: {lk.improving.software()}_",
         f"- **{t('worsening')}:** {lk.worsening.id}. {lk.worsening.name()} — _{t('sw_reading')}: {lk.worsening.software()}_"]
    L += _resolved(lk, queries)
    L.append("")
    if lk.kind == "same-parameter":
        return L + [t("same_param"), ""]
    if lk.status == "verified":
        L += [f"> {t('st_verified', n=lk.agree)}", ""]
    elif lk.status == "contested":
        L += [f"> **{t('st_contested', n=lk.agree, alt=_ids(lk.alt or ()))}**", ""]
    elif lk.status == "consensus":
        L += [f"> {t('st_consensus', n=lk.agree)}", ""]
    if lk.kind == "empty":
        L += [t("empty_cell"), ""]
        if lk.alt:
            L += [f"> **{t('st_contested', n=lk.agree, alt=_ids(lk.alt))}**", ""]
    else:
        L += [f"{level} {t('h_principles')}", "",
              f"| # | {t('col_principle')} | {t('col_meaning')} | {t('col_example')} |", "|--:|---|---|---|"]
        for p in lk.principles:
            L.append(f"| {p.id} | **{_cell(p.name())}** | {_cell(p.description())} | {_cell(p.example())} |")
        L += ["", t("idea_note", imp=lk.improving.name(), wor=lk.worsening.name()), ""]
    L.append(t("reverse", wor=lk.worsening.name(), imp=lk.improving.name(), ids=_ids(lk.reverse))
             if lk.reverse else t("reverse_none", wor=lk.worsening.name(), imp=lk.improving.name()))
    L.append("")
    return L


def lookup_markdown(lk: Lookup, queries: tuple[str, str] | None = None) -> str:
    L = [f"# {t('h_lookup', imp=lk.improving.name(), wor=lk.worsening.name())}", ""]
    L += lookup_body(lk, queries)
    L += ["---", t("footer"), ""]
    return "\n".join(L)


def ranking_table(a: Analysis, limit: int | None = None) -> list[str]:
    L = [t("rank_note"), "", f"| {t('col_count')} | # | {t('col_principle')} | {t('col_pairs')} |", "|--:|--:|---|---|"]
    for r in a.ranking[:limit]:
        flag = f" ⚠ {t('contested_in_rank')}" if r.contested else ""
        L.append(f"| {r.count}/{len(a.lookups)} | {r.principle.id} | **{_cell(r.principle.name())}** — "
                 f"{_cell(r.principle.example())} | {', '.join(map(str, r.pairs))}{flag} |")
    L.append("")
    return L


def analysis_markdown(a: Analysis, title: str = "", context: str = "", notes: list[str] | None = None,
                      queries: list[tuple[str, str]] | None = None) -> str:
    L = [f"# {t('h_analysis', title=title or '-')}", ""]
    if context:
        L += [context, ""]
    L += [f"## {t('h_rank')}", ""] + ranking_table(a)
    for n, lk in enumerate(a.lookups, start=1):
        L += [f"## {t('h_pair', n=n, imp=lk.improving.name(), wor=lk.worsening.name())}", ""]
        if notes and notes[n - 1]:
            L += [f"_{notes[n - 1]}_", ""]
        L += lookup_body(lk, queries[n - 1] if queries else None, level="###")
    L += ["---", t("footer"), ""]
    return "\n".join(L)


def params_markdown(m: Matrix) -> str:
    L = [f"# {t('h_params')}", "", t("params_note"), "",
         f"| {t('col_id')} | {t('col_name')} | {t('sw_reading')} |", "|--:|---|---|"]
    for p in m.params.values():
        L.append(f"| {p.id} | {_cell(p.name())} | {_cell(p.software())} |")
    return "\n".join(L + [""])


def principles_markdown(m: Matrix) -> str:
    L = [f"# {t('h_all_principles')}", "",
         f"| {t('col_id')} | {t('col_name')} | {t('col_desc')} | {t('col_example')} |", "|--:|---|---|---|"]
    for p in m.principles.values():
        L.append(f"| {p.id} | **{_cell(p.name())}** | {_cell(p.description())} | {_cell(p.example())} |")
    return "\n".join(L + [""])
