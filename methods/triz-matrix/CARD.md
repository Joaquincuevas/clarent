# TRIZ Contradiction Matrix — methodology card

## Origin
TRIZ was developed in the USSR by Genrikh Altshuller and Rafael Shapiro from 1946 onward, by studying patents to find recurring ways inventors resolve a *technical contradiction*: improving one property of a system worsens another. The contradiction matrix maps a pair (parameter to improve, parameter that worsens), chosen from 39 engineering parameters, to up to four of 40 inventive principles. The Altshuller Foundation presents the table as Appendix 1 of Altshuller's *Algorithm of Invention* (Moscow, 1973); later editions and translations differ in small ways (see Limitations).

## Sources
- G.S. Altshuller Foundation, table of principles for technical contradictions — https://www.altshuller.ru/triz/technique2.asp — `read` (parsed cell by cell with `tools/triz_crosscheck.py`; used for verification only, not copied).
- Altshuller, *Creativity as an Exact Science* (Gordon and Breach, 1984), ISBN 0-677-21230-5 — `exists` (catalog record only; not opened).
- Five MIT-licensed transcriptions of the matrix, pinned by commit in `clarent_triz/data/matrix.json` — `read`. Licenses, copyright holders and what is *not* verified about their upstream: `clarent_triz/data/DATA_LICENSE.md`.

## Problem it solves
Engineers usually trade one property for another and stop at the compromise. The matrix points to patterns that have been used to remove the trade-off instead, which widens the set of ideas you consider before settling.

## When to use / when NOT to use
- Use: a design is stuck because improving A makes B worse (latency vs. complexity, flexibility vs. simplicity, speed vs. reliability) and you want idea prompts beyond "add a cache".
- Do not use: the problem has a single objective to optimize, the same property must take opposite values (a *physical* contradiction; the engine says so and does not apply the matrix), or you need a ready-made solution. The matrix returns prompts for ideas, never a design.

## How it maps to software work
The 39 parameters are physical (weight, speed, temperature, …). Clarent adds a **software reading** for each (for example *Speed* → latency or throughput; *Device complexity* → components, dependencies and code paths) and a **software example** for each of the 40 principles. Both are Clarent's own adaptation, not Altshuller's, and are meant to help you map your problem; the principles themselves were derived from mechanical and physical patents, so some map to software loosely. Typical uses: architecture trade-offs, performance vs. operability, flexibility vs. complexity.

## Inputs and outputs
- Input: a pair (improving, worsening) given as a number, an English or Spanish name, or a software word such as `latency` (ambiguous words are rejected with the candidates listed, never guessed); or a JSON file with several pairs (`examples/search-api.json`).
- Output: the principles in the order the matrix lists them, each with a description and a software example; the cell's verification status; the reverse cell; and, for several pairs, principles ranked by how many contradictions list them. Markdown or JSON.
- Example (3 lines): `clarent triz-matrix lookup latency "Device complexity"` → *Speed* vs. *Device complexity* → principles 10, 28, 4, 34 (Preliminary action, Mechanics substitution, Asymmetry, Discarding and recovering), cell verified against the 1973 table.

## Algorithm (what is deterministic)
Everything the engine does is deterministic and needs no LLM:
- **Resolve** a name to one of 39 parameters: number → exact name (either language, or alias) → unique substring → unique match in the software reading; anything ambiguous is an error that lists candidates.
- **Look up** the cell (improving, worsening) and report its status: `verified` (the consensus of the voting sources equals the 1973 table), `contested` (it differs; both readings are shown) or `consensus` (the 1973 page was unreadable for that cell). Same parameter on both sides is reported as a physical contradiction; an empty cell is reported as such with the reverse cell.
- **Rank** principles across several contradictions by count, then by mean position in the cells.
- The *dataset* is built reproducibly by `tools/triz_crosscheck.py`: a cell is accepted when a strict majority of five independent transcriptions agree on the set of principles.

What the engine does **not** do: generate or evaluate solutions. That is the agent's job, with the skill's rules.

## Limitations
- The matrix is a heuristic from patents, with known typos across editions. 29 of 1 248 cells are `contested`; a check against the book has not been done.
- The chain of title behind the transcriptions is **not** established (see `DATA_LICENSE.md`). Use `--data DIR` with your own `matrix.json` if you need a clean chain.
- Principles are suggestions, not solutions; software readings and examples are Clarent's adaptation.
- Order inside a cell is the most common order among the sources, which is by Altshuller's suggested priority in the transcriptions we compared; sources occasionally differ on order, and order is not checked against the 1973 table.
- The classic 39-parameter matrix dates from before software engineering existed; newer matrices with more parameters exist and are not included.

## Prior art (GitHub scan)
Scanned 2026-11-24. At least eight small repositories (mostly MIT) ship a TRIZ contradiction matrix as an agent skill or tool: `Antropocosmist/triz-engineering-solver` (24 stars), `ironyjk/triz-agents` (5), `magery-ai/triz-skill` (4), `SharathSPhD/triz-engine` (6), `seogineer/triz-solver` (0), `luchi2333/triz-worker-innovation-research` (3), `sampil/triz-skill` (license not detected) and `ayoub-elkhader/llm-triz-dfx` (1). `ironyjk/strategy-frameworks` (47) includes TRIZ among 30 frameworks and `jenson500/triz-prompt-engineering` (41) is a prompt format, not a matrix. Most are markdown-first. The space is **crowded**; this method's contribution is the cross-checked dataset with per-cell status, a stdlib engine with tests, bilingual output and software readings. See `research/novelty.md`.

## Worked example
`examples/search-api.json` (**synthetic**, English) and `examples/search-api.es.json` (Spanish):
`python -m clarent_triz analyze examples/search-api.json` → three contradictions about making a search API faster; principle 28 (Mechanics substitution) appears in all three.

## Evaluation
Not yet measured. The data quality is measured (see `DATA_LICENSE.md`: 1 218 of 1 248 cells match the 1973 table). Whether the tool helps people find better designs is not: planned as a comparison of design options produced with and without the skill on 10 real architecture trade-offs, rated blind, published even if null.
