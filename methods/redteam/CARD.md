# Red Team — methodology card

## Origin
"Red teaming" in the sense used here comes from the US Army's University of Foreign Military and Cultural Studies (UFMCS), whose *Red Team Handbook* collects techniques to challenge a plan before committing to it: check its assumptions, imagine its failure, argue the opposite, look at it through the adversary's eyes. The techniques themselves come from several traditions that the Handbook cites (intelligence analysis, Gary Klein's decision research). Clarent does not reproduce the Handbook's text or its exercises; it takes a few of its techniques, adds three classes of its own, and puts a deterministic gate in front of what a model writes.

## Sources
- UFMCS, *Red Team Handbook* v5 (15 Apr 2011) — https://newandimproved.com/wp-content/uploads/2014/04/ufmcs_red_team_handbook_apr2011.pdf — `read`. Sections read in full, by printed page: Validating Assumptions pp. 85–88 (an assumption is "information accepted as true in the absence of facts", and must be both *valid* and *necessary*; a red team challenges invalid or unneeded assumptions and finds the unstated ones); Pre-mortem Analysis pp. 138–140 (imagine the plan has failed and write the reasons); ADSO "String of Pearls" p. 140 (sensitivity of a plan to faulty assumptions, to dependencies not in place, and to second- and third-order effects); Key Assumptions Check pp. 151–152 (write down the analytic line, list the premises "both stated and unstated", challenge each, keep those that "must be true"); Devil's Advocacy p. 161; High-Impact/Low-Probability Analysis p. 165; "What If?" Analysis pp. 166–167; Red Team Analysis pp. 173–174 (model how the adversary would think). The copy read is hosted on newandimproved.com, not on a US government site.
- Klein, *Performing a Project Premortem*, IEEE Engineering Management Review (2008), a reprint of the Harvard Business Review article of September 2007 — https://doi.org/10.1109/EMR.2008.4534313 — `exists` (Crossref record with matching title, author and year; the text was not opened). The Handbook credits the pre-mortem to Klein and cites his book.
- Klein, *Sources of Power: How People Make Decisions* (MIT Press, 1998) — https://openlibrary.org/works/OL2731587W — `exists` (Open Library record; not opened). This is the book the Handbook cites for the pre-mortem (footnote 94).
- Heuer & Pherson, *Structured Analytic Techniques for Intelligence Analysis* (3rd ed.) — ISBN-10 150636893X as listed in web search results — `exists` (not opened).

## Problem it solves
A design document or a PR is written by someone who already believes it. The assumptions it rests on are mostly unstated, the failure cases are the ones the author already thought of, and a reviewer who asks a model to "find problems" gets a fluent list of generic worries with nothing behind them. Red Team forces the attack to be *anchored* (it quotes the text it attacks), *backed* (what it calls verified or contradicted cites something that exists), *complete* (six classes, each applied or explicitly skipped) and *ranked* (a short list of what to look at first, and what to verify before trusting it).

## When to use / when NOT to use
- Use: before approving a design doc, ADR or RFC; before merging a PR that changes behavior in ways tests do not pin down (retries, migrations, concurrency, permissions); when everyone agrees too fast.
- Do not use: to review code for bugs line by line (use a code review tool; this method attacks *claims*, not syntax); on a text with no claims to attack (a changelog, a rename); to produce a security assessment — the "abuse" class is a prompt to think about misuse, not a penetration test or a threat model.

## How it maps to software work
A *target* is a design document or a PR (its description plus its diff). An **assumption** is something the target takes for granted, stated or not, that must be true for it to work; each carries a literal quote that it rests on and a status: `verified` (something checked backs it), `contradicted` (something checked says it is false) or `unverified` (nobody has looked). An **attack** says what goes wrong if an assumption is false or abused, in one of six **classes**:

| Class | Question | Origin |
|-------|----------|--------|
| `key-assumptions` | What must be true, and has each thing been checked? | Handbook: Key Assumptions Check; Validating Assumptions |
| `failure-modes` | How does it fail, and what happens next? | Handbook: Pre-mortem; "What If?" |
| `abuse` | How can someone use it in a way its author did not intend? | Handbook: Red Team Analysis, adapted (the adversary is a hostile or careless user) |
| `scale` | What breaks at 10x or 100x? | **Clarent's own**; no Handbook technique by this name |
| `dependency` | What does it depend on that it does not control? | **Clarent's own**; related to the String of Pearls (dependencies not in place) |
| `reversibility` | If this is wrong, how do you go back? | **Clarent's own** |

The questions, the wording of the prompts (`clarent redteam catalog`), and the rating rubrics are Clarent's, not the Handbook's.

## Inputs and outputs
- Input: `findings.json` (`schema: "clarent.redteam/1"`): the target files (`target.files`, with `kind` `design` or `pr`; for a PR use the description and a saved `gh pr diff`), a `root` folder, the `assumptions` and the `attacks` a model proposes, and `skipped_classes` with a reason for each class that does not apply. Every assumption and attack carries a `quote`; every attack carries `check` (a command or a concrete question), `impact` and `plausibility` (1–5), and optional `evidence`.
- Output: Markdown or JSON (`--format json`, `schema: "clarent.redteam.report/1"`): summary, **top 3 attacks**, the **assumption matrix** (assumption × class, with status and evidence), **verify next**, all attacks ranked, class coverage, rejected findings and warnings.
- Commands: `clarent redteam {init,validate,check,top,catalog}`; `check --fail-on S1|S2|S3|S4` and `--strict` for CI. Exit codes: 0 ok · 1 a finding was rejected, or `--fail-on`/`--strict` was reached · 2 invalid input.
- Example (3 lines): `clarent redteam init .clarent/redteam/adr-14.json --target docs/adr-14.md` → fill in assumptions and attacks (the skill does this) → `clarent redteam check .clarent/redteam/adr-14.json`.

## Algorithm (what is deterministic)
1. **Anchor.** Each assumption and attack must quote the target. The quote is searched character by character, case included; the only normalization is that any run of whitespace counts as one space (so a quote may span a line break). For a diff, a quote without the `+`/`-` markers also anchors to the changed line. A missing quote, one shorter than 12 characters, or one not in the target: **rejected**. The report shows where each quote was found (`file:line`).
2. **Back the status.** `verified` and `contradicted` need at least one evidence item `{ref, observation}`. A ref written as `file:line` or `file:a-b` must point at an existing line under the root (paths cannot leave the root); a free-text ref (a command, a log excerpt) is only required to be non-empty. Otherwise **rejected**.
3. **Cascade and de-duplicate.** An attack on a rejected assumption is rejected. An attack without `check` is rejected. Two attacks of the same class on the same assumption whose words overlap by 80% or more (Jaccard) count once.
4. **Score.** `risk = impact × effective plausibility`. The assumption's status moves plausibility: `contradicted` → 5 (the premise is already false), `verified` → at most 2 (the premise holds), `unverified` → as rated. Severity: `S1` risk ≥ 20, `S2` ≥ 12, `S3` ≥ 6, otherwise `S4`. Ties: higher impact, then more evidence items, then id.
5. **Report.** Assumption matrix, top 3, "verify next" (unverified assumptions ordered by the highest risk of the attacks that depend on them), coverage of the six classes, and warnings: a class neither applied nor skipped with a reason; an assumption nobody attacked; fewer than 3 assumptions or 3 attacks; a top attack that rests on an unverified assumption.

## Limitations
- **The engine proves that a finding is anchored and backed, not that it is right.** A quote that exists can still be attacked with a wrong argument. A free-text `ref` is never executed; whether a command was really run and said what the observation says is on the person (or the model) who wrote it.
- The six classes, the 12-character minimum quote, the 80% duplicate threshold, the 1–5 rubrics, the plausibility rule and the severity bands are **Clarent's own constants**, chosen by judgment and not calibrated against any data. Three of the six classes have no counterpart in the Handbook.
- Risk is a prioritization score, **not a probability** and not a measure of how likely the target is to fail.
- A fixed catalog finds what the catalog asks about. It does not replace a domain expert, a threat model or a security review.
- The Handbook's Team A / Team B technique (two independent analyses compared for disagreement) is **not implemented** yet.
- Nothing here is evidence that using it improves reviews; see Evaluation.

## Prior art (GitHub scan)
Scanned 2026-11-25 with short queries (raw data: `research/data/github-scan-redteam.json`). I read READMEs and file lists, not source code. The space is more crowded than `research/novelty.md` recorded on 2026-11-24:
- **Plan stress-tests as prompts.** `aaddrick/contrarian` (43 stars, Unlicense): a subagent and skill that steel-mans a plan, audits assumptions, runs a pre-mortem and returns severity-rated findings; its repository holds prompts and install checks, no engine. Descriptions only: `Hainrixz/abogado-del-diablo` (43), `orange2ai/devils-advocate-skill` (33), `wtfzambo/devils-advocate` (5). Pre-mortem skills are well covered (`Hi1talib1World/Premortem` 88, `AndyShaman/premortem` 61, `MADEVAL/Pre-Mortem-Skill` 59).
- **Adversarial PR review.** `liliu-z/magpie` (180 stars): several models review a PR, debate, and a tool-equipped verifier audits each issue against the code. `liatrio-labs/claude-code-gauntlet` (13, Apache-2.0): seven specialist agents plus a skeptical validator and a blind challenger; reports a benchmark of 15 PRs. `YahampathChandika/adv-review` (6, MIT): every finding must survive a skeptic told to refute it; reports a calibration on 21 PRs with planted defects. `zhjai/agent-arena` (25): evidence-first multi-agent debate. In all of them the verification is another model pass.
- **Not what this is:** the large red-team ecosystem for offensive security (for example `elementalsouls/Claude-BugHunter`, 22.8k stars) is a different use case.
- **What I did not find** in the READMEs and file lists read: a gate that rejects findings by checking quotes against the text, an assumption matrix with verified/unverified/contradicted status that feeds the ranking, or a fixed class catalog with coverage warnings. That is Clarent's angle, and it is narrow: the existing tools may do more than their READMEs say, and their benchmarks (which Clarent does not have yet) are a real advantage.

## Worked example
`examples/design-doc/` — a **synthetic** design for moving notifications to a stream consumer, in English (`design.md` + `findings.json`) and Spanish (`design.es.md` + `findings.es.json`); `examples/pr/` — a synthetic PR (`description.md` + `change.diff` + `findings.json`); `examples/design-doc/findings.rejected.json` — the same design with nine findings the engine must refuse.
`python -m clarent_redteam check examples/design-doc/findings.json` → 6 assumptions (1 verified, 3 unverified, 2 contradicted), 7 attacks, top 3: X3 (rollout leaves no way back, risk 25, S1), X1 (a Redis outage leaves rows nobody reads, 20, S1), X2 (acknowledging on read can lose a notification, 16, S2); the report flags that X2 rests on an unverified assumption and lists what to verify first. The same command on `findings.rejected.json` exits 1 and lists why each of the nine findings was refused.

## Evaluation
Not yet measured. Planned: take 10 real design docs or PRs where a defect was found after merge; run the method with and without the engine's rejection step; count (a) how many findings the gate rejects and whether those were in fact unsupported, (b) whether a contradicted or unverified assumption covers the defect that later appeared, (c) reviewer time. Publish the result even if it is null.
