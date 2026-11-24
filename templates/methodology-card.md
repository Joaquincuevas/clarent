# <Method name> — methodology card

> Copy this file to `methods/<id>/CARD.md`. Every section is required: `clarent doctor` fails if one is missing.
> Rule of the house: **no invented sources.** Mark each source `read`, `exists`, `blocked` or `unverified` in `method.toml`.

## Origin
Who created it, where, when, for which problem. One short paragraph. Say which parts are folklore and which are documented.

## Sources
Primary sources first (manuals, papers, doctrine). For each: title, URL or full citation, and how much you verified (`read` / `exists` / `blocked` / `unverified`). Quote the passage you rely on.

## Problem it solves
The failure it prevents, in one or two sentences, without jargon.

## When to use / when NOT to use
Concrete triggers ("a test fails 1 in 8 runs") and concrete anti-triggers ("the cause is already known").

## How it maps to software work
Which daily activity (debugging, review, planning, incidents, refactor, prompts) and what the mapping *adds* beyond the original method. Say clearly what is your own adaptation.

## Inputs and outputs
Input file(s) and schema version. Output report(s). One real example, three lines.

## Algorithm (what is deterministic)
What the engine computes or validates with no LLM involved. If the answer is "nothing", this is a prompt, not a Clarent method — explain why it still belongs.

## Limitations
Known failure modes of the method and of this implementation. Which constants are yours and not the source's.

## Prior art (GitHub scan)
Date of the scan, queries used, closest repos with stars and last push, and the gap this method fills. Update when it changes.

## Worked example
A runnable example in `examples/` and the command to run it. Mark synthetic examples as synthetic.

## Evaluation
How you would know it helps: the eval task, the baseline, the result (a null result is fine and must be published).
