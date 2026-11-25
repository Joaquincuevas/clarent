# TRIZ analysis: Make the search API faster without making it harder to run (SYNTHETIC EXAMPLE)

p95 latency of /search is 900 ms and the target is 300 ms. Every fix we tried (more caches, more replicas, more special cases) adds moving parts, hurts reliability, or makes the system rigid.

## Principles across all contradictions

Ranked by how many contradictions list the principle, then by average position in the cells.

| In | # | Principle | Contradictions |
|--:|--:|---|---|
| 3/3 | 28 | **Mechanics substitution** — Replace polling with events or webhooks; replace manual review with automated static analysis. | 1, 2, 3 |
| 1/3 | 10 | **Preliminary action** — Precompute results; warm caches; ahead-of-time compilation; pre-pulled images and pre-provisioned environments. | 1 |
| 1/3 | 11 | **Beforehand cushioning** — Retries with backoff, fallbacks, redundancy, backups, and kill switches behind feature flags. | 2 |
| 1/3 | 15 | **Dynamics** — Autoscaling; adaptive timeouts; dynamic configuration and feature flags; adaptive batch sizes. | 3 |
| 1/3 | 29 | **Pneumatics and hydraulics** — Elastic or serverless pools instead of fixed allocations; streams instead of fixed-size buffers. | 3 |
| 1/3 | 35 | **Parameter changes** — Change the data format (JSON to Protobuf); compression level; consistency or isolation level; lock granularity. | 2 |
| 1/3 | 4 | **Asymmetry** — Separate read and write paths (CQRS); one writer with many read replicas; asymmetric roles in a protocol. | 1 |
| 1/3 | 27 | **Cheap short-living objects** — Ephemeral containers and VMs; spot instances; disposable preview environments; immutable infrastructure. | 2 |
| 1/3 | 37 | **Thermal expansion** — Self-resizing buffers, connection pools and thread pools; tiers of timeouts or caches that react at different speeds. | 3 |
| 1/3 | 34 | **Discarding and recovering** — Garbage collection; cache eviction and TTLs; log rotation; automatic cleanup of ephemeral environments; compaction. | 1 |

## Contradiction 1: improve «Speed» / worsen «Device complexity»

_Faster responses, but each speed-up adds components and code paths._

- **Improving:** 9. Speed — _software reading: latency, response time or throughput of an operation_
- **Worsening:** 36. Device complexity — _software reading: system complexity: number of components, dependencies, code paths_
- «latency» was interpreted as parameter 9 (Speed) by software-reading match

> Cell verified: the consensus of 4 independent transcriptions equals the Altshuller Foundation 1973 table.

### Principles (in the order the matrix lists them)

| # | Principle | What it means | Software example |
|--:|---|---|---|
| 10 | **Preliminary action** | Carry out the required change, fully or partly, before it is needed. | Precompute results; warm caches; ahead-of-time compilation; pre-pulled images and pre-provisioned environments. |
| 28 | **Mechanics substitution** | Replace the way the parts interact with a different kind of channel or field. | Replace polling with events or webhooks; replace manual review with automated static analysis. |
| 4 | **Asymmetry** | Replace a symmetrical form with an asymmetrical one, or increase existing asymmetry. | Separate read and write paths (CQRS); one writer with many read replicas; asymmetric roles in a protocol. |
| 34 | **Discarding and recovering** | Let parts that have done their job go away or change during operation, and restore used-up parts straight away. | Garbage collection; cache eviction and TTLs; log rotation; automatic cleanup of ephemeral environments; compaction. |

Principles are prompts for ideas, not solutions. Check every candidate against the original contradiction: a good idea improves «Speed» without bringing back the worsening of «Device complexity».

Reverse cell (improve «Device complexity», worsen «Speed»): 34, 10, 28

## Contradiction 2: improve «Speed» / worsen «Reliability»

_Aggressive caching and shortcuts made incidents more frequent._

- **Improving:** 9. Speed — _software reading: latency, response time or throughput of an operation_
- **Worsening:** 27. Reliability — _software reading: reliability and availability_

> Cell verified: the consensus of 5 independent transcriptions equals the Altshuller Foundation 1973 table.

### Principles (in the order the matrix lists them)

| # | Principle | What it means | Software example |
|--:|---|---|---|
| 11 | **Beforehand cushioning** | Prepare emergency means in advance to compensate for the low reliability of an object. | Retries with backoff, fallbacks, redundancy, backups, and kill switches behind feature flags. |
| 35 | **Parameter changes** | Change the state, concentration, flexibility or other parameters of the object. | Change the data format (JSON to Protobuf); compression level; consistency or isolation level; lock granularity. |
| 27 | **Cheap short-living objects** | Replace an expensive durable object with several cheap disposable ones, accepting some loss of quality. | Ephemeral containers and VMs; spot instances; disposable preview environments; immutable infrastructure. |
| 28 | **Mechanics substitution** | Replace the way the parts interact with a different kind of channel or field. | Replace polling with events or webhooks; replace manual review with automated static analysis. |

Principles are prompts for ideas, not solutions. Check every candidate against the original contradiction: a good idea improves «Speed» without bringing back the worsening of «Reliability».

Reverse cell (improve «Reliability», worsen «Speed»): 21, 35, 11, 28

## Contradiction 3: improve «Adaptability or versatility» / worsen «Device complexity»

_Product wants many ranking variants without a tangle of special cases._

- **Improving:** 35. Adaptability or versatility — _software reading: flexibility: configurability, extensibility, range of use cases_
- **Worsening:** 36. Device complexity — _software reading: system complexity: number of components, dependencies, code paths_

> Cell verified: the consensus of 5 independent transcriptions equals the Altshuller Foundation 1973 table.

### Principles (in the order the matrix lists them)

| # | Principle | What it means | Software example |
|--:|---|---|---|
| 15 | **Dynamics** | Let the characteristics of an object adjust to be optimal at each stage; make a rigid object flexible or adaptive. | Autoscaling; adaptive timeouts; dynamic configuration and feature flags; adaptive batch sizes. |
| 29 | **Pneumatics and hydraulics** | Replace rigid parts with gas or liquid ones that fill, flow or cushion. | Elastic or serverless pools instead of fixed allocations; streams instead of fixed-size buffers. |
| 37 | **Thermal expansion** | Use material that expands or contracts with its conditions, or combine materials that react at different rates. | Self-resizing buffers, connection pools and thread pools; tiers of timeouts or caches that react at different speeds. |
| 28 | **Mechanics substitution** | Replace the way the parts interact with a different kind of channel or field. | Replace polling with events or webhooks; replace manual review with automated static analysis. |

Principles are prompts for ideas, not solutions. Check every candidate against the original contradiction: a good idea improves «Adaptability or versatility» without bringing back the worsening of «Device complexity».

Reverse cell (improve «Device complexity», worsen «Adaptability or versatility»): 29, 15, 28, 37

---
_Matrix data: consensus of independent transcriptions of Altshuller's table (see DATA_LICENSE.md). Descriptions and software examples are Clarent's own adaptation._

