# ACH — Analysis of Competing Hypotheses — methodology card

## Origin
Created by Richards J. Heuer Jr. at the CIA to counter confirmation bias in intelligence analysis. Documented in *Psychology of Intelligence Analysis* (CIA Center for the Study of Intelligence, 1999), a collection of articles Heuer wrote between 1978 and 1986. The technique also appears in the UFMCS *Red Team Handbook* as a structured analytic technique.

## Sources
- Heuer, *Psychology of Intelligence Analysis*, CIA/CSI, 1999 — https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/ — `read` (landing page: author, year, 214-page PDF). The text itself was read in a copy hosted by IALEIA, https://www.ialeia.org/docs/Psychology_of_Intelligence_Analysis.pdf (not the CIA site): **Chapter 8 is "Analysis of Competing Hypotheses", p. 95**, and Heuer's preface calls it "arguably the most important single chapter".
- UFMCS *Red Team Handbook* v5 (15 Apr 2011): Key Assumptions Check p. 151, ACH p. 158 — `read` (table of contents).
- Heuer & Pherson, *Structured Analytic Techniques for Intelligence Analysis* — `exists`.

## Problem it solves
People pick the first plausible explanation and then collect evidence that fits it. ACH forces you to list rival explanations, test *all* evidence against *all* of them, and focus on what each hypothesis cannot explain.

## When to use / when NOT to use
- Use: a flaky test, an intermittent production error, or an incident with ≥ 3 plausible causes and conflicting signals.
- Do not use: the cause is already reproduced; the question is a choice between options (use a decision matrix) rather than an explanation.

## How it maps to software work
Hypotheses are candidate root causes; evidence is what you observed by running commands. Clarent adds (our adaptation, not Heuer's): a mandatory `ref` for observed evidence, a catch-all hypothesis that can never lead, and a ranking of *proposed* tests by how well they separate the hypotheses still alive.

## Inputs and outputs
- Input: `.clarent/ach/<slug>.json`, schema in `clarent_ach/model.py` (hypotheses, evidence with ratings `CC|C|N|I|II`, credibility, relevance, cost).
- Output: Markdown or JSON report with ranking, matrix, diagnosticity, sensitivity, next test, warnings.
- Example (3 lines): `clarent ach init .clarent/ach/flaky.json` → fill hypotheses and cited evidence → `clarent ach score .clarent/ach/flaky.json` prints the report and the test to run next.

## Algorithm (what is deterministic)
- Score of a hypothesis = Σ over observed evidence of `weight × penalty`, with penalty `I = 1`, `II = 2`, everything else `0`; `weight = credibility × relevance` (1–9). Consistent evidence never adds to the score.
- Evidence kinds: *diagnostic* (penalties differ across hypotheses), *supports-only* (only C vs CC differ), *non-diagnostic* (identical ratings).
- Sensitivity: remove each evidence item and recompute; flag the conclusion as fragile if the leader set changes.
- Next test: among non-refuted, non-catch-all hypotheses, `priority = spread × weight / cost`, where `spread = max(rating) − min(rating)`.

## Limitations
- The numeric constants (penalties, weights, refutation threshold of 6) are Clarent's, not Heuer's.
- Garbage in, garbage out: ratings are judgments. The `ref` requirement reduces, but does not remove, invented evidence.
- The output is a ranking, not a probability. Heuer's method is not a Bayesian update.
- Needs a reasonably complete hypothesis set; the catch-all warning is a reminder, not a guarantee.

## Prior art (GitHub scan)
Scanned 2026-11-24. `Burton/Analysis-of-Competing-Hypotheses` (112 stars, PHP, last push 2012); `suprathermal/ACH-Grounding` (2); `lightcaptainguy/bayesian-ach-reasoning-prototype` (2); prompt-only ACH in `product-on-purpose/thinking-framework-skills`. Adjacent: `doraemonkeys/claude-code-debug-mode` (hypothesis-driven debugging with runtime logs). No deterministic engine with diagnosticity, sensitivity and next-test selection was found. See `research/novelty.md`.

## Worked example
`examples/flaky-test.json` (**synthetic**, English) and `examples/flaky-test.es.json` (Spanish).
`python -m clarent_ach score examples/flaky-test.json` → leaders H1 and H5 (tie), H2/H3/H4 refuted, T1 recommended first because it separates the two leaders.

## Evaluation
Not yet measured. Planned: 10 real, closed flaky-test/incident cases with known root cause; compare time-to-correct-hypothesis and number of wrong fixes, with and without the skill, and publish the result even if null.
