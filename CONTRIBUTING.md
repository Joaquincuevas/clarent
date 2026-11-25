# Contributing to Clarent

Thanks for helping. Clarent grows by **one method at a time**, and each method is a self-contained folder.

## The house rules

1. **Deterministic core.** The method must compute, validate or reject something with no LLM involved. If it cannot, it is a prompt — good prompts belong in a prompt collection, not here.
2. **No invented sources.** Every source in `method.toml` is marked `read`, `exists`, `blocked` or `unverified`. If you did not open it, say so. `clarent doctor` enforces the vocabulary.
3. **Evidence discipline.** Anything a method treats as a fact must carry a `ref` the reader can follow.
4. **Say what is yours.** Constants, weights and thresholds that are not in the original source must be listed under *Limitations* in the card.
5. **Prior art first.** Re-run `tools/github_scan2.py` for your method and record the result in the card. Duplicating a well-maintained repo is not a contribution we can merge.
6. **No performance claims without an eval.** A null result is welcome.

## Add a method (about an afternoon for a small one)

```bash
# 1. open a "New method" issue first, so nobody duplicates your work
mkdir -p methods/<id>/{<module>,skill,tests,examples}
cp templates/methodology-card.md methods/<id>/CARD.md      # fill every section
cp methods/ach/method.toml methods/<id>/method.toml         # edit: id, name, sources, novelty, surfaces
# 2. write the engine in methods/<id>/<module>/ (stdlib only) exposing main(argv) -> int
# 3. write tests (unittest) and at least one runnable example
# 4. check everything
python tools/test_all.py
PYTHONPATH=src python -m clarent doctor <id>
# 5. if you ship a skill, regenerate the Claude Code plugin and commit the result
python tools/build_plugin.py
```

Use `methods/ach/` as the reference layout. Skill descriptions must stay under 300 characters: they are loaded into the context of every session.

## Smaller contributions (good first issues)

Open ones are listed under the [`good first issue` label](https://github.com/Joaquincuevas/clarent/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Larger pieces of work, one issue per method that is specified but not yet implemented, carry [`new-method`](https://github.com/Joaquincuevas/clarent/issues?q=is%3Aissue+is%3Aopen+label%3Anew-method) and [`help wanted`](https://github.com/Joaquincuevas/clarent/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22). Comment on an issue to claim it. The drafts those issues were created from are in [`research/issues/`](research/issues/).

- Add a **translation** of a method's messages (see `methods/ach/clarent_ach/i18n.py`).
- Add a **worked example** from a real, public, closed bug (link the issue; no private data).
- **Verify a source** currently marked `unverified` in `research/catalog.md`, and upgrade its level with the passage you read.
- Add a **worked example** for `redteam`: a real, public design doc or PR (saved as files) with a `findings.json` whose quotes the engine accepts; or a **rule** (for `spc`, once it exists) — each one is a small set of files.
- Challenge the **attack catalog** of `redteam` (`methods/redteam/clarent_redteam/catalog.py`): the six classes are fixed on purpose, so a proposed change starts with an issue showing a design where the six classes missed something that mattered.
- Improve a **limitation**: found a case where a method misleads? Open an issue with the input that shows it.

## Commits and sign-off

Use the [Developer Certificate of Origin](https://developercertificate.org/): sign commits with `git commit -s`. Keep commits small and the message focused on *why*.

## Tests

`python tools/test_all.py` runs the core tests and every method's tests (stdlib `unittest`, no installs). CI also runs `clarent doctor` and checks that `plugins/claude-code/` is up to date.
