---
title: "method: spc — Statistical Process Control on CI and delivery metrics (Shewhart, 1931)"
labels: [new-method, help wanted, v1, difficulty:medium]
difficulty: medium
effort: "1 week"
---

## What it solves
Tells you whether a change in CI duration, flaky-test rate or lead time is a real signal or noise, using control charts instead of eyeballing a graph.
It alerts only on special causes (Western Electric style rules), so a bad day does not look like a regression.

## Example (expected behavior)
Input:
```
clarent spc chart --from-gh-runs ci.yml --metric duration
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
signal (rule: run of 8 above the mean) since run #3412: +3m10s over the baseline; candidate commits: a1b2c3..d4e5f6
(plus an SVG control chart, generated with no dependencies)
```

## References
- Spec: [`product-spec.md` — 3. `spc` — Cartas de control para CI y métricas de entrega](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#3-spc--cartas-de-control-para-ci-y-métricas-de-entrega) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — L12 · SPC (Control Estadístico de Procesos)](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#l12--spc-control-estadístico-de-procesos). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - Shewhart, *Economic Control of Quality of Manufactured Product* (1931) — **exists (Open Library record; not opened)**
  - NIST/SEMATECH e-Handbook, ch. 6 *Process or Product Monitoring and Control* — https://www.itl.nist.gov/div898/handbook/pmc/pmc.htm — **exists**
  - Western Electric, *Statistical Quality Control Handbook* (1956), for the run rules — **exists (several secondary sources; the manual was not opened, and they disagree on one rule)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/4/4/5/4 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/spc/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_spc/                 # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_spc.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/spc/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `spc` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Tests with synthetic series that have a known shift: the shift is detected within ≤ 3 points, and **pure noise does not alert** (false-alarm rate measured on 1,000 simulated series with a fixed seed, and documented in the card).
- [ ] XmR chart limits use the standard constant 2.66; the run-length rule is **configurable** (default 8) because sources disagree (one gives 9, some swap rules 2 and 3), and the report names the rule by its definition, not its number.
- [ ] Autocorrelated or non-normal series produce a warning and the option of a larger window.

Note from the spec: Western Electric definitions come from secondary sources (the 1956 manual was not opened): verify them against a source before publishing and say what you read.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1 week** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#3-spc--cartas-de-control-para-ci-y-métricas-de-entrega); the author's estimate, never measured).
- **Milestone:** `v1` — roadmap week 2 of v1; `spc` is part of the minimum launch set.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
