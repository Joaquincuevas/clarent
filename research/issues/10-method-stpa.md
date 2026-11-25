---
title: "method: stpa — STAMP/STPA control-structure analysis for agents and microservices (Leveson, MIT)"
labels: [new-method, help wanted, v2, difficulty:hard]
difficulty: hard
effort: "2 weeks"
---

## What it solves
Reviews a system for unsafe interactions, not only component failures: an agent that can take actions, a deploy orchestrator, an autoscaler.
It forces completeness: every control action is examined in every unsafe-action category, and everything traces back to a hazard and a loss.

## Example (expected behavior)
Input:
```
/clarent-methods:stpa deploy-controller.json
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
36 UCA cells, 31 analysed, 5 pending (exit 1); UCA-7: ordering a rollback *too late* if error-rate feedback arrives 5 minutes late
```

## References
- Spec: [`product-spec.md` — `stpa` — Análisis de estructura de control (agentes y microservicios)](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#stpa--análisis-de-estructura-de-control-agentes-y-microservicios) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — E04 · STAMP / STPA](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#e04--stamp--stpa). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - Leveson & Thomas, *STPA Handbook* (2018) — http://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf — **exists (the four steps were checked by search; not read in full)**
  - Leveson, *Engineering a Safer World* (MIT Press, 2011) — **exists (Open Library record; not opened)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/4/3/3/3 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/stpa/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_stpa/                # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_stpa.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/stpa/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `stpa` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Tests: an orphan UCA, a control loop without feedback and an unanalysed cell are each detected.
- [ ] Traceability: every UCA links to ≥ 1 hazard and every hazard to ≥ 1 loss.
- [ ] The UCA coverage table is generated (action × not provided / provided / wrong timing or order / wrong duration for continuous actions × context) and every cell ends `unsafe`, `safe` or `n/a`.
- [ ] Valid Mermaid output; a `--lite` mode with only steps 2–3.

Note from the spec: It is the heaviest method and the one with the most novelty at stake: a guided template and a canonical example reduce the risk of bureaucracy. The STPA Handbook (2018) is marked `exists` in the catalog: say what you read.

## Difficulty and time
- **Difficulty: hard.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=3.
- **Estimated effort: 2 weeks** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#stpa--análisis-de-estructura-de-control-agentes-y-microservicios); the author's estimate, never measured).
- **Milestone:** `v2` — moved out of the top 10 to v2 by the author's decision on 2026-11-25; start with `--lite`.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
