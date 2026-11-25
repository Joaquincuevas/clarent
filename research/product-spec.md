# Especificación de producto — top 10 de v1 (revisado el 2026-11-25)

Principio rector: **cada herramienta = (1) un motor determinista que calcula o valida algo + (2) un envoltorio de agente que reúne evidencia y hace el juicio + (3) un reporte auditable.** El LLM propone y cita; el motor comprueba, puntúa y puede *rechazar*. Si una herramienta no puede rechazar nada de forma determinista, no entra a Clarent como herramienta (se queda como prompt en una colección).

> Estado: `ach` (`methods/ach/`), `redteam` (`methods/redteam/`, beta) y `triz-matrix` (`methods/triz-matrix/`, método adicional fuera del ranking) están **implementadas**. Las otras siete del top 10 (`spc`, `intent`, `rcf`, `kt`, `gate`, `fta`, `hazop`) y `aar` (plaza 10, §10) son especificaciones. `fmea` y `stpa` pasaron a v2. Los esfuerzos son estimaciones mías para una persona.

## 1. `ach` — Hipótesis competidoras (+ Key Assumptions Check) · ✅ implementada

| | |
|--|--|
| **Para qué** | Debugging/incidentes con varias causas plausibles; evitar el anclaje en la primera hipótesis. |
| **Forma** | CLI `clarent ach {init,validate,score,next}`; skill `/clarent-methods:ach`; MCP `clarent_ach_score`. |
| **Input** | JSON: hipótesis (una marcada `catch_all`), evidencias `observed` (con `ref`, credibilidad, relevancia, ratings `CC/C/N/I/II` por hipótesis) y pruebas `proposed` (ratings = predicciones). |
| **Motor** | Puntaje = Σ peso × penalización(I=1, II=2); la evidencia consistente **no suma**; diagnosticidad (spread por evidencia: *diagnostic / supports-only / non-diagnostic*); sensibilidad (¿quitar esta evidencia cambia al líder?); selección de la próxima prueba = spread entre hipótesis vivas × peso / costo; comodín nunca lidera pero se advierte. |
| **Output** | Reporte `.md`/`.json`: ranking, matriz, diagnosticidad, sensibilidad, próxima prueba, advertencias. |
| **Protocolo del skill** | (1) listar supuestos (KAC) y ≥ 4 hipótesis + comodín antes de mirar evidencia; (2) reunir evidencia **ejecutando comandos**, citando `ref`; (3) calificar **por evidencia contra todas las hipótesis** (no hipótesis por hipótesis, para no anclar); (4) `score`; (5) ejecutar la prueba #1 de `next`; (6) repetir. |
| **Ejemplo (3 líneas)** | `Tests flaky en CI` → `/clarent-methods:ach test_checkout_total falla 1/8` → el agente propone 5 causas, corre `pytest -n 0` ×60 y `-n 4` ×40, `score` descarta reloj/red/hash-seed y recomienda como siguiente prueba reproducir con la semilla del fallo. |
| **Aceptación** | `python -m unittest discover -s methods/ach/tests` verde; ejemplo `examples/flaky-test.json` produce líderes H1,H5 y prueba T1 primero. |
| **Limitaciones** | Pesos y umbral son parametrización de Clarent (no de Heuer); depende de que las calificaciones sean honestas. El ejemplo es **sintético**. |
| **Esfuerzo restante** | Hook `PostToolUse` opcional, MCP, y un eval en 10 bugs reales (1 semana). |

## 2. `redteam` — Ataque a diseños y PRs con catálogo fijo · ✅ implementada (beta)

> Implementada el 2026-11-25 en `methods/redteam/` (82 pruebas con los ejemplos y la integración con el núcleo). Esta sección describe lo que **hay**; difiere de la especificación original (lentes como archivos, subagente, modo Team A/Team B) en lo indicado en *Pendiente*.

