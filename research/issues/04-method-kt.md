---
title: "method: kt — IS / IS-NOT differential over CI runs (Kepner-Tregoe, 1965)"
labels: [new-method, help wanted, v2, difficulty:medium]
difficulty: medium
effort: "1 week"
---

## What it solves
Turns "it fails sometimes" into a specification: where and when it fails, where and when it does not, and what distinguishes the two (OS, shard, runner image, hour…).
It can seed an `ach` analysis with the distinctions it finds.

## Example (expected behavior)
Input:
```
clarent kt analyze runs.csv --outcome failed
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
Fails 14/15 on `shard=3 ∧ runner_image=2026-11-02`; 0/200 elsewhere. Distinction: new runner image (change: 2026-11-02).
```

## References
- Spec: [`product-spec.md` — 6. `kt` — IS / IS-NOT diferencial sobre corridas de CI](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#6-kt--is--is-not-diferencial-sobre-corridas-de-ci) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — E06 · Kepner-Tregoe (Problem Analysis)](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#e06--kepner-tregoe-problem-analysis). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - Official Kepner-Tregoe excerpt, *The New Rational Manager* ch. 1–2 (Problem Analysis) — https://kepner-tregoe.com/wp-content/uploads/2025/08/The-New-Rational-Manager-Chapters-1-2-PA.pdf — **exists (the IS / IS-NOT mechanics were checked by search, the PDF was not read in full)**
  - Kepner & Tregoe, *The Rational Manager* (McGraw-Hill, 1965) — **exists**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 3/5/4/4/3 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/kt/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_kt/                  # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_kt.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/kt/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `kt` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Synthetic data with a known cause plus noise dimensions (fixed seed): the tool recovers the right dimension and reports **no** distinctions on pure noise.
- [ ] Fisher's exact test implemented with `math.comb`; multiple-comparison correction (Holm); refuses to flag values with n below a minimum.
- [ ] Output in IS / IS-NOT columns (what, where, when, magnitude), a distinctions list (IS side only) and the checklist "a candidate cause must explain the whole specification".
- [ ] `clarent kt to-ach` seeds hypotheses and evidence for `ach`.

Note from the spec: Findings are *distinctions*, not causes: confounders and collinearity are warned about in the report.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1 week** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#6-kt--is--is-not-diferencial-sobre-corridas-de-ci); the author's estimate, never measured).
- **Milestone:** `v2` — roadmap v2, block "Ingeniería".

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
