# Clarent<!-- id: title -->

[English](https://github.com/Joaquincuevas/clarent/blob/main/README.md) | Español

[![ci](https://github.com/Joaquincuevas/clarent/actions/workflows/ci.yml/badge.svg)](https://github.com/Joaquincuevas/clarent/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/clarent-methods.svg)](https://pypi.org/project/clarent-methods/)
[![license: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![python: >=3.11](https://img.shields.io/badge/python-%E2%89%A53.11-blue.svg)](pyproject.toml)

![clarent ach puntuando el ejemplo flaky-test y luego listando las siguientes pruebas a ejecutar](https://raw.githubusercontent.com/Joaquincuevas/clarent/main/docs/demo/ach.gif)

<sub>Salida real de `clarent ach` sobre el ejemplo sintético flaky-test; solo la velocidad de tecleo y las pausas están escenificadas ([`docs/demo/make_ach_gif.py`](docs/demo/make_ach_gif.py) lo regenera).</sub>

**Métodos clásicos de decisión, optimización e ingeniería, como herramientas que calculan, no prompts que suenan inteligentes.**

## ¿Qué es Clarent?<!-- id: what-is -->

Las personas y los agentes de IA tienden a anclarse en la primera hipótesis plausible. Existen métodos probados (CIA, ejército, Toyota, NASA, TRIZ soviético), pero viven en manuales.
Clarent los convierte en comandos que calculan (un motor determinista, sin ningún LLM), no en prompts:

| Comando | Origen | Qué hace |
|---|---|---|
| `clarent ach` | Análisis de Hipótesis Competidoras, CIA (Heuer) | Ordena las causas rivales según cuánta evidencia las contradice y sugiere la siguiente prueba a ejecutar. |
| `clarent redteam` | Red Teaming, Ejército de EE. UU. (UFMCS) | Ataca un documento de diseño o un PR y rechaza todo ataque que no esté citado del texto. |
| `clarent triz-matrix` | Matriz de contradicciones TRIZ, Altshuller (URSS) | Dado "mejorar X sin empeorar Y", devuelve los principios inventivos de la tabla de 1973. |

La diferencia: la IA propone; el motor puntúa, valida y rechaza lo que no tenga evidencia.

> **Estado: pre-lanzamiento (v0.1).** Hay tres métodos implementados de punta a punta (`ach`, 24 pruebas; `redteam`, 82; `triz-matrix`, 38). Otros ocho están especificados en [`research/product-spec.md`](research/product-spec.md); el resto del plan está en [`research/roadmap.md`](research/roadmap.md). Nada de lo que hay aquí afirma que tu agente corregirá más errores; véase [Lo que no afirmamos](#lo-que-no-afirmamos).

## Instalación<!-- id: install -->

```bash
pip install clarent-methods                                        # el CLI `clarent`; Python >= 3.11, sin dependencias
# o la versión de desarrollo:  pip install git+https://github.com/Joaquincuevas/clarent
```

```text
/plugin marketplace add Joaquincuevas/clarent                      # en Claude Code: añade el marketplace...
/plugin install clarent-methods@clarent                            # ...e instala las skills
```

## ¿Por qué otro repositorio de métodos?<!-- id: why -->

Doctrina militar, el taller de Toyota, los algoritmos de los inventores soviéticos, la ingeniería de seguridad de la NASA: décadas de método para encontrar causas raíz, atacar planes y estimar con honestidad. Clarent los convierte en herramientas pequeñas y auditables para desarrolladores y sus agentes de programación: skills de Claude Code, un CLI y (pronto) hooks, herramientas MCP y GitHub Actions.

Ya existen colecciones de "marcos de pensamiento como prompts" (la más grande que encontramos tiene unas 1,7 mil estrellas; véase [`research/novelty.md`](research/novelty.md)). Le dan al agente una lista de verificación. La regla de Clarent es más estricta: **todo método debe tener un núcleo determinista**, algo que el código calcula o rechaza sin ningún LLM de por medio, además de disciplina con la evidencia:

- el agente **propone**, el motor **puntúa, valida y puede decir que no**;
- todo hecho observado necesita un `ref` (el comando, el `archivo:línea` o el registro que lo produjo);
- los informes dicen lo que son: una puntuación ACH es un *ranking de inconsistencias*, nunca una probabilidad.

## Demostración<!-- id: demo -->

Todo lo que sigue es la salida real del comando mostrado, sobre los ejemplos sintéticos incluidos en [`methods/`](methods/). Los archivos de [`docs/demo/`](docs/demo/) contienen las salidas completas y se regeneran con `python tools/gen_demo.py` (el CI falla si se desincronizan).

### `ach` — depurar con hipótesis en competencia<!-- id: demo-ach -->

Una prueba, `test_checkout_total`, falla más o menos 1 de cada 8 ejecuciones en el CI. Cinco causas rivales y una comodín, cinco piezas de evidencia, cada una evaluada contra *todas* las hipótesis:

```console
$ clarent ach score methods/ach/examples/flaky-test.json
```

Extracto (el informe completo incluye además la matriz de evidencia, el poder discriminante, la sensibilidad y las advertencias; véase [`docs/demo/ach-score.md`](docs/demo/ach-score.md)):

```markdown
## Conclusion

- Tie: several hypotheses share the lowest inconsistency score.
- Leader(s): H1, H5 (margin over the next: 21)
- This is a ranking of inconsistencies, **not a probability**.

## Hypothesis ranking (lower inconsistency = better)

| # | Hypothesis | Inconsistency | State | Contradicted by |
|---|-----------|---------------:|--------|-----------------|
| 1 | **H1** Race condition between xdist workers on a session-scoped fixture | 0 | alive | — |
| 1 | **H5** Leftover DB state from another test that ran earlier on the same worker | 0 | alive | — |
| 1 | **H6** Something else I am not considering | 0 | catch-all | — |
| 2 | **H2** Clock/timezone dependence (datetime.now near a day boundary) | 21 | refuted | E2, E1 |
| 3 | **H3** Real, unmocked network call that sometimes answers slowly or errors | 27 | refuted | E4, E1 |
| 4 | **H4** Non-deterministic set/dict ordering (PYTHONHASHSEED) changes a float sum | 33 | refuted | E3, E1, E5 |
```

Las causas de reloj, red y semilla de hash quedan refutadas por evidencia citada; dos causas empatan. ¿Qué experimento único las separa?

```console
$ clarent ach next methods/ach/examples/flaky-test.json
T1  priority=36.0  for=H5  against=H1
    Reproducing serially with the same random order as the failure (pytest-randomly --randomly-seed=<seed of run #8812>) also fails
T2  priority=9.0  for=H1  against=-
    Changing the fixture from scope=session to scope=function removes the failures in 200 runs with '-n 4'
```

### `redteam` — atacar un diseño o un PR; el motor rechaza lo que no puede anclar<!-- id: demo-redteam -->

Un documento de diseño sintético mueve las notificaciones de un cron job a un consumidor de streams ([`design.md`](methods/redteam/examples/design-doc/design.md)). Un modelo propone supuestos y ataques como JSON, cada uno citando el pasaje en el que se apoya; el motor los contrasta con el texto:

```console
$ clarent redteam check methods/redteam/examples/design-doc/findings.json
```

Extracto (el informe completo incluye además la matriz de supuestos, qué verificar a continuación, la cobertura por clase y las advertencias; véase [`docs/demo/redteam-check.md`](docs/demo/redteam-check.md)):

```markdown
## Top 3 attacks by impact

| # | Attack | Class | Assumption | Risk | Where | How to check |
|--:|---|---|---|---|---|---|
| 1 | **X3** After the rollout there is no way back: the flag cannot bring back the cron job or the sent_at column, so a bad release can only be fixed by shipping another one while notifications are being lost. | Reversibility | A5 (contradicted) | 25 (S1) | `design.md:26` | Apply the migration in staging, then try to revert to the previous release and send a notification. |
| 2 | **X1** If Redis is down when the API publishes, the row stays in the table but nothing reads it once the cron job is gone: those notifications are never sent and nobody is told. | Failure modes | A1 (contradicted) | 20 (S1) | `design.md:19` | Stop Redis in staging, create 20 notifications, restart Redis and count how many are sent. |
| 3 | **X2** A consumer that crashes after the read and before the provider answers loses the notification: acknowledging on read gives at-most-once delivery, and the row stays pending for ever. | Failure modes | A6 (unverified) | 16 (S2) | `design.md:14` | In staging, kill -9 a consumer between the read and the provider call; count the rows still pending after 10 minutes. |
```

`Where` es la línea del diseño que cita el ataque; `contradicted` significa que el supuesto se comprobó y la evidencia dice que es falso (aquí, `design.md:15` elimina al único lector de la tabla), lo que aumenta la plausibilidad de todo ataque que depende de él. X2 se apoya en un supuesto *no verificado*, por eso el informe lo lista primero en "Verify next".

El mismo diseño con hallazgos que el motor debe rechazar (una cita inventada, "verified" sin evidencia, una referencia a una línea que no existe, un duplicado, un ataque sin forma de comprobarlo) termina con código 1 y explica por qué:

```console
$ clarent redteam check methods/redteam/examples/design-doc/findings.rejected.json
```

```markdown
## Rejected findings

| Kind | ID | Reason |
|---|---|---|
| assumption | A3 | the quote does not appear in the target (compared literally, ignoring only whitespace) |
| assumption | A4 | status 'verified' needs at least one evidence item with a ref and an observation |
| assumption | A5 | evidence ref 'design.md:99' is not valid: line out of range (the file has 27 lines) |
| attack | X3 | its assumption A3 was rejected |
| attack | X4 | the quote has 5 characters; at least 12 are required to anchor a finding |
| attack | X5 | duplicate of X2 (same class and assumption, near-identical text) |
| attack | X6 | no 'check': say how to verify this attack (a command or a concrete question) |
| attack | X7 | its assumption A4 was rejected |
| attack | X8 | its assumption A5 was rejected |
```

El motor demuestra que un hallazgo está anclado y respaldado, no que sea correcto. También funciona con PRs (descripción más `gh pr diff`): [`docs/demo/redteam-pr.md`](docs/demo/redteam-pr.md).

### `triz-matrix` — un compromiso de diseño, resuelto contra la tabla de 1973<!-- id: demo-triz -->

"Hacer `/search` más rápido sin hacer el sistema más difícil de operar":

```console
$ clarent triz-matrix lookup latency "Device complexity"
```

```markdown
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
```

El informe continúa con un recordatorio de que los principios son estímulos para generar ideas, no soluciones, y con la celda inversa. `triz-matrix analyze methods/triz-matrix/examples/search-api.json` hace lo mismo para varias contradicciones a la vez y ordena los principios que se repiten ([`docs/demo/triz-analyze.md`](docs/demo/triz-analyze.md)). Los nombres ambiguos se rechazan listando los candidatos, nunca se adivinan.

### En Claude Code<!-- id: claude-code -->

```text
/clarent-methods:ach test_checkout_total fails ~1 in 8 CI runs
/clarent-methods:redteam docs/adr-014-event-sourcing.md
/clarent-methods:triz-matrix make /search faster without making it harder to run
```

Las skills son solo manuales (`disable-model-invocation`), así que no consumen contexto hasta que las invocas. `ach` hace que el agente liste primero las causas rivales, reúna evidencia ejecutando comandos, evalúe cada elemento contra *todas* las hipótesis y vuelva a puntuar hasta que sobreviva una explicación o el diagnóstico se declare sin resolver.

## Métodos<!-- id: methods -->

| Método | Herramienta | Estado |
|--------|------|--------|
| Análisis de Hipótesis Competidoras (Heuer, CIA) | `ach` | **implementado** (referencia) |
| Red Teaming (UFMCS) | `redteam` | **implementado** (beta) |
| Matriz de contradicciones TRIZ (Altshuller) | `triz-matrix` | **implementado** (beta); método adicional, fuera del ranking de los 10 primeros |
| Control Estadístico de Procesos (Shewhart) en el CI | `spc` | especificación |
| Intención del Comandante / Mission Command | `intent` | especificación |
| Pronóstico por clase de referencia | `rcf` | especificación |
| Kepner-Tregoe ES / NO ES | `kt` | especificación |
| Catecismo de Heilmeier | `gate` | especificación |
| Análisis de Árbol de Fallos | `fta` | especificación |
| HAZOP (palabras guía sobre APIs y flujos de datos) | `hazop` | especificación |
| Revisión Posterior a la Acción (US Army TC 25-20) | `aar` | especificación |
| FMEA, STAMP / STPA | `fmea`, `stpa` | pospuesto a la v2 |

El ranking es juicio del autor, no una medición; las puntuaciones, los criterios y las correcciones hechas en el camino están en [`research/ranking.md`](research/ranking.md). Se catalogaron 63 métodos, cada fuente marcada como `read / exists / blocked / unverified`: [`research/`](research/).

## Lo que no afirmamos<!-- id: no-claims -->

- Que una skill haga que un agente resuelva más tareas. gstack (uno de los repos más grandes de este espacio) publica en su README un resultado nulo en su propio benchmark de corrección de errores; publicaremos el nuestro, sea nulo o no.
- Que los números sean de Heuer, de Shewhart o de Goldratt. Cuando una constante es nuestra (pesos, umbrales), la ficha del método lo dice.
- Que todas las fuentes del catálogo estén verificadas. Cada una lleva su nivel de verificación.
- Que los datos de la matriz TRIZ tengan una cadena de titularidad limpia. Sus licencias y vacíos están escritos en [`DATA_LICENSE.md`](methods/triz-matrix/clarent_triz/data/DATA_LICENSE.md); 29 de sus 1 248 celdas son discutidas entre transcripciones, y puedes aportar tu propia matriz con `--data`.
- Que las demostraciones sean incidentes reales. Los ejemplos son sintéticos y están rotulados como tales.
- Que los métodos especificados existan. `spc`, `intent`, `rcf`, `kt`, `gate`, `fta`, `hazop` y `aar` son especificaciones; no se promete nada sobre cuándo estarán disponibles.
- Que los hallazgos del red team sean correctos. El motor rechaza los hallazgos que no están citados del texto o no están respaldados por evidencia; decidir si un ataque es acertado sigue siendo un juicio. Tres de sus seis clases de ataque (`scale`, `dependency`, `reversibility`) son propias de Clarent y no están en el manual de UFMCS en el que se basa.
- Que funcione en agentes distintos de Claude Code. El plugin está validado con `claude plugin validate`; Cursor, Codex y otros no se han probado.
- Que el ranking de métodos sea una medición, ni que sus hallazgos de "no existe un repo equivalente" sean prueba de ausencia: son cotas inferiores obtenidas de búsquedas en GitHub.

## Contribuir<!-- id: contributing -->

Un método nuevo es una carpeta, una ficha, un motor, pruebas y un ejemplo. Empieza por [`CONTRIBUTING.md`](CONTRIBUTING.md); `clarent doctor` te dice qué falta.

## Licencia<!-- id: license -->

Apache-2.0. Véase [`LICENSE`](LICENSE).
