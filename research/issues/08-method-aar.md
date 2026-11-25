---
title: "method: aar — After Action Review from git, CI and incidents (US Army, TC 25-20)"
labels: [new-method, help wanted, v2, difficulty:medium]
difficulty: medium
effort: "1–1.5 weeks"
---

## What it solves
Compares what was planned with what happened for a release, migration or incident, using `git log`, CI results and an incident JSON, and records why they differ and what to sustain or improve.
It checks that every miss has a cause or an explicit "unknown", and every action has an owner, a date and a way to verify it.

## Example (expected behavior)
Input:
```
clarent aar collect --since v2.3.0 --until v2.4.0 --ci ci-runs.json --incident INC-2210.json   (hypothetical)
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
Expected: zero-downtime deploy, p95 < 300 ms. Happened: 14 commits, 2 failed CI runs, p95 410 ms (missed, +110 ms), 38 min to detect. Proposed cause: timeout with no cache (evidence: `src/search.py:88`). Actions: sustain the flag rollback; improve the p95 alert (owner, due date, verification).
```

## References
- Spec: [`product-spec.md` — 10. `aar` — After Action Review desde git, CI e incidentes](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#10-aar--after-action-review-desde-git-ci-e-incidentes) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — M04 · After Action Review (AAR)](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#m04--after-action-review-aar). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - US Army, TC 25-20 *A Leader's Guide to After-Action Reviews* (30 Sept 1993) — http://www.victoryprinciples.com/wp-content/uploads/2009/07/tc-25-20-ldrs-guide-aars.pdf — **read (AAR format; the 'what was supposed to happen', 'what happened', key issues and sustain/improve sections)**
  - Morrison & Meliza, *Foundations of the After Action Review Process*, ARI Special Report 42 (1999) — **exists (via an APA article; not opened)**
  - Google SRE book, *Postmortem Culture* — https://sre.google/sre-book/postmortem-culture/ — **exists**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 3/4/4/3/4 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/aar/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_aar/                 # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_aar.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/aar/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `aar` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Temporary git repository plus fixed CI and incident JSON: timeline order and interval calculation are exact.
- [ ] Metric verdicts (`met`, `missed`, `exceeded`); an expectation with no metric → `unassessed` with a warning.
- [ ] A `missed` difference with no cause → exit 1; a cited SHA that does not exist → rejected; a cause that names a commit author → warning (blameless heuristic); an action without `verification` → rejected; no `sustain` action → warning.
- [ ] `followup --on <date>` lists overdue actions.

Note from the spec: TC 25-20 is `read` for the sections listed in the spec; the Morrison & Meliza ARI report is only known to exist. A tool does not create a blameless culture: say so in the card's Limitations.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1–1.5 weeks** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#10-aar--after-action-review-desde-git-ci-e-incidentes); the author's estimate, never measured).
- **Milestone:** `v2` — roadmap v2, block "Aprendizaje tras el evento"; slot 10 by the author's decision on a tie.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
