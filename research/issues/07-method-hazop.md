---
title: "method: hazop — Guide words on APIs and data flows (HAZOP, ICI, 1960s)"
labels: [new-method, help wanted, v2, difficulty:medium]
difficulty: medium
effort: "1 week"
---

## What it solves
Reviews an API or data flow for deviations by applying every guide word (no, more, less, reverse, other than, early, late…) to every parameter of every node, and refuses to leave any cell unexamined.
It complements `redteam`: a checkable exhaustive grid instead of a free-form attack.

## Example (expected behavior)
Input:
```
/clarent-methods:hazop openapi/orders.json   (hypothetical)
```
Output (expected; illustrative, taken from the spec, nothing is implemented yet):
```
4 nodes, 9 parameters, 90 cells; 83 resolved, 7 `unanalyzed` (exit 1). One deviation: `POST /orders` · `idempotency-key` · `no` → a client retry creates a duplicate order (S2), no safeguard in `src/orders/create.py` → open action.
```

## References
- Spec: [`product-spec.md` — 9. `hazop` — Palabras guía sobre APIs y flujos de datos](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#9-hazop--palabras-guía-sobre-apis-y-flujos-de-datos) — the algorithm, input format, motor and risks are written there.
- Sources: [`catalog.md` — row X10 of the table in "Familia 6 — Adicionales poco conocidas (19)"](https://github.com/Joaquincuevas/clarent/blob/main/research/catalog.md#familia-6--adicionales-poco-conocidas-19). As recorded there (marks: read = opened and read; exists = a record or document confirmed, content not read; unverified = no primary source found):
  - ICI (UK), 1960s; Lawley, *Chemical Engineering Progress* (1974); Kletz, *Hazop and Hazan* (1983) — **exists (sources disagree on how much is due to Kletz)**
  - IEC 61882 (the standard for HAZOP studies): the guide-word list in the spec is **not** checked against it — **unverified**
- Priority and plan: [`ranking.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/ranking.md), [`roadmap.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/roadmap.md) (score 4/3/4/3/4 for N/U/E/V/C in [`scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv)).
- Reference implementation: [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) (and `triz-matrix`, `redteam`).

## Files to create
```
methods/hazop/
├── method.toml                  # manifest: id, version, family, status, [[sources]] with honest levels, [novelty]
├── CARD.md                      # methodology card (copy templates/methodology-card.md; `doctor` checks the sections)
├── clarent_hazop/               # importable stdlib-only package: __init__, __main__, cli, model, engine, render, i18n
├── skill/SKILL.md               # Claude Code skill (description ≤ 300 characters, `disable-model-invocation: true`)
├── tests/test_hazop.py           # unittest, run from any directory
└── examples/                    # runnable example(s), English and Spanish, clearly labelled SYNTHETIC if synthetic
```
Also: run `python tools/build_plugin.py` and commit `plugins/claude-code/skills/hazop/` (never edit it by hand), update the
method table in `README.md`, and add the real output of one command to `tools/gen_demo.py` so `docs/demo/` carries it.

## Acceptance criteria
- [ ] `python tools/test_all.py` passes (your tests run there automatically).
- [ ] `PYTHONPATH=src python -m clarent doctor` passes for `hazop` (manifest, card sections, skill, sources, examples).
- [ ] `python tools/build_plugin.py --check` passes (plugin regenerated and committed).
- [ ] `claude plugin validate ./plugins/claude-code` passes.
- [ ] `python tools/gen_demo.py --check` passes (demo output is real, not typed by hand).
- [ ] Every source in `method.toml` and `CARD.md` is marked honestly: `read` only for what you opened and read (say which pages), `exists` for a record you confirmed, `blocked`, or `unverified`. No invented sources or quotes.
- [ ] Constants that are not from the original source (weights, thresholds, bands) are listed under **Limitations** in the card.
- [ ] Prior art re-scanned with **short** (1–2 word) GitHub queries and recorded in the card (`python tools/github_scan3.py`; long queries gave false zeros before).
- [ ] No runtime dependency outside the Python ≥ 3.11 standard library; no claim that the method improves agent performance without a published eval.
- [ ] Small OpenAPI fixture with an expected full grid (exact cell count).
- [ ] A cell left unresolved → exit 1; a `safeguard.ref` that does not exist → rejected; `n/a` without a reason → rejected; duplicate ids, orphan nodes and unknown guide words → rejected.
- [ ] A guide word added as a file shows up in the grid; cell order is reproducible.
- [ ] `scaffold` reads an OpenAPI **JSON** (YAML is outside the standard library) and never invents causes or consequences.

Note from the spec: The guide-word list and its applicability to software are Clarent's adaptation and are **not checked against IEC 61882** (`unverified`): verify before publishing the card.

## Difficulty and time
- **Difficulty: medium.** Derived from the ease score `E` the author recorded in [`research/data/scores.csv`](https://github.com/Joaquincuevas/clarent/blob/main/research/data/scores.csv) (E=5 → easy, E=4 → medium, E≤3 → hard). That mapping is mine; the spec gives effort, not difficulty. Here E=4.
- **Estimated effort: 1 week** for one person ([`product-spec.md`](https://github.com/Joaquincuevas/clarent/blob/main/research/product-spec.md#9-hazop--palabras-guía-sobre-apis-y-flujos-de-datos); the author's estimate, never measured).
- **Milestone:** `v2` — roadmap v2, block "Ingeniería"; it enters the top 10 on a tie-break, so it is the most fragile slot.

## Before you start
- Comment here to claim the issue. One method per pull request.
- Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md) and use [`methods/ach/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach) as the reference layout; [`methods/triz-matrix/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/triz-matrix) and [`methods/redteam/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam) are two more worked examples.
- Sign off commits (`git commit -s`, DCO).
- The spec is the author's design, not scripture: if you find a better algorithm, say so in the PR and update the spec section in the same PR.
