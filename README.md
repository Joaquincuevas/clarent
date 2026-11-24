# Clarent

**Classic decision, optimization and engineering methods — as tools that compute, not prompts that sound smart.**

Military doctrine, Toyota's shop floor, Soviet inventors' algorithms, NASA safety engineering: decades of method for finding root causes, attacking plans and estimating honestly. Clarent turns them into small, auditable tools for developers and their coding agents: Claude Code skills, a CLI, and (soon) hooks, MCP tools and GitHub Actions.

> **Status: pre-release (v0.1).** Two methods are implemented end-to-end (`ach`, 23 tests; `triz-matrix`, 38 tests). Eight more are specified in [`research/product-spec.md`](research/product-spec.md). Nothing here claims to make your agent fix more bugs — see [What we do not claim](#what-we-do-not-claim).

## Why another methods repo?

Collections of "thinking frameworks as prompts" already exist (the biggest we found has ~1.7k stars; see [`research/novelty.md`](research/novelty.md)). They give an agent a checklist. Clarent's rule is stricter: **every method must have a deterministic core** — something the code computes or rejects with no LLM involved — plus evidence discipline:

- the agent **proposes**, the engine **scores, validates and can say no**;
- every observed fact needs a `ref` (the command, `file:line` or log that produced it);
- reports say what they are: an ACH score is a *ranking of inconsistencies*, never a probability.

## 60-second tour (ACH: debugging with competing hypotheses)

```bash
git clone https://github.com/OWNER/clarent && cd clarent      # replace OWNER once published
python -m pip install -e .                                     # stdlib only; Python >= 3.11

clarent list
clarent ach score methods/ach/examples/flaky-test.json         # synthetic flaky-test example
clarent ach next  methods/ach/examples/flaky-test.json         # the most discriminating test to run next

clarent triz-matrix lookup latency "Device complexity"          # TRIZ: principles for a design trade-off
clarent triz-matrix analyze methods/triz-matrix/examples/search-api.json
```

What you get for a flaky test that fails 1 run in 8 (synthetic example): clock-dependence, network and hash-seed hypotheses are **refuted** by cited evidence, two causes tie for the lead, and the engine tells you which single experiment separates them — *"reproduce serially with the failing run's random seed"*.

### In Claude Code

```text
/plugin marketplace add OWNER/clarent
/plugin install clarent-methods@clarent
/clarent-methods:ach test_checkout_total fails ~1 in 8 CI runs
/clarent-methods:triz-matrix make /search faster without making it harder to run
```

The skill is manual-only (`disable-model-invocation`), so it costs no context until you call it. It makes the agent list rival causes first, gather evidence by running commands, rate each item against *all* hypotheses, and re-score until one explanation survives or the diagnosis is declared unresolved.

## Methods

| Method | Tool | Status |
|--------|------|--------|
| Analysis of Competing Hypotheses (Heuer, CIA) | `ach` | **implemented** (reference) |
| Red Teaming (UFMCS) | `redteam` | spec |
| Statistical Process Control (Shewhart) on CI | `spc` | spec |
| Commander's Intent / Mission Command | `intent` | spec |
| Reference Class Forecasting | `rcf` | spec |
| FMEA | `fmea` | spec |
| Kepner-Tregoe IS / IS-NOT | `kt` | spec |
| STAMP / STPA | `stpa` | spec |
| Heilmeier Catechism | `gate` | spec |
| TRIZ contradiction matrix (Altshuller) | `triz-matrix` | **implemented** (beta) |
| Fault Tree Analysis | `fta` | spec (moved to v2) |

Research behind the selection (63 methods catalogued, sources marked `read / exists / blocked / unverified`): [`research/`](research/).

## What we do not claim

- That a skill makes an agent solve more tasks. gstack (one of the biggest repos in this space) publishes a null result on its own bug-fixing benchmark in its README; we will publish ours, null or not.
- That the numbers are Heuer's, Shewhart's or Goldratt's. Where a constant is ours (weights, thresholds) the method card says so.
- That the catalog's sources are all verified. Each one carries its verification level.
- That the TRIZ matrix data has a clean chain of title. Its licenses and gaps are written down in [`DATA_LICENSE.md`](methods/triz-matrix/clarent_triz/data/DATA_LICENSE.md); you can supply your own matrix with `--data`.

## Contributing

A new method is one folder, one card, one engine, tests and an example. Start with [`CONTRIBUTING.md`](CONTRIBUTING.md); `clarent doctor` tells you what is missing.

## License

Apache-2.0. See [`LICENSE`](LICENSE).
