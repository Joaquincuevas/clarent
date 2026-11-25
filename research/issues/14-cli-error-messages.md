---
title: "cli: improve error messages and argument validation"
labels: [good first issue, enhancement, difficulty:easy]
difficulty: easy
effort: "a few hours"
---

## What and why
Most errors are clean (`error: file not found: nope.json`), but a few paths in the core CLI ([`src/clarent/cli.py`](https://github.com/Joaquincuevas/clarent/blob/main/src/clarent/cli.py)) and in the argument parsers are unhelpful. Found by running the commands on 2026-11-25:

| Command | What happens today | What it should do |
|---------|--------------------|-------------------|
| `clarent acch score x.json` | `error: unknown command or method 'acch'` followed by a usage line that does not list the methods | Suggest the closest match (`did you mean 'ach'?`, e.g. with `difflib.get_close_matches`) and print the installed methods |
| `clarent list --format xml` | silently prints the table and exits 0 | Reject an unsupported format with a clear error and exit 2 |
| `clarent ach` (no subcommand) | `clarent-ach: error: the following arguments are required: cmd` | Say `<command>` instead of the internal name `cmd`, and show the available subcommands |
| `clarent --lang es ach score` | the missing-argument error is in English | At least keep it consistent, or translate the parser's messages for the methods that have a Spanish catalog |

(The last row can be a documented limitation if translating argparse is too invasive: say so in the PR.)

## What to do
Fix the first three rows in `src/clarent/cli.py` and the method parsers' `dest`/`metavar`, with tests in [`tests/test_core.py`](https://github.com/Joaquincuevas/clarent/blob/main/tests/test_core.py) that pin the new messages and exit codes (look at how `run()` captures output there).

## Acceptance criteria
- [ ] Each fixed row has a test; exit codes are unchanged for valid input and 2 for invalid input.
- [ ] No new runtime dependency (standard library only).
- [ ] `python tools/test_all.py` passes; `PYTHONPATH=src python -m clarent doctor` still passes.

## Difficulty and time
- **Difficulty: easy.** Estimated time: a few hours (my estimate; this issue is not from the spec).

Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md); sign off commits (`git commit -s`).