| | |
|--|--|
| **Para qué** | Atacar un documento de diseño, un ADR o un PR (descripción + diff) antes de comprometerse, de modo que cada hallazgo quede **anclado en el texto** y **respaldado**. |
| **Forma** | CLI `clarent redteam {init,validate,check,top,catalog}`; skill `/clarent-methods:redteam <ruta\|PR#>`; `check --fail-on S1..S4` y `--strict` para CI. |
| **Input** | `findings.json` (`schema: "clarent.redteam/1"`): `target.files` (`kind: design\|pr`; para un PR, la descripción y un `gh pr diff` guardado), `root`, `assumptions[]` (`id, text, quote, status: verified\|unverified\|contradicted, evidence[{ref, observation}], check`), `attacks[]` (`id, class, assumption, quote, attack, impact 1–5, plausibility 1–5, check, evidence`) y `skipped_classes[{class, reason}]`. |
| **Catálogo fijo** | Seis clases: `key-assumptions`, `failure-modes`, `abuse`, `scale`, `dependency`, `reversibility`. Las tres primeras aplican técnicas del *Red Team Handbook* de UFMCS (leídas: Key Assumptions Check pp. 151–152, Pre-mortem pp. 138–140, What If? pp. 166–167, Red Team Analysis pp. 173–174); **`scale`, `dependency` y `reversibility` son aportes de Clarent** sin técnica equivalente en el Handbook. Cada clase se aplica o se omite con motivo. |
| **Motor determinista** | (1) **Ancla**: la `quote` debe aparecer literalmente en el objetivo (se ignora solo la diferencia de espacios en blanco; mínimo 12 caracteres; en un diff, también sin los marcadores `+`/`-`); sin cita, cita corta o ausente → **rechazado**. (2) **Respalda**: `verified`/`contradicted` exigen evidencia; un `ref` `archivo:línea` debe existir bajo la raíz; un ref libre (comando, log) solo se exige no vacío. (3) **Cascada y duplicados**: un ataque sobre un supuesto rechazado se rechaza; sin `check` se rechaza; mismo texto (Jaccard ≥ 0.8) en la misma clase y supuesto cuenta una vez. (4) **Puntúa**: `riesgo = impacto × plausibilidad efectiva`; `contradicted` → 5, `verified` → máximo 2, `unverified` → lo calificado; severidad S1 ≥ 20, S2 ≥ 12, S3 ≥ 6, S4 el resto. (5) **Reporta**: matriz de supuestos (supuesto × clase, con estado y evidencia), los 3 ataques principales, qué verificar a continuación, cobertura de las 6 clases, rechazos y advertencias. |
| **Output** | Markdown o `--format json` (`clarent.redteam.report/1`); códigos de salida 0 / 1 (rechazo, `--fail-on`, `--strict`) / 2 (entrada inválida). |
| **Demo** | `docs/demo/redteam-check.md`, `redteam-pr.md` y `redteam-rejected.md`, generados por `tools/gen_demo.py`. |
| **Limitaciones** | El motor prueba que un hallazgo está anclado y respaldado, **no que sea correcto**; los refs libres no se ejecutan; las constantes (clases, 12 caracteres, 0.8, escalas, bandas de severidad) son de Clarent y no están calibradas. Ver `methods/redteam/CARD.md`. |
| **Pendiente** | Modo Team A / Team B (dos corridas independientes y reporte de desacuerdos), subagente de contexto aislado, Action que ejecute `check --fail-on` en PRs, y un eval en 10 diseños o PRs reales (ver la ficha). |
| **Esfuerzo real** | Una sesión de trabajo larga, sin medir con rigor (la estimación original era 1 semana). |

## 3. `spc` — Cartas de control para CI y métricas de entrega

| | |
|--|--|
| **Para qué** | Saber si un cambio en duración de CI, tasa de flakes o lead time es **señal real** o ruido. |
| **Forma** | CLI `clarent spc chart`; GitHub Action programada; skill para interpretar. |
| **Input** | Serie temporal (CSV/JSON con `timestamp`, `value`) o `--from-gh-runs <workflow>` (usa `gh run list --json`). Para proporciones (tasa de flake): `failed`, `total` por periodo. |
| **Motor** | Carta XmR (individuales y rango móvil): línea central = media; límites = media ± 2.66 × promedio del rango móvil (2.66 = 3/1.128, constante estándar de XmR). Reglas de detección tipo Western Electric (punto fuera de 3σ; 2 de 3 fuera de 2σ del mismo lado; 4 de 5 fuera de 1σ del mismo lado; 8 seguidos del mismo lado). Fuentes secundarias coinciden en esas cuatro reglas, pero una da 9 en la última y algunas intercambian el orden de las reglas 2 y 3 (no abrí el manual de 1956): **el largo de racha es configurable (por defecto 8) y el reporte nombra la regla por su definición, no por su número**). Carta p para proporciones con límites binomiales. Línea base configurable (`--baseline N`) y recalculo explícito tras un cambio confirmado. |
| **Output** | SVG/PNG (SVG generado sin dependencias) + lista de señales con ventana de commits candidata (`git log` entre el punto anterior y la señal). |
| **Ejemplo** | `clarent spc chart --from-gh-runs ci.yml --metric duration` → "señal regla 4 desde el run #3412: 8 corridas seguidas sobre la media (+3m10s); commits candidatos: a1b2c3..d4e5f6". |
| **Aceptación** | Test con series sintéticas con desplazamiento conocido: detecta la señal ≤ 3 puntos después y **no** alerta en ruido puro (tasa de falsa alarma medida en 1000 series simuladas con semilla fija). |
| **Riesgos** | Series autocorrelacionadas o no normales inflan falsas alarmas → advertir y ofrecer ventana mayor. |
| **Esfuerzo** | 1 semana. |

