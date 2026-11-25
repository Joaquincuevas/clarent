---
title: "method: intent — Commander's Intent delegation contract (US Army, ADP 6-0)"
labels: [new-method, help wanted, v1, difficulty:medium]
difficulty: medium
effort: "1–1.5 weeks"
---

## What it solves
Lets you delegate to a subagent (or a person) with the purpose, the end state and the limits instead of a script of steps, and then checks that the result stayed inside them.
It catches "intent drift": a subagent that changes files it was told not to touch.

## Example (expected behavior)
Input:
```
/clarent-methods:intent "migrate the HTTP client to httpx"
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
writes `intent.md` with `forbidden_paths: [infra/**]`; when the subagent finishes, `clarent intent verify` finds a change under `infra/terraform/…` and returns exit 2 so the hook sends it back to fix it
```

## References
- Spec: [`product-spec.md` — 4. `intent` — Contrato de delegación (Commander's Intent / Mission Command)](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#4-intent--contrato-de-delegación-commanders-intent--mission-command) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — M07 · Commander's Intent](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#m07--commanders-intent). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - ADP 6-0 *Mission Command* (17 May 2012) — https://adamdrake.com/static/ADP-6-0-Mission-Command.pdf — **read (its definition names *purpose* and *end state*;  is Clarent's addition)**
  - ADP 6-0 (2019 ed.) and Herrera, *History, Mission Command, and the Auftragstaktik Infatuation*, Military Review 2022, for M02 Mission Command — **exists (the origin of Auftragstaktik is disputed; Clarent claims none)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/5/4/4/3 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/intent/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_intent/              # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_intent.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/intent/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `intent` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] `lint` tests with valid and invalid files (required fields, an observable end state, no micromanagement signal, non-empty `stop_conditions`).
- [ ] `verify` test with a temporary git repository and a diff outside `allowed_paths`.
- [ ] Minimal template of 4 required fields; everything else optional.
- [ ] The `SubagentStop` hook (exit 2 keeps the subagent working) is tried with a **real** subagent before the card claims anything about it (the roadmap lists this as the main risk).

Note from the spec: ADP 6-0 defines intent as *purpose* and *end state*; `key_tasks` and the path constraints are Clarent's additions and must be labelled as such.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1–1.5 weeks** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#4-intent--contrato-de-delegación-commanders-intent--mission-command); the author's estimate, never measured).
- **Milestone:** `v1` — roadmap week 3 of v1; it is the first thing cut if v1 slips (then it moves to v1.1).

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
