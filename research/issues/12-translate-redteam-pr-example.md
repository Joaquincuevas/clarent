---
title: "i18n: translate the redteam PR example to Spanish"
labels: [good first issue, i18n, difficulty:easy]
difficulty: easy
effort: "1–2 hours"
---

## What and why
The `redteam` design-doc example exists in English and Spanish, but the PR example ([`methods/redteam/examples/pr/`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam/examples/pr)) is English only. A Spanish version shows that the method works on non-English text, and the engine **checks your translation for you**: every `quote` must appear literally in the target text, or the finding is rejected.

## What to do
- Add `description.es.md` (translate [`description.md`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam/examples/pr/description.md); keep the line structure so `file:line` refs still point at the right lines). `change.diff` is code and stays as it is.
- Add `findings.es.json` (translate the titles, assumptions, attacks and checks; **quotes taken from the description must match your Spanish text exactly**; quotes taken from the diff stay as they are; keep the ids, classes, statuses and ratings).
- Add a test next to `test_spanish_example_gives_the_same_ranking` in [`methods/redteam/tests/test_redteam.py`](https://github.com/Joaquincuevas/clarent/blob/main/methods/redteam/tests/test_redteam.py) asserting that the Spanish PR example has no rejections and the same ranking as the English one.
- Label the example as synthetic ("EJEMPLO SINTÉTICO"), like the design-doc one.

## Acceptance criteria
- [ ] `python -m clarent --lang es redteam check methods/redteam/examples/pr/findings.es.json` exits 0, with no rejected findings.
- [ ] The top 3 and every risk score equal the English example's.
- [ ] `python tools/test_all.py` passes; `python tools/build_plugin.py --check` still passes (examples are not copied into the plugin, but check anyway).

## Difficulty and time
- **Difficulty: easy.** Estimated time: 1–2 hours (my estimate; this issue is not from the spec).

Read [`CONTRIBUTING.md`](https://github.com/Joaquincuevas/clarent/blob/main/CONTRIBUTING.md); sign off commits (`git commit -s`).