## 4. `intent` — Contrato de delegación (Commander's Intent / Mission Command)

| | |
|--|--|
| **Para qué** | Delegar a subagentes (o personas) con el *para qué* y los límites, no un guion de pasos; verificar que el resultado respeta la intención. |
| **Forma** | Formato `intent.md` (frontmatter YAML) + CLI `clarent intent {lint,verify}` + skill `/clarent-methods:intent` + hook `SubagentStop`. |
| **Formato** | `purpose` y `end_state` (condición **observable**; los dos elementos que define ADP 6-0, 2012 📖) y, como añadidos propios de Clarent, `key_tasks` (opcional), `constraints.allowed_paths/forbidden_paths/must/must_not`, `freedom` (qué puede decidir sin preguntar), `stop_conditions` (cuándo volver a preguntar), `verification` (comandos). |
| **Motor** | `lint`: campos obligatorios; `end_state` debe contener un criterio comprobable (un comando en `verification` o un predicado); señal de microgestión (≥ 4 pasos numerados en `key_tasks` sin `purpose`); `stop_conditions` no vacío. `verify` (en `SubagentStop`): ejecuta `verification`, compara `git diff --name-only` con `allowed/forbidden_paths` y devuelve **exit 2** (el hook de Claude Code mantiene al subagente trabajando) con un informe de "deriva de intención". |
| **Ejemplo** | `/clarent-methods:intent "migrar el cliente HTTP a httpx"` → genera `intent.md` con `forbidden_paths: [infra/**]`; al terminar el subagente, `verify` detecta un cambio en `infra/terraform/…` y lo devuelve a corregir. |
| **Aceptación** | Test del lint (casos válidos/ inválidos); test de `verify` con repo git temporal y diff fuera de rutas permitidas. |
| **Riesgos** | Formato demasiado pesado para tareas triviales → plantilla mínima de 4 campos obligatorios y el resto opcional. |
| **Esfuerzo** | 1–1.5 semanas. |

## 5. `rcf` — Estimar con tu propio historial (Reference Class Forecasting)

| | |
|--|--|
| **Para qué** | Responder "¿cuánto tardará esto?" con la distribución de trabajos similares de **este** repo, y registrar el pronóstico para calibrarlo. |
| **Forma** | CLI `clarent rcf {build,forecast,log,score}`; skill `/clarent-methods:rcf`. |
| **Input** | Repo (git log) y opcionalmente PRs de `gh`. Objetivo: texto + rutas esperadas + etiquetas + tamaño estimado. |
| **Motor** | (1) *Clase de referencia*: PRs pasados con similitud por solapamiento de directorios (Jaccard), etiqueta y banda de tamaño (líneas cambiadas). (2) Tiempo = primer commit → merge. (3) Cuantiles empíricos P50/P80/P90 con intervalo bootstrap. (4) **Se niega** si la clase tiene < 10 elementos. (5) Muestra la **vista externa primero** y registra el ajuste de la vista interna por separado. (6) `log` guarda el pronóstico; `score` calcula calibración (pinball loss / cobertura de intervalos) cuando el trabajo termina. |
| **Ejemplo** | `/clarent-methods:rcf "agregar paginación a /orders"` → "Clase: 23 PRs similares. P50 2.9 d, P80 6.1 d, P90 11 d. Tu estimación interna (1 d) cae bajo el P10 de la clase." |
| **Aceptación** | Test con historial git sintético generado con semilla; se niega con n < 10; reproducibilidad. |
| **Riesgos** | Tiempo de PR ≠ esfuerzo; squash/rebase distorsiona fechas; bots. Se documenta y se permite excluir autores/etiquetas. |
| **Esfuerzo** | 1 semana. |

## 6. `kt` — IS / IS-NOT diferencial sobre corridas de CI

| | |
|--|--|
| **Para qué** | Convertir "falla a veces" en una **especificación**: dónde/cuándo/cuánto ocurre y dónde no, y qué distingue a ambos. |
| **Forma** | CLI `clarent kt analyze`; skill `/clarent-methods:kt`; puente `clarent kt to-ach` que siembra hipótesis y evidencia de ACH. |
| **Input** | Tabla de corridas (CSV/JSON o `--from-gh-runs`): `outcome` + dimensiones (`os`, `python`, `shard`, `runner_image`, `branch`, `hour`, `weekday`, `test_position`, `author`…). |
| **Motor** | Para cada valor de cada dimensión: tasa de fallo, riesgo relativo y **test exacto de Fisher** (implementado con `math.comb`); corrección por comparaciones múltiples (Holm); **se niega a señalar** valores con n < mínimo. Salida estilo KT: *QUÉ/DÓNDE/CUÁNDO/MAGNITUD* en columnas **ES / NO ES**, lista de **distinciones** (solo del lado ES), y para cada distinción la primera aparición (cambios). Regla KT: una causa candidata debe explicar *toda* la especificación (checklist en el reporte). |
| **Ejemplo** | `clarent kt analyze runs.csv --outcome failed` → "Falla 14/15 en `shard=3 ∧ runner_image=2026-11-02`; 0/200 en el resto. Distinción: imagen nueva del runner (cambio: 2026-11-02)." |
| **Aceptación** | Test con datos sintéticos con una causa conocida y dimensiones de ruido: recupera la dimensión correcta y **no** reporta distinciones en ruido puro (semilla fija). |
| **Riesgos** | Confusores y colinealidad; se advierte que son *distinciones*, no causas. |
| **Esfuerzo** | 1 semana. |

