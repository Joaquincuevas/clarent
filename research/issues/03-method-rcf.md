---
title: "method: rcf — Reference Class Forecasting from your own git history (Kahneman & Tversky; Flyvbjerg)"
labels: [new-method, help wanted, v1, difficulty:medium]
difficulty: medium
effort: "1 week"
---

## What it solves
Answers "how long will this take?" with the distribution of similar past work in this repository (the outside view) instead of a gut feeling, and records the forecast so it can be scored later.
It refuses to forecast when the reference class is too small.

## Example (expected behavior)
Input:
```
/clarent-methods:rcf "add pagination to /orders"
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
Class: 23 similar PRs. P50 2.9 d, P80 6.1 d, P90 11 d. Your internal estimate (1 d) falls below the P10 of the class.
```

## References
- Spec: [`product-spec.md` — 5. `rcf` — Estimar con tu propio historial (Reference Class Forecasting)](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#5-rcf--estimar-con-tu-propio-historial-reference-class-forecasting) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — row X06 of the table in "Familia 6 — Adicionales poco conocidas (19)"](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#familia-6--adicionales-poco-conocidas-19). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - Kahneman & Tversky, *Intuitive prediction: biases and corrective procedures*, TIMS Studies in Management Science 12 (1979) — **exists (consistent secondary citations; no Crossref record)**
  - Flyvbjerg, *From Nobel Prize to Project Management: Getting Risks Right*, Project Management Journal (2006), doi:10.1177/875697280603700302 — **exists (Crossref)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/4/4/5/3 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/rcf/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_rcf/                 # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_rcf.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/rcf/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `rcf` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Test with a seeded synthetic git history.
- [ ] Refuses (exit 1) when the class has fewer than 10 items.
- [ ] Reproducible: same history and seed give the same quantiles and bootstrap interval.
- [ ] Squash/rebase distortion, bots and "PR time ≠ effort" are documented, and authors/labels can be excluded.

Note from the spec: The catalog's Flyvbjerg citation was corrected once already (the first DOI pointed at another article): re-check any citation you add.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1 week** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#5-rcf--estimar-con-tu-propio-historial-reference-class-forecasting); the author's estimate, never measured).
- **Milestone:** `v1` — roadmap v1.1 (weeks 6–9), after the v1 launch set.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
