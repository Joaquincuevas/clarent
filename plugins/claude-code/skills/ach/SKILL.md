---
name: ach
description: Diagnose a bug, flaky test or incident with competing hypotheses (Heuer's ACH). Use when several causes are plausible and you risk anchoring on the first one. Outputs a scored matrix and the most discriminating next test.
disable-model-invocation: true
argument-hint: [problem description]
---

# ACH — Analysis of Competing Hypotheses

You are running a disciplined diagnosis. The goal is **to refute hypotheses, not to confirm them**. A bundled script does the scoring; your job is to supply honest, *cited* evidence and honest ratings.

Problem: $ARGUMENTS

## Tooling

The engine is stdlib-only Python. Run it with whichever of `python3` / `python` exists:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" init  .clarent/ach/<slug>.json
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" score .clarent/ach/<slug>.json
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" next  .clarent/ach/<slug>.json
```

Add `--lang es` before the subcommand for Spanish output. Use `--strict` once you believe the file is final.

## Procedure

1. **Frame.** `init` a file. Write the `question` as one sentence a stranger could answer.
2. **Key assumptions.** List what you are currently assuming (e.g. "the test fails in the code under test, not in the harness"). Any assumption you cannot back with an observation becomes a hypothesis.
3. **Hypotheses.** Write at least 4 distinct, falsifiable causes, plus one `"catch_all": true` ("something else"). Each must predict something *observable*. Do **not** rate anything yet.
4. **Gather evidence by running commands** (tests, logs, `git log`, bisect, profiling). Every observation becomes an `observed` evidence item with:
   - `text`: what was observed, stated neutrally;
   - `ref`: the exact command, `file:line`, or log excerpt that produced it;
   - `credibility` and `relevance`: `low | medium | high`.
   If you only *believe* something, it is **not evidence**: either observe it or leave it out. Never invent a `ref`.
5. **Rate row by row.** For each evidence item, rate it against **all** hypotheses before moving to the next item (never hypothesis by hypothesis — that anchors you). Ask: *"If this hypothesis were true, how surprised would I be to see this?"*

   | Rating | Meaning |
   |--------|---------|
   | `CC` / `C` | very consistent / consistent |
   | `N` | neutral or not applicable |
   | `I` / `II` | inconsistent / very inconsistent |

   Only inconsistency counts in the score. Consistent evidence rarely discriminates.
6. **Score.** Run `score`. Read the **warnings first**: uncited evidence, fragile conclusions, and an un-refuted catch-all all matter.
7. **Test the leaders.** Run `next`. Execute the top recommended test, then change its `status` to `observed`, add a `ref`, set its ratings to what actually happened, and re-score. Repeat.
8. **Stop** when one hypothesis leads, the conclusion is not fragile, and its predictions have survived a test — or after 3 rounds without progress, in which case say the diagnosis is **unresolved** and ask the user.

## Reporting

Paste the Markdown report. State the leader as a **working hypothesis**, never as a proven cause or a probability. Mention the catch-all warning if it appears.

## Rules

- Do not adjust ratings to reach a preferred answer. Do not delete evidence that contradicts the leader.
- Mark evidence `observed` only if you ran something this session and can cite it.
- The score is a ranking of inconsistencies, **not a probability**.
- If a fix is requested, apply it only after step 8, then re-run the failing check as new evidence.