## 7. `gate` — Puerta de propuesta (Catecismo de Heilmeier)

| | |
|--|--|
| **Para qué** | Que un PR/RFC no avance sin responder las ocho preguntas de DARPA. |
| **Preguntas** (📖 de la página de DARPA) | 1 Qué intentas hacer, sin jerga · 2 Cómo se hace hoy y límites · 3 Qué es nuevo y por qué funcionará · 4 Quién se beneficia y qué cambia · 5 Riesgos · 6 Costo · 7 Duración · 8 Exámenes intermedios/finales de éxito. |
| **Forma** | CLI `clarent gate check <archivo.md>`; GitHub Action que comenta el PR; skill que ayuda a redactar. |
| **Motor** | Parseo por encabezados; cada pregunta debe tener respuesta; heurísticas **deterministas y explicables**: P1 con densidad alta de identificadores/siglas → "jerga"; P6/P7 deben contener cifras con unidad; P8 debe contener un criterio comprobable (comando, métrica o umbral). Salida: aprobado/pendiente por pregunta con la razón. |
| **Ejemplo** | PR "Migrar a Kafka" → `gate`: "P7 sin duración; P8 sin criterio medible" → etiqueta `needs-gate`. |
| **Aceptación** | Test de cada heurística con casos que pasan y que fallan. |
| **Riesgos** | Heurísticas ruidosas → siempre muestran el motivo y permiten `<!-- gate: ignore Q6 reason -->`. |
| **Esfuerzo** | 3–4 días. |

## 8. `fta` — Árbol de fallas desde incidentes, con conjuntos mínimos de corte

| | |
|--|--|
| **Para qué** | Pasar de la línea de tiempo de un incidente a **qué combinaciones mínimas de fallos** provocan el evento tope; detectar puntos únicos de falla. |
| **Forma** | CLI `clarent fta {validate,cutsets,render}`; skill `/clarent-methods:fta <incidente>`. |
| **Input** | `tree.json`: evento tope; compuertas AND/OR; eventos básicos con `ref` (log, métrica, commit) y probabilidad opcional. |
| **Motor** | Valida (acíclico, aridad, sin eventos sin desarrollar ocultos); calcula **conjuntos mínimos de corte** por expansión top-down con absorción (algoritmo clásico de FTA, p. ej. tipo MOCUS); lista **SPOF** (cortes de tamaño 1); si hay probabilidades, cota superior de min-cut y medida de importancia. Render Mermaid. |
| **Referencia** | NASA *Fault Tree Handbook v1.1* ✅. |
| **Ejemplo** | `/clarent-methods:fta INC-2210` → "evento tope: checkout 500; 3 conjuntos mínimos; SPOF: `config-server timeout` (sin caché)." |
| **Aceptación** | Árboles de libro con cortes conocidos; propiedad: ningún corte es subconjunto de otro. |
| **Riesgos** | El árbol lo construye el LLM: cada evento básico exige `ref`. |
| **Esfuerzo** | 1 semana. |

> Reincorporada al top 10 el 2026-11-25 por puntaje (3.67); había pasado a v2 el 2026-11-24 al ceder su plaza a `triz-matrix`.

## 9. `hazop` — Palabras guía sobre APIs y flujos de datos

> Estado: **solo especificación** (re-puntuada el 2026-11-25: 3.58, puesto 11 de 63; entra al top 10 por desempate de novedad). Los esfuerzos y los ejemplos son estimaciones mías, sin medir. Las palabras guía y su aplicabilidad a software son adaptación de Clarent: **no se han contrastado con la norma IEC 61882** (nivel `unverified`); verificarlas antes de publicar la ficha.

