---
name: redteam
description: Attack a design doc, ADR or PR with six fixed attack classes before approving it. A script rejects findings that are not quoted from the text or not backed by evidence, builds an assumption matrix and ranks the top 3 attacks.
disable-model-invocation: true
argument-hint: [path to a design doc | PR number]
---

# Red team — attack a design or a PR

You are the red team. Your job is to find what the author did not, **and to prove each finding is anchored in the text**. A bundled script rejects any finding whose quote is not in the target or whose evidence does not exist; it does not judge whether you are right, so be right.

Target: $ARGUMENTS

## Tooling

Stdlib-only Python. Use whichever of `python3` / `python` exists:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" catalog                       # the six classes, their questions, the 1-5 scales
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" init  .clarent/redteam/<slug>.json --target <file>
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" check .clarent/redteam/<slug>.json
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" top   .clarent/redteam/<slug>.json
```

Add `--lang es` before the subcommand for Spanish output. In the findings file set `"root"` to the repository root relative to the file (for `.clarent/redteam/x.json`, `"../.."`): target files and `file:line` refs are resolved from there. `init` does this when you run it from the repo root.

## Procedure

1. **Get the target as files.**
   - A design doc: its path.
   - A PR: `gh pr view <n> --json title,body -q '"# "+.title+"\n\n"+.body' > .clarent/redteam/<slug>/description.md` and `gh pr diff <n> > .clarent/redteam/<slug>/change.diff`; list both under `target.files` with `"kind": "pr"`.
2. **Read the target and `catalog`.** Do not attack anything you have not read.
3. **List assumptions** (the key assumptions check): what must be true for this to work, **including what the text never says** (ordering, who calls it, volume, environment, rollback). For each: `id`, `text`, a `quote` copied character by character from a passage it rests on (at least 12 characters), `status: "unverified"` and a `check` (a command or a concrete question that would settle it). Prefer 5–8 that matter over 15 that do not.
4. **Verify what you can by running things.** Read the code, run the command, grep the callers. Then:
   - `contradicted`: you found something that says it is false → add `evidence: [{ "ref": "path:line" or the command you ran, "observation": "what it showed" }]`.
   - `verified`: you found something that says it holds → same evidence.
   - Anything you merely believe stays `unverified`. A `ref` you did not produce this session is an invented ref.
5. **Attack, class by class.** For each of `key-assumptions`, `failure-modes`, `abuse`, `scale`, `dependency`, `reversibility`: write at least one attack, or add the class to `skipped_classes` with a real reason. Each attack: `assumption` (the one it attacks), `quote` (literal, from the target), `attack` (what goes wrong if the assumption is false or abused, in concrete terms: no "be careful with scalability"), `check` (how to confirm it), `impact` and `plausibility` 1–5 using the rubric printed by `catalog`. Rate honestly; the script raises plausibility itself where you proved the assumption false.
6. **Run `check`.** Read **Rejected findings first**. Fix each one by finding the real passage or the real evidence; never loosen a quote to make it match, never delete the check that failed. Re-run until nothing is rejected.
7. **Verify next.** Do the top items of that list (run the `check` commands), update statuses and evidence, re-run. Stop after 2 rounds or when the top 3 no longer rest on unverified assumptions.

## Reporting

Paste the Markdown report. Lead with the top 3 attacks and what to verify first. Say that the ranking is a prioritization, **not a probability**, and that the script proves findings are anchored and backed, not that they are correct. If a class was skipped, say why in one line.

## Rules

- Quote, do not paraphrase: copy the passage. Do not attack text that is not in the target.
- Never mark `verified` or `contradicted` without evidence you produced; never invent a `file:line`.
- Do not pad: a rejected or duplicate finding is noise. Three real attacks beat ten generic ones.
- Do not edit the target while attacking it. If asked to fix the design afterwards, do it as a separate step and re-run `check` on the new text.
- For CI: `check --fail-on S1` exits 1 if an accepted attack is that severe.
