# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-11-26

First public release, published on PyPI as `clarent-methods` (the CLI is still `clarent`).

### Added

- `clarent` command with `list`, `doctor` and delegation to each method's own CLI; `--lang en|es`.
- Method `ach` (Analysis of Competing Hypotheses): scores competing causes by inconsistency, finds
  non-discriminating evidence and recommends the next most informative test.
- Method `redteam`: attacks a design doc or a PR with a fixed catalog of six attack classes; rejects
  findings it cannot anchor in the text and ranks the top attacks.
- Method `triz-matrix`: Altshuller contradiction matrix lookup with software readings of the 39
  parameters; every cell is verified against the 1973 table (data under `DATA_LICENSE.md`).
- Claude Code plugin and marketplace entry generated from the methods.
- Standard-library-only runtime: no dependencies, Python >= 3.11.
- Release workflow publishing to PyPI through Trusted Publishing (OIDC).

[0.1.0]: https://github.com/Joaquincuevas/clarent/releases/tag/v0.1.0