| | |
|--|--|
| **Para qué** | Revisar sistemáticamente un diseño de API o un flujo de datos por **desviaciones** de su intención: aplicar cada palabra guía a cada parámetro de cada nodo y no dejar celdas sin examinar. Complementa a `redteam` (que ataca supuestos expresados en un documento): HAZOP recorre una **rejilla exhaustiva** que el motor puede comprobar. |
| **Origen del método** | Revisión de procesos industriales con palabras guía (ICI, años 60; Kletz, *Hazop and Hazan*, 1983 ✅ catálogo X10). El catálogo anota que las fuentes discrepan sobre cuánto se debe a Kletz. |
| **Forma** | CLI `clarent hazop {scaffold,validate,matrix,report}`; skill `/clarent-methods:hazop <openapi.json\|flujo>`; palabras guía como datos (`guidewords/<id>.json`), una por archivo. |
| **Input** | `hazop.json` (`schema: "clarent.hazop/1"`): `nodes[]` (un endpoint, un tópico/cola, un paso de un pipeline o una llamada entre servicios), cada nodo con `intention` (qué debe ocurrir, en una frase) y `parameters[]` (`payload`, un campo concreto, `order`, `rate`, `latency`, `auth`, `idempotency`, `version`, …). Opcional: un OpenAPI **en JSON** para `scaffold` (YAML queda fuera para mantener la biblioteca estándar). |
| **Palabras guía (por defecto)** | `no/none`, `more`, `less`, `as-well-as`, `part-of`, `reverse`, `other-than`, y de tiempo/orden `early`, `late`, `before`, `after`. Es la lista clásica de HAZOP **según mi lectura de fuentes secundarias**; no se abrió la norma. Un equipo puede añadir o quitar palabras con un archivo. |
| **Motor determinista** | (a) `scaffold`: del OpenAPI genera nodos (operación = método + ruta) y parámetros (cada parámetro de ruta/consulta/cabecera, cada propiedad de primer nivel del cuerpo y de las respuestas) con la intención vacía; **no inventa causas ni consecuencias**. (b) `matrix`: producto nodo × parámetro × palabra guía; **cada celda debe resolverse** como `deviation` o `not-credible` (con motivo) o `n/a` (con motivo, según una tabla de aplicabilidad por tipo de parámetro que también es dato, p. ej. `reverse` no aplica a `latency`). Celdas `unanalyzed` → exit 1. (c) `validate`: toda `deviation` lleva ≥ 1 `cause` y ≥ 1 `consequence`; con severidad ≥ S2 exige `safeguard` o `action`; `safeguard.ref` de la forma `archivo:línea` debe existir en el repo; ids duplicados, nodos huérfanos y palabras guía desconocidas se rechazan. (d) `report`: tabla por nodo y lista de acciones abiertas ordenadas por severidad; con `--fail-on S1` exit 1. |
| **Qué hace el agente** | Propone intención, desviaciones, causas y consecuencias con la **evidencia que encuentra en el código** (el handler, el esquema, los reintentos del cliente), citando `archivo:línea`. El motor no juzga si una desviación es creíble; exige que la rejilla esté completa y que lo afirmado tenga referencia. |
| **Output** | `hazop.md` (una tabla por nodo: `parámetro · palabra guía · desviación · causas · consecuencias · salvaguardas · acción · severidad`) y `hazop.json`. |
| **Ejemplo (hipotético; aún no implementado)** | `/clarent-methods:hazop openapi/orders.json` → 4 nodos, 9 parámetros, 90 celdas; 83 resueltas, 7 `unanalyzed` (exit 1). Una desviación: `POST /orders` · `idempotency-key` · `no` → "reintento del cliente crea un pedido duplicado" (S2) sin salvaguarda en `src/orders/create.py` → acción abierta. |
| **Aceptación** | Fixture OpenAPI pequeño con rejilla completa y esperada (conteo exacto de celdas); celda sin resolver → exit 1; `safeguard.ref` inexistente → rechazo; `n/a` sin motivo → rechazo; palabra guía añadida por archivo aparece en la rejilla; reproducibilidad del orden. |
| **Riesgos** | Explosión combinatoria (10 palabras × muchos parámetros) → `scaffold --params-per-node N`, tabla de aplicabilidad que marca `n/a` por defecto lo evidentemente inaplicable y agrupación por tipo; sesgo del LLM hacia desviaciones genéricas → exigir `ref` y causa concreta; la analogía de proceso industrial a software es **adaptación nuestra**, no una práctica estandarizada. |
| **Esfuerzo** | 1 semana (estimación mía). Contribución típica: una palabra guía o una regla de aplicabilidad = un archivo. |

## 10. `aar` — After Action Review desde git, CI e incidentes

> Estado: **solo especificación** (plaza 10 por decisión del autor, 2026-11-25; M04, 3.58). Los esfuerzos y el ejemplo son estimaciones mías, sin medir. **Fuente leída:** TC 25-20, *A Leader's Guide to After-Action Reviews* (Departamento del Ejército de EE. UU., 30 sept. 1993), <http://www.victoryprinciples.com/wp-content/uploads/2009/07/tc-25-20-ldrs-guide-aars.pdf> (`read`: capítulo 1, Figura 1-2 *AAR Format*, Figura 4-1 *Sequence for Conducting AARs* y las secciones *Commander's Mission and Intent (What Was Supposed to Happen)*, *Summary of Recent Events (What Happened)*, *Discussion of Key Issues* y *Tasks to Sustain/Improve*). Del informe de Morrison y Meliza (ARI, 1999) que cita el catálogo solo consta que existe; no se abrió.

