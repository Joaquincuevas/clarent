# r/ClaudeCode (borrador)

> **Reglas sin verificar:** Reddit bloquea la lectura automática. Antes de publicar, lee las reglas con tu sesión (ver [`README.md`](README.md)). Confirma en particular: autopromoción, flair, si piden código o enlace al repo en el cuerpo, y divulgación del uso de IA. Este público es técnico y usa Claude Code a diario: entra por la instalación y los detalles del plugin.

**Enfoque:** mecánica del plugin, coste de contexto, y lo que el motor determinista hace distinto de una skill de solo prompt.

## Título

```
Clarent: Claude Code plugin with manual-only skills backed by deterministic engines (ACH, red team, TRIZ), stdlib Python, no deps
```

## Cuerpo

```
Most "thinking framework" skills are a prompt. This is a plugin where each skill
calls a small Python engine that the agent can't talk its way around.

How it fits Claude Code:
- Marketplace + plugin: `/plugin marketplace add Joaquincuevas/clarent`, then
  `/plugin install clarent-methods@clarent`. Validated with
  `claude plugin validate`.
- The skills are `disable-model-invocation` (manual only), so they add nothing to
  your context until you run e.g. `/clarent-methods:ach why does test_x fail 1 in 8 runs`.
- The same engines are a CLI (`pip install clarent-methods`, command `clarent`),
  so you can use them in scripts or CI without an agent.

What the engines do (all deterministic, no LLM):
- `ach`: scores rival causes by inconsistency, finds evidence that doesn't
  discriminate, ranks the next test. Every observed fact needs a `ref`
  (command, file:line or log) or it is rejected.
- `redteam`: rejects attack findings that aren't quoted from the doc or PR they
  attack; builds an assumption matrix and ranks the top attacks.
- `triz-matrix`: Altshuller's contradiction matrix with software readings of the
  parameters.

The agent proposes; the engine validates and can say no. [GIF]

What I'm not claiming: no eval yet showing better task success (I will publish
it, null or not), only tested with Claude Code, 8 more methods are specs only,
and the TRIZ data has a documented incomplete chain of title.

144 tests; `clarent doctor` validates manifests, cards and skills. Apache-2.0.
https://github.com/Joaquincuevas/clarent
[Disclose here how it was built, including use of Claude Code.]

Feedback welcome on the skill/CLI split and on what a good eval for this would look like.
```

## Antes de publicar

- [ ] Confirmar reglas y flair.
- [ ] Probar `/plugin marketplace add` + `/plugin install` en una instalación limpia el mismo día (verificado el 2026-11-26 con el CLI de Claude Code y un directorio de configuración aislado).
- [ ] Rellenar la divulgación.
