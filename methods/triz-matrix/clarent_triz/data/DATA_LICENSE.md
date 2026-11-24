# Data license and provenance

This folder holds three kinds of content with different origins. Read this file before redistributing the data.

| File | What it is | License / status |
|------|------------|------------------|
| `catalog.json` | Names of the 39 parameters and 40 principles; descriptions, software readings and software examples in English and Spanish | Names are the standard published names (taken from source E; source A differs only in wording for three principles; aliases cover wording variants of parameters). Descriptions, readings and examples are **Clarent's own wording**, Apache-2.0. They are not Altshuller's text. |
| `matrix.json` | The 39x39 contradiction matrix: a **consensus** of five independent transcriptions, each cell compared with the Altshuller Foundation's 1973 table | Derived from the MIT-licensed works listed below; see "What is and is not verified". |
| this file | Notices | Apache-2.0 (own text) plus the MIT notices required below. |

## Voting sources (all MIT; the `LICENSE` file of each repository was read on 2026-11-24)

A cell is accepted when a strict majority of these sources agree on the set of principles. Commits and file hashes are pinned in `matrix.json` (`meta.voting_sources`) and reproducible with `tools/triz_crosscheck.py`.

| Key | Repository | File used | Copyright notice in its LICENSE |
|-----|------------|-----------|---------------------------------|
| A | https://github.com/Antropocosmist/triz-engineering-solver | `resources/contradiction_matrix.json` | Copyright (c) 2026 useful-skills contributors |
| B | https://github.com/SharathSPhD/triz-engine | `triz-engine/data/triz-matrix.json` | Copyright (c) 2026 triz-engine contributors |
| C | https://github.com/seogineer/triz-solver | `skills/triz-analysis/data/contradiction-matrix.json` | Copyright (c) 2026 DoGyeong Seo |
| D | https://github.com/magery-ai/triz-skill | `skills/triz/data/contradiction-matrix.csv` | Copyright (c) 2026 magery.ai |
| E | https://github.com/luchi2333/triz-worker-innovation-research | `triz-worker-innovation-research/references/contradiction-matrix.json` | Copyright (c) 2026 luchi2333 |

### MIT License (applies to the data taken from the five repositories above)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notices and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Verification reference (not redistributed)

The consensus was compared cell by cell with the table on the official site of the G.S. Altshuller Foundation, <https://www.altshuller.ru/triz/technique2.asp>, which cites G. S. Altshuller, *Algorithm of Invention* (Moscow, Moskovsky Rabochy, 1973), Appendix 1. That page is **not** copied into this repository. For the cells where the two disagree, `matrix.json` records the 1973 reading (`alt`: a list of principle numbers) so you can see both. Principle numbers are facts, not creative text; if the Foundation objects to even that, delete the `alt` fields.

## What is and is not verified

**Verified in this repository (2026-11-24):**
- Each voting source's repository has a `LICENSE` file with the MIT text above.
- 1 218 of 1 248 filled cells have the same set of principles as the 1973 table; 29 cells differ (status `contested`); 1 cell could not be read on the 1973 page because of a defect on the page (status `consensus`).
- No cell is `disputed` among the voting sources (every cell has a strict majority).

**Not verified, and what that means for you:**
- The chain of title *behind* the five repositories. Repository A states that it imported the matrix from `kamil-szczepanik/TRIZ-Agents` (a 2007 transcription by Casey Perno of Altshuller 1985). That upstream repository's README says "MIT" but it has **no LICENSE file** and GitHub reports it as unlicensed. Repository D cites triz40.com and the `pytriz` package; repository E cites triz-consulting.de and the same TRIZ-Agents spreadsheet. We could not establish the terms of those original transcriptions.
- Whether a compilation of Altshuller's published research results is protected by copyright, and by whom. The matrix records the results of Altshuller's analysis of patents (1946 onward); the individual cells are factual associations, but we cannot give legal advice and make no claim either way.
- That the matrix is *correct*. It is the classical table, which has known typos in print and online copies. The 29 `contested` cells are exactly where our sources and the 1973 table disagree. A comparison with the book (Altshuller, *40 Principles*, Shulyak and Rodman translation, 1997) has not been done.

**If you need a clean chain of title,** do not use the bundled `matrix.json`. Supply your own with `--data DIR` (it must contain a `matrix.json` in the same format; `catalog.json` falls back to the bundled one). The engine, the catalog texts and the tests do not depend on the bundled matrix.

## Reporting a problem

Open an issue in the Clarent repository if you hold rights to any of this data and want it removed or credited differently, or if you find a wrong cell (include the cell, the source and the page).