| | |
|--|--|
| **Para qué** | Después de un despliegue, una migración, un incidente o un sprint, producir un AAR **con evidencia**: qué se esperaba, qué ocurrió, por qué difieren y qué conservar o mejorar. El método original lo define así: «una discusión profesional de un evento […] que permite descubrir qué pasó, por qué pasó y cómo sostener fortalezas y mejorar debilidades»; el propio manual aclara que **no es una crítica** y que no califica éxito o fracaso. |
| **Forma** | CLI `clarent aar {init,collect,validate,report,followup}`; skill `/clarent-methods:aar <evento>`. |
| **Estructura (las cuatro preguntas)** | 1 *Lo planeado*: expectativas observables (la «intención» de TC 25-20). 2 *Lo ocurrido*: observaciones con fuente. 3 *Diferencia y causa*: por cada expectativa, veredicto y, si falló o no estaba planeado, su causa con evidencia. 4 *Sostener / mejorar*: acciones con responsable, fecha y verificación. |
| **Input** | `aar.json` (`schema: "clarent.aar/1"`) con: `event` (`id, title, kind: release\|incident\|migration\|sprint, window {from, to}`); `expectations[]` (`id, text, source` —un ADR, un PR, un ticket—, y opcionalmente `metric {name, op, value, unit}`); `observations[]` (`id, text, at, source {kind: git\|ci\|incident\|manual, ref}, value`); `differences[]` (`expectation, observations, verdict`, y `cause {category: plan\|execution\|tooling\|environment\|unknown, text, evidence[]}`); `actions[]` (`id, kind: sustain\|improve, differences, text, owner, due, verification`). Insumos que `collect` convierte en observaciones: **`git log`** de la ventana (commits, fusiones, reversiones), **resultados de CI** (`gh run list --json` o un CSV/JSON equivalente) y un **JSON de incidente** (`clarent.incident/1`: `id, severity, started_at, detected_at, mitigated_at, resolved_at, impact, timeline[{at, text, ref}]`). |
| **Motor determinista** | (a) **Línea de tiempo**: fusiona commits, corridas de CI y eventos del incidente en orden y calcula los intervalos (tiempo hasta detectar, mitigar y resolver; del primer commit al despliegue; de la corrida fallida a la corrección). (b) **Plan contra realidad**: toda expectativa con `metric` recibe un veredicto calculado (`met`, `missed`, `exceeded`) con su diferencia; una expectativa **sin criterio observable** se marca `unassessed` y se advierte (no hay con qué compararla); lo ocurrido sin expectativa se lista como `unplanned`. (c) **Completitud**: todo `missed` y `unplanned` exige causa con ≥ 1 evidencia o `category: unknown` explícita; toda diferencia, ≥ 1 acción o un motivo de «sin acción»; toda acción, `owner`, `due` y `verification`; debe haber ≥ 1 acción `sustain` (el manual insiste en que siempre hay fortalezas que sostener y debilidades que mejorar). (d) **Referencias**: un SHA citado debe existir en el repositorio (`git cat-file -e`) y un `file:line` debe existir. (e) **Sin culpables (heurística)**: advierte si una causa o diferencia nombra a un autor de commit o a un respondedor del incidente tomado de los insumos. (f) `followup --on <fecha>`: lista acciones vencidas o sin verificar. |
| **Qué hace el agente** | Redacta expectativas observables a partir del ADR/PR de origen, propone causas y acciones citando evidencia del `collect`. El motor exige que lo comparable se compare, que cada causa tenga respaldo o diga que no lo tiene, y que ninguna acción quede sin dueño ni verificación. **No puntúa personas ni equipos.** |
| **Output** | `aar.md` con las cuatro secciones y la línea de tiempo (para pegar en un postmortem o en el PR) y `aar.json`; exit 1 si hay expectativas sin veredicto, causas sin respaldo o acciones incompletas. |
| **Relación con otras herramientas** | La pregunta «por qué» puede sembrar un análisis `ach` cuando hay varias causas plausibles; las series de CI son las mismas que usa `spc`; las expectativas con métrica pueden provenir de un contrato `intent`. |
| **Ejemplo (hipotético; aún no implementado)** | `clarent aar collect --since v2.3.0 --until v2.4.0 --ci ci-runs.json --incident INC-2210.json` → «Esperado: despliegue sin interrupción, p95 < 300 ms. Ocurrió: 14 commits, 2 corridas de CI fallidas, p95 410 ms (missed, +110 ms), 38 min hasta detectar. Causa propuesta: timeout sin caché (evidencia: `src/search.py:88`). Acciones: sostener rollback por flag (funcionó); mejorar alerta de p95 (dueño, fecha, verificación)». |
| **Aceptación** | Repo git temporal + CI y JSON de incidente fijos: orden y cálculo de la línea de tiempo; veredictos de métricas (`met`, `missed`, `exceeded`); expectativa sin métrica → `unassessed` con advertencia; `missed` sin causa → exit 1; SHA inexistente → rechazo; causa que nombra a un autor → advertencia; acción sin `verification` → rechazo; ningún `sustain` → advertencia; `followup` detecta una acción vencida. |
| **Riesgos** | `git log` es un mal proxy de «lo ocurrido» con squash y rebase (se documenta; las observaciones manuales son de primera clase); el CI vía `gh` requiere autenticación; los incidentes tienen formatos distintos (esquema mínimo + adaptadores en v1.1); la heurística de «sin culpables» da falsos positivos y negativos y solo advierte; **una herramienta no crea una cultura sin culpa**: el manual depende de un facilitador y de un clima de franqueza, y eso no se automatiza. |
| **Prior art** | `coopersimson96/aar-loop` (125★; AAR de sesiones de IA, no de equipos de software; no abierto). Re-escanear con consultas cortas antes de implementar. |
| **Esfuerzo** | 1–1.5 semanas (estimación mía). |

