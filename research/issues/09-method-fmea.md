---
title: "method: fmea — Failure Mode and Effects Analysis for a software module (US Army MIL-P-1629, 1949)"
labels: [new-method, help wanted, v2, difficulty:medium]
difficulty: medium
effort: "1.5 weeks"
---

## What it solves
Produces a prioritized list of failure modes for a module with severity, occurrence and detection tied to repository data (fix commits from git, line coverage) instead of guesses.
A failure mode without a `file:line` reference is rejected.

## Example (expected behavior)
Input:
```
/clarent-methods:fmea src/payments/
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
14 failure modes; the 3 high-priority ones are gateway calls with no timeout and low coverage, each linked to lines
```

## References
- Spec: [`product-spec.md` — `fmea` — FMEA de un módulo de software](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#fmea--fmea-de-un-módulo-de-software) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — E01 · FMEA / FMECA](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#e01--fmea--fmeca). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - MIL-P-1629 (1949) / MIL-STD-1629A (1980), NASA FMECA for Apollo (1966) — **exists (several secondary sources)**
  - AIAG & VDA, *FMEA Handbook* (1st ed., 2019), which replaced RPN with Action Priority — **exists (secondary sources agree; paid, not opened)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 3/4/4/3/4 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/fmea/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_fmea/                # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_fmea.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/fmea/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `fmea` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Fixture module: occurrence and detection are computed from real data (a temporary git repository and a minimal `coverage.xml`).
- [ ] A failure mode without a `ref` is rejected.
- [ ] Python only in v1 (via `ast`); TypeScript is a later issue.
- [ ] Priority uses Clarent's own rules, **not a copy of the AIAG-VDA tables**: maximum severity is always high, otherwise S×O×D with a documented cut, with a warning about the known limits of RPN.

Note from the spec: Line coverage is not real detection capability: the report must say so. The AIAG-VDA handbook is paid and was not opened (`exists` via secondary sources).

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1.5 weeks** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#fmea--fmea-de-un-módulo-de-software); the author's estimate, never measured).
- **Milestone:** `v2` — moved out of the top 10 to v2 by the author's decision on 2026-11-25.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
