---
title: "method: fta — Fault Tree Analysis with minimal cut sets (H. A. Watson, Bell Labs, 1961–62)"
labels: [new-method, help wanted, v2, difficulty:hard]
difficulty: hard
effort: "1 week"
---

## What it solves
Turns an incident timeline into the minimal combinations of failures that cause the top event, and lists the single points of failure.
Every basic event must cite evidence (a log, a metric, a commit), so the tree cannot be invented.

## Example (expected behavior)
Input:
```
/clarent-methods:fta INC-2210
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
top event: checkout 500; 3 minimal cut sets; SPOF: `config-server timeout` (no cache)
```

## References
- Spec: [`product-spec.md` — 8. `fta` — Árbol de fallas desde incidentes, con conjuntos mínimos de corte](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#8-fta--árbol-de-fallas-desde-incidentes-con-conjuntos-mínimos-de-corte) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — E02 · Análisis de Árbol de Fallas (FTA)](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#e02--análisis-de-árbol-de-fallas-fta). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - NASA, *Fault Tree Handbook with Aerospace Applications*, v1.1 (Aug 2002) — **exists (the catalog notes the handbook confirms the early-1960s aerospace origin and uses the Minuteman analysis as an example; it does not name Watson)**
  - H. A. Watson, Bell Labs, 1961–62 (USAF Minuteman launch control), as the origin — **exists (several secondary sources)**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/4/3/4/3 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/fta/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_fta/                 # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_fta.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/fta/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `fta` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Textbook trees with known cut sets give exactly those cut sets.
- [ ] Property test: no cut set is a subset of another.
- [ ] `validate` rejects cycles, wrong gate arity and hidden undeveloped events; every basic event needs a `ref`.
- [ ] Cut sets by top-down expansion with absorption (MOCUS-style); with probabilities, an upper bound and an importance measure; Mermaid rendering.

Note from the spec: The tree is built by an LLM in practice: the `ref` requirement is the defence against invented causes. The NASA Fault Tree Handbook v1.1 is marked `exists` in the catalog: say which parts you read.

## Difficulty and time
- **Difficulty: hard.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=3.
- **Estimated effort: 1 week** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#8-fta--árbol-de-fallas-desde-incidentes-con-conjuntos-mínimos-de-corte); the author's estimate, never measured).
- **Milestone:** `v2` — roadmap v2, block "Ingeniería"; it is the riskiest of the top 10 to implement.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