---

## Fuera del ranking: `triz-matrix` — Matriz de contradicciones de TRIZ con ejemplos de software · ✅ implementada

> **Decisión del autor (2026-11-24, ajustada el 2026-11-25):** método adicional **fuera del ranking**; no ocupa plaza del top 10. No es novedosa (hay ≥ 8 repos pequeños con la matriz; ver `novelty.md`); su aporte es el dataset verificado y el motor con tests.

| | |
|--|--|
| **Para qué** | Un diseño atascado entre dos propiedades (mejorar A empeora B): obtener los principios inventivos que la matriz clásica asocia al par, con ejemplos en software. |
| **Forma** | CLI `clarent triz-matrix {lookup,rank,analyze,params,principles,info,init}`; skill `/clarent-methods:triz-matrix`; datos propios con `--data DIR`. |
| **Input** | Par (mejora, empeora) como número, nombre (en/es) o palabra de software (`latency`); o un JSON con varios pares (`examples/search-api.json`). Lo ambiguo se rechaza listando candidatos, nunca se adivina. |
| **Motor** | Resolución de nombres (número → nombre exacto o alias → subcadena única → lectura en software única); búsqueda de la celda; **estado de la celda** (`verified` = el consenso de 5 transcripciones iguala la tabla de 1973; `contested` = difiere, se muestran ambas lecturas; `consensus` = la página de 1973 no se pudo leer); mismo parámetro en ambos lados = contradicción física (la matriz no aplica); celda vacía + celda inversa; `rank` = principios ordenados por cuántas contradicciones los listan. Todo determinista. |
| **Dataset** | `tools/triz_crosscheck.py` reconstruye `matrix.json`: mayoría estricta entre 5 transcripciones MIT, comparada celda a celda con la tabla de 1973 de la Fundación Altshuller. Resultado: **1 248 celdas con principios; 1 218 verificadas, 29 en disputa, 1 solo por consenso**. Procedencia y límites de licencia: `clarent_triz/data/DATA_LICENSE.md`. |
| **Output** | Markdown o JSON (`--format json`): principios con descripción y ejemplo de software, estado de la celda, celda inversa; para varios pares, ranking de principios. `--lang es` para español. |
| **Ejemplo (3 líneas)** | `clarent triz-matrix lookup latency "Device complexity"` → *Speed* vs. *Device complexity* → principios 10, 28, 4, 34 (Acción previa, Sustitución de sistemas mecánicos, Asimetría, Descarte y regeneración), celda verificada. |
| **Aceptación** | 38 tests: integridad del catálogo (39 parámetros, 40 principios, en/es), celdas ancla, conteos de estado, procedencia (commits y hashes), resolución de nombres, ambigüedad, ranking, CLI, datos propios inválidos. |
| **Limitaciones** | La matriz es una heurística con erratas conocidas; 29 celdas en disputa; la cadena de titularidad previa a las transcripciones **no está establecida** (ver DATA_LICENSE.md); lecturas y ejemplos en software son adaptación de Clarent; no genera ni evalúa soluciones. |
| **Pendiente** | Comparar las 29 celdas en disputa con el libro (Altshuller, *40 Principles*, Shulyak y Rodman, 1997); decidir la licencia de datos con asesoría; ARIZ-85 (v2). |

