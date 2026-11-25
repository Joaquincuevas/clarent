---
title: "method: gate — Proposal gate from the Heilmeier Catechism (DARPA)"
labels: [new-method, help wanted, v2, difficulty:easy, good first issue]
difficulty: easy
effort: "3–4 days"
---

## What it solves
Stops a PR or RFC from moving forward until it answers DARPA's eight questions (what, how it is done today, what is new, who cares, risks, cost, duration, how success is checked).
The checks are simple, explainable heuristics, not an LLM opinion.

## Example (expected behavior)
Input:
```
clarent gate check proposals/migrate-to-kafka.md
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
Q7: no duration found; Q8: no measurable criterion — pending (label `needs-gate`)
```

## References
- Spec: [`product-spec.md` — 7. `gate` — Puerta de propuesta (Catecismo de Heilmeier)](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#7-gate--puerta-de-propuesta-catecismo-de-heilmeier) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — row X04 of the table in "Familia 6 — Adicionales poco conocidas (19)"](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#familia-6--adicionales-poco-conocidas-19). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - DARPA, *The Heilmeier Catechism* — https://www.darpa.mil/about/heilmeier-catechism — **exists (the eight questions in the spec are from this page; read it and upgrade the level if you do)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 3/4/5/3/4 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/gate/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_gate/                # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_gate.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/gate/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `gate` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] A test for each heuristic with cases that pass and cases that fail: Q1 jargon density, Q6/Q7 need figures with units, Q8 needs a checkable criterion (command, metric or threshold).
- [ ] Every verdict shows its reason; a `<!-- gate: ignore Q6 reason -->` comment suppresses one question with a recorded reason.
- [ ] Output is approved / pending per question.

Note from the spec: The eight questions are quoted from DARPA's page (marked `exists` in the catalog, not `read`): read the page and say so in the card.

## Difficulty and time
- **Difficulty: easy.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=5.
- **Estimated effort: 3–4 days** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#7-gate--puerta-de-propuesta-catecismo-de-heilmeier); the author's estimate, never measured).
- **Milestone:** `v2` — roadmap v2, block "Gobernanza de propuestas".

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
