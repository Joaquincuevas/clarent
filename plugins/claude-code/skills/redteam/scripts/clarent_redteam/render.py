"""Markdown rendering of the red team report (meant to be pasted into a PR, an ADR or a review thread)."""
from __future__ import annotations

from .catalog import CATALOG, CLASSES
from .engine import TOP_N, Result
from .i18n import get_lang, t
from .model import Findings


def _c(s: str) -> str:
    """One table cell: no pipes, no newlines."""
    return " ".join(str(s).split()).replace("|", "\\|")


def _cls(class_id: str) -> str:
    return CATALOG[class_id][get_lang()]["name"]


def _plaus(a) -> str:
    return str(a.plausibility) if a.plausibility == a.effective_plausibility else f"{a.plausibility}→{a.effective_plausibility}"


def markdown(f: Findings, res: Result) -> str:
    L: list[str] = [f"# {t('h_title', title=f.title)}", ""]
    L += [t("target_line", kind=f.kind, files=", ".join(f"`{x.name}`" for x in f.files)), ""]

    n = res.status_counts()
    L += [f"## {t('h_summary')}", "",
          f"- {t('s_assumptions', n=len(res.assumptions), v=n['verified'], u=n['unverified'], c=n['contradicted'])}",
          f"- {t('s_attacks', n=len(res.attacks))}",
          f"- {t('s_severity', sev=res.worst_severity) if res.worst_severity else t('s_none_severity')}"]
    if res.rejections:
        L.append(f"- {t('s_rejected', n=len(res.rejections))}")
    L += [f"- {t('not_probability')}", ""]

    L += [f"## {t('h_top', n=TOP_N)}", ""]
    if res.top:
        L += [f"| {t('col_rank')} | {t('col_attack')} | {t('col_class')} | {t('col_assumption')} | {t('col_risk')} | "
              f"{t('col_where')} | {t('col_check')} |", "|--:|---|---|---|---|---|---|"]
        for a in res.top:
            L.append(f"| {a.rank} | **{a.id}** {_c(a.text)} | {_cls(a.class_id)} | {a.assumption} "
                     f"({t('status_' + a.assumption_status)}) | {a.risk} ({a.severity}) | `{a.where}` | {_c(a.check)} |")
    else:
        L.append(f"- {t('s_none_severity')}")
    L.append("")

    L += [f"## {t('h_matrix')}", "",
          f"| {t('col_assumption')} | {t('col_status')} | " + " | ".join(_cls(c) for c in CLASSES) + f" | {t('col_evidence')} |",
          "|---|---|" + "|".join(":-:" for _ in CLASSES) + "|---|"]
    for a in res.assumptions:
        cells = " | ".join(", ".join(a.attacks_by_class[c]) or "·" for c in CLASSES)
        ev = "; ".join(f"`{r}`" for r, _ in a.evidence) or "—"
        L.append(f"| **{a.id}** {_c(a.text)} (`{a.where}`) | {t('status_' + a.status)} | {cells} | {ev} |")
    L.append("")
    for a in res.assumptions:
        if a.evidence:
            L += [f"- **{a.id}** ({t('status_' + a.status)}): " + " ".join(f"`{r}` — {_c(o)}" for r, o in a.evidence)]
    if any(a.evidence for a in res.assumptions):
        L.append("")

    L += [f"## {t('h_verify')}", ""]
    if res.verify_next:
        L += [f"- {t('verify_line', aid=v.assumption, text=_c(v.text), risk=v.max_risk, check=_c(v.check) or '—')}"
              for v in res.verify_next]
    else:
        L.append(f"- {t('verify_none')}")
    L.append("")

    L += [f"## {t('h_attacks')}", ""]
    if res.attacks:
        L += [f"| {t('col_rank')} | {t('col_id')} | {t('col_class')} | {t('col_assumption')} | {t('col_impact')} | "
              f"{t('col_plaus')} | {t('col_risk')} | {t('col_sev')} |", "|--:|---|---|---|--:|--:|--:|---|"]
        for a in res.attacks:
            L.append(f"| {a.rank} | {a.id} | {_cls(a.class_id)} | {a.assumption} | {a.impact} | {_plaus(a)} | {a.risk} | {a.severity} |")
        L.append("")
        for a in res.attacks:
            if a.plausibility != a.effective_plausibility:
                L.append(f"- **{a.id}**: " + t("plaus_note", p=a.plausibility, e=a.effective_plausibility,
                                               status=t("status_" + a.assumption_status)))
        L.append("")
    else:
        L += [f"- {t('s_none_severity')}", ""]

    L += [f"## {t('h_coverage')}", ""]
    for c in res.coverage:
        if c.attack_ids:
            state = t("cov_attacks", n=len(c.attack_ids), ids=", ".join(c.attack_ids))
        elif c.skipped_reason:
            state = t("cov_skipped", reason=_c(c.skipped_reason))
        else:
            state = f"**{t('cov_uncovered')}**"
        L.append(f"- {_cls(c.class_id)}: {state}")
    L.append("")

    if res.rejections:
        L += [f"## {t('h_rejected')}", "", f"| {t('col_kind')} | {t('col_id')} | {t('col_reason')} |", "|---|---|---|"]
        L += [f"| {t('kind_' + r.kind)} | {r.id} | {_c(r.detail)} |" for r in res.rejections]
        L.append("")

    if res.warnings:
        L += [f"## {t('h_warnings')}", ""] + [f"- {w}" for w in res.warnings] + [""]
    L += ["---", t("footer"), ""]
    return "\n".join(L)
