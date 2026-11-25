---
title: "docs: add a real example to ach from a public, closed bug"
labels: [help wanted, docs, difficulty:medium]
difficulty: medium
effort: "a few hours"
---

## What and why
The only `ach` example, [`flaky-test.json`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach/examples/flaky-test.json), is **synthetic**. A worked example from a real, public, closed bug would show what honest evidence and ratings look like, and the cases collected this way are the seed of the evaluation the card plans (10 real, closed cases with a known root cause).

## What to do
1. Pick a **public, closed** bug or flaky-test issue in an open-source project where several causes were plausible and the real cause is known (link the issue; no private data).
2. Write `methods/ach/examples/<short-name>.json`: a question, 4+ hypotheses plus one `catch_all`, and the evidence that was *actually observed in the issue thread* (logs, commands, bisect results), each with a `ref` that a reader can follow (issue comment URL, commit, `file:line`). Rate every evidence item against **all** hypotheses.
3. Do not rate with hindsight: rate each item as someone who has only seen the evidence up to that point would.
4. Add a short test that pins the expected leader(s) (see the golden tests in [`methods/ach/tests/test_ach.py`](https://github.com/Joaquincuevas/clarent/blob/main/methods/ach/tests/test_ach.py)) and mention the example in the card's *Worked example* section.

## Acceptance criteria
- [ ] `clarent ach validate <file> --strict` passes (every observed item has a `ref`).
- [ ] `clarent ach score <file>` leads with the cause the issue eventually established, **or** the PR says honestly that it did not and why (that is useful too).
- [ ] The issue link and the project's licence are recorded in the example's title or notes.
- [ ] `python tools/test_all.py` passes.

## Difficulty and time
- **Difficulty: medium** (it needs you to read a real thread carefully). Estimated time: a few hours (my estimate; this issue is not from the spec).

Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md); sign off commits (`git commit -s`).
