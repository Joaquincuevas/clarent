---
name: triz-matrix
description: Resolve a design trade-off (improving A worsens B) with TRIZ's contradiction matrix. Returns inventive principles with software examples and says how far each matrix cell can be trusted. Use when a design is stuck between two competing properties.
disable-model-invocation: true
argument-hint: [trade-off in one sentence]
---

# TRIZ contradiction matrix

You are helping resolve a **technical contradiction**: improving one property of a system worsens another. A bundled script looks up the classical matrix; your job is to state the contradiction precisely and turn the principles into concrete, checkable design candidates.

Trade-off: $ARGUMENTS

## Tooling

Stdlib-only Python. Use whichever of `python3` / `python` exists:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" params                      # the 39 parameters with their software readings
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" lookup "<improving>" "<worsening>"
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" rank --pair "A:B" --pair "C:D"
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" principles                  # the 40 principles
python3 "${CLAUDE_SKILL_DIR}/scripts/run.py" info                        # data provenance
```

Add `--lang es` before the subcommand for Spanish, and `--format json` to parse the output.

## Procedure

1. **State the contradiction in one sentence:** "If we improve X, then Y gets worse." Both X and Y must be properties of the *same* system, and you must be able to say how you would notice each.
2. **Map X and Y to the 39 parameters.** Run `params` and read the *software reading* column. Pass a number or exact name to `lookup`. If the tool reports an ambiguous or unknown name, choose from the candidates it lists; do not guess. For "Loss of …" parameters, improving means *reducing* the loss.
3. **Look up the pair.** Read the cell status first:
   - `verified`: the consensus matches the 1973 table.
   - `contested`: the sources and the 1973 table disagree; consider the principles from **both** lists.
   - empty cell: say so, then try the reverse cell the tool reports, or restate the parameters more generally or more specifically.
   - same parameter on both sides: it is a *physical* contradiction (one property needs opposite values); say so and consider separation in space, time, condition or between whole and parts instead.
4. **For each principle returned (top 2–4), write one concrete candidate for THIS system:** what exactly would change, in which component. A candidate that only repeats the software example from the table is not done.
5. **Test each candidate against the original contradiction.** Keep it only if it improves X *without* bringing back the worsening of Y, or if you can state what it costs and why that is acceptable. Discard the rest and say why.
6. **If you have several related contradictions,** use `rank`: principles that appear in more than one are worth the first look.

## Reporting

For each kept candidate give: the principle (number and name), the concrete change, the effect on X, the effect on Y, and how you would verify both. Quote the cell status. Offer the data caveat (`info`) if the user asks about trust.

## Rules

- The matrix returns **prompts for ideas, not solutions**. Never present a principle as proven to work.
- Software readings and examples are an adaptation of a physical-patent method; say when a principle maps loosely.
- Do not invent parameters or principles; use only what the tool returns.
- A candidate you did not check against the contradiction is a suggestion, not a result.