## v2 — movidas desde el top 10 (decisión del autor, 2026-11-25)

> `fmea` y `stpa` salen del top 10 de v1 y pasan a v2. Las especificaciones se conservan tal cual estaban, con la numeración de la versión anterior.

### `fmea` — FMEA de un módulo de software

| | |
|--|--|
| **Para qué** | Lista priorizada de modos de falla de un módulo, con severidad, ocurrencia y detección **ancladas en datos del repo**. |
| **Forma** | CLI `clarent fmea {scaffold,score}`; skill `/clarent-methods:fmea <ruta>`. |
| **Input** | Ruta de módulo; opcional `coverage.xml`; historial de git. |
| **Motor** | `scaffold` (v1 Python vía `ast`): enumera funciones públicas, llamadas externas (red, FS, BD, subprocess), manejo de errores. **Ocurrencia** ← número de commits tipo *fix* que tocaron el archivo (`git log`); **Detección** ← cobertura de las líneas de la función (si hay `coverage.xml`) o existencia de tests que la referencian; **Severidad** ← la asigna el agente/humano con una rúbrica de 4 niveles (obligatoria y citada). Prioridad por reglas propias (no se copia la tabla AIAG-VDA): Severidad máxima siempre alta; si no, S×O×D con corte documentado, y se **advierte** las limitaciones conocidas de RPN. |
| **Output** | Tabla `modo de falla · efecto · causa · S · O · D · prioridad · acción recomendada · ref (archivo:línea)`, ordenada, en `.md` y `.csv`. |
| **Ejemplo** | `/clarent-methods:fmea src/payments/` → 14 modos de falla; los 3 de prioridad alta son llamadas a la pasarela sin timeout y con baja cobertura, ligados a líneas. |
| **Aceptación** | Test con módulo fixture: O y D se calculan de datos reales (git temporal, `coverage.xml` mínimo); modo de falla sin `ref` es rechazado. |
| **Riesgos** | Cobertura de líneas no es detección real; el reporte lo dice. TypeScript en v1.1. |
| **Esfuerzo** | 1.5 semanas. |

### `stpa` — Análisis de estructura de control (agentes y microservicios)

| | |
|--|--|
| **Para qué** | Revisar un sistema por *interacciones inseguras*, no solo por fallas de componentes: p. ej. un agente que puede ejecutar acciones, un orquestador de despliegues, un autoscaler. |
| **Forma** | CLI `clarent stpa {validate,uca,trace}`; skill `/clarent-methods:stpa`; render Mermaid. |
| **Pasos** (según el *STPA Handbook*, 2018 ✅) | 1) pérdidas y peligros; 2) estructura de control; 3) acciones de control inseguras (UCA); 4) escenarios de pérdida. |
| **Input** | `stpa.json`: `losses[]`, `hazards[]` (cada uno → pérdidas), `controllers[]`/`controlled_processes[]`, `control_actions[]` (de→a), `feedback[]`, `context_variables[]` por acción. |
| **Motor** | (a) valida la estructura: controladores sin feedback, acciones huérfanas, procesos sin controlador; (b) **genera la tabla de cobertura de UCA**: acción × {no proporcionada, proporcionada, fuera de tiempo/orden, duración incorrecta (solo continuas)} × contexto → cada celda debe quedar `unsafe/safe/n-a`; celdas `unanalyzed` → exit 1; (c) trazabilidad: toda UCA enlaza a ≥ 1 peligro, y todo peligro a ≥ 1 pérdida; (d) esqueleto de escenarios de pérdida en las 2 categorías del Handbook. El agente propone; el motor exige completitud y trazabilidad. |
| **Ejemplo** | `/clarent-methods:stpa deploy-controller.json` → 36 celdas UCA, 31 analizadas, 5 pendientes; UCA-7: "ordenar rollback *demasiado tarde* si el feedback de error-rate llega con 5 min de retraso". |
| **Aceptación** | Test: UCA huérfana, ciclo sin feedback y celda sin analizar se detectan; Mermaid válido. |
| **Riesgos** | Es el método más pesado; plantilla guiada y ejemplo canónico. Riesgo de burocracia: modo `--lite` solo pasos 2–3. |
| **Esfuerzo** | 2 semanas (apuesta de mayor novedad). |

---

## Plataforma compartida (no cuenta en el top 10, pero se necesita)

- **`clarent` router** (inspirado en Cynefin ✅): una skill de entrada que, dada la tarea, devuelve **un** método recomendado (o `NONE`), para no inundar el contexto. Competidor con router: `cc-thinking-skills` (ver novelty.md).
- **Registro de métodos** y **plantilla de "methodology card"** (ver `architecture.md`).
- **Arnés de evals** (`evals/`): una tarea con respuesta conocida por método, comparando con y sin el skill; se publica aunque el resultado sea nulo.
