"""Markdown rendering of ACH results (meant to be pasted into a PR, issue or postmortem)."""
from __future__ import annotations

from .engine import Result
from .i18n import t
from .model import Analysis


def markdown(an: Analysis, res: Result) -> str:
    L: list[str] = [f"# {t('h_title', title=an.title)}", ""]
    if an.question:
        L += [t("question", q=an.question), ""]

    L += [f"## {t('h_conclusion')}", "", f"- {t('v_' + res.verdict)}"]
    if res.verdict != "no-discrimination":
        margin = t("margin", m=res.margin) if res.margin is not None else ""
        L.append("- " + t("leaders", ids=", ".join(res.leaders)) + margin)
    if res.fragile:
        L.append(f"- {t('fragile_flag')}")
    L += [f"- {t('not_probability')}", ""]

    L += [f"## {t('h_ranking')}", "",
          f"| # | {t('col_hyp')} | {t('col_incons')} | {t('col_state')} | {t('col_contra')} |",
          "|---|-----------|---------------:|--------|-----------------|"]
    for s in res.scores:
        state = t("st_catch_all") if s.catch_all else (t("st_refuted") if s.refuted else t("st_alive"))
        L.append(f"| {s.rank} | **{s.id}** {s.text} | {s.inconsistency} | {state} | "
                 f"{', '.join(s.contradicted_by) or '—'} |")
    L.append("")

    hyp_ids = [h.id for h in an.hypotheses]
    L += [f"## {t('h_matrix')}", "",
          f"| {t('col_evidence')} | {t('col_weight')} | " + " | ".join(hyp_ids) + " |",
          "|-----------|-----:|" + "|".join(":-:" for _ in hyp_ids) + "|"]
    for e in an.observed:
        row = " | ".join(e.ratings.get(h, "N") for h in hyp_ids)
        ref = f" _({e.ref})_" if e.ref else f" _{t('no_ref')}_"
        L.append(f"| **{e.id}** {e.text}{ref} | {e.weight} | {row} |")
    L.append("")

    L += [f"## {t('h_diag')}", "",
          f"| {t('col_evidence')} | {t('col_type')} | {t('col_spread')} | {t('col_spread_w')} |", "|---|---|--:|--:|"]
    for d in res.diagnostics:
        L.append(f"| {d.id} | {t('kind_' + d.kind)} | {d.spread} | {d.weighted} |")
    non = [d.id for d in res.diagnostics if d.kind != "diagnostic"]
    if non:
        L += ["", t("non_diag", ids=", ".join(non))]
    L.append("")

    L += [f"## {t('h_sens')}", ""]
    crit = [s for s in res.sensitivity if s.changes_leader]
    if crit:
        for s in crit:
            L.append("- " + t("sens_item", eid=s.evidence_id, ids=", ".join(s.leaders_without)))
    else:
        L.append(f"- {t('sens_none')}")
    L.append("")

    L += [f"## {t('h_next')}", ""]
    if res.next_tests:
        L += [f"| {t('col_test')} | {t('col_priority')} | {t('col_for')} | {t('col_against')} |", "|---|--:|---|---|"]
        for x in res.next_tests:
            L.append(f"| **{x.id}** {x.text} | {x.priority} | {', '.join(x.separates) or '—'} | "
                     f"{', '.join(x.against) or '—'} |")
    else:
        L.append(f"- {t('no_next')}")
    L.append("")

    if res.warnings:
        L += [f"## {t('h_warnings')}", ""] + [f"- {w}" for w in res.warnings] + [""]
    L += ["---", t("footer"), ""]
    return "\n".join(L)
