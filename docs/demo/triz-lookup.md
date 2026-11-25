# TRIZ contradiction: improve «Speed» without worsening «Device complexity»

- **Improving:** 9. Speed — _software reading: latency, response time or throughput of an operation_
- **Worsening:** 36. Device complexity — _software reading: system complexity: number of components, dependencies, code paths_
- «latency» was interpreted as parameter 9 (Speed) by software-reading match

> Cell verified: the consensus of 4 independent transcriptions equals the Altshuller Foundation 1973 table.

## Principles (in the order the matrix lists them)

| # | Principle | What it means | Software example |
|--:|---|---|---|
| 10 | **Preliminary action** | Carry out the required change, fully or partly, before it is needed. | Precompute results; warm caches; ahead-of-time compilation; pre-pulled images and pre-provisioned environments. |
| 28 | **Mechanics substitution** | Replace the way the parts interact with a different kind of channel or field. | Replace polling with events or webhooks; replace manual review with automated static analysis. |
| 4 | **Asymmetry** | Replace a symmetrical form with an asymmetrical one, or increase existing asymmetry. | Separate read and write paths (CQRS); one writer with many read replicas; asymmetric roles in a protocol. |
| 34 | **Discarding and recovering** | Let parts that have done their job go away or change during operation, and restore used-up parts straight away. | Garbage collection; cache eviction and TTLs; log rotation; automatic cleanup of ephemeral environments; compaction. |

Principles are prompts for ideas, not solutions. Check every candidate against the original contradiction: a good idea improves «Speed» without bringing back the worsening of «Device complexity».

Reverse cell (improve «Device complexity», worsen «Speed»): 34, 10, 28

---
_Matrix data: consensus of independent transcriptions of Altshuller's table (see DATA_LICENSE.md). Descriptions and software examples are Clarent's own adaptation._

