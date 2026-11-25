# Scoring y selección del top 10 para v1

> Fuente de los puntajes: `research/data/scores.csv`. La tabla se regenera con `python tools/rank.py research/data/scores.csv`. **Los puntajes son juicio mío apoyado en la evidencia de `novelty.md`**; no son una medición. Cámbialos en el CSV y vuelve a generar.

## Criterios (1–5)

| Criterio | Pregunta | 5 | 1 |
|----------|----------|---|---|
| **N** Novedad (del *ángulo Clarent*: motor ejecutable + datos de dev) | ¿Existe ya algo bueno? | 0 repos, sin cobertura ni en colecciones | Saturado (≥ 1 repo dev, mantenido, ≥ 500★) |
| **U** Utilidad diaria para devs | ¿Se usa varias veces por semana? | a diario | casi nunca |
| **E** Facilidad de implementación | ¿MVP en ≤ 1 semana, sin datos/licencias difíciles? | 1–2 días | meses o requiere datos no libres |
| **V** Potencial viral / demo | ¿Se entiende en un GIF de 10 s? | imagen/gráfico que se comparte solo | explicación larga |
| **C** Facilidad de contribución | ¿Otros pueden añadir variantes (datos, reglas, personas) sin entender todo? | contribución = 1 archivo | requiere experto |

**Ponderado = (1.5·N + 1.5·U + E + V + C) / 6.** Se pesa más N y U porque el objetivo del autor es "implementar cosas NO comunes" y que se use a diario. Desempate: mayor N, luego mayor U.

## Tabla completa (63 metodologías)

| # | ID | Metodología | Familia | N | U | E | V | C | Σ | Ponderado | Estado en GitHub |
|--:|----|-------------|---------|--:|--:|--:|--:|--:|--:|----------:|------------------|
| 1 | D04 | ACH (Heuer) | Decision | 4 | 5 | 5 | 4 | 4 | 22 | **4.42** | existe pero debil |
| 2 | L12 | SPC (control charts) | Lean | 4 | 4 | 4 | 5 | 4 | 21 | **4.17** | existe pero abandonado |
| 3 | M07 | Commander's Intent | Militar | 4 | 5 | 4 | 4 | 3 | 20 | **4.08** | no existe |
| 4 | X06 | Reference Class Forecasting | Extra | 4 | 4 | 4 | 5 | 3 | 20 | **4.0** | no existe |
| 5 | E06 | Kepner-Tregoe (IS/IS-NOT) | Ingenieria | 3 | 5 | 4 | 4 | 3 | 19 | **3.83** | existe pero debil |
| 6 | M05 | Red Teaming (UFMCS) | Militar | 2 | 4 | 5 | 5 | 4 | 20 | **3.83** | existe pero debil |
| 7 | D05 | Key Assumptions Check | Decision | 3 | 4 | 5 | 3 | 4 | 19 | **3.75** | existe pero debil |
| 8 | X04 | Heilmeier Catechism | Extra | 3 | 4 | 5 | 3 | 4 | 19 | **3.75** | existe pero debil |
| 9 | E02 | Fault Tree Analysis | Ingenieria | 4 | 4 | 3 | 4 | 3 | 18 | **3.67** | existe pero debil |
| 10 | M02 | Auftragstaktik / Mission Command | Militar | 4 | 4 | 4 | 3 | 3 | 18 | **3.67** | no existe |
| 11 | X10 | HAZOP (guidewords) | Extra | 4 | 3 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 12 | D03 | Superforecasting / calibracion | Decision | 3 | 4 | 4 | 4 | 3 | 18 | **3.58** | existe pero debil |
| 13 | E01 | FMEA/FMECA | Ingenieria | 3 | 4 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 14 | M04 | After Action Review (AAR) | Militar | 3 | 4 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 15 | E04 | STAMP/STPA | Ingenieria | 4 | 4 | 3 | 3 | 3 | 17 | **3.5** | existe pero debil |
| 16 | X07 | Design Structure Matrix | Extra | 4 | 4 | 3 | 3 | 3 | 17 | **3.5** | existe pero debil |
| 17 | D01 | Delphi | Decision | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 18 | L03 | Andon | Lean | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 19 | M08 | CARVER | Militar | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 20 | E05 | Theory of Constraints / DBR | Ingenieria | 3 | 4 | 3 | 4 | 3 | 17 | **3.42** | existe pero debil |
| 21 | L01 | Jidoka | Lean | 3 | 4 | 4 | 3 | 3 | 17 | **3.42** | existe pero debil |
| 22 | L08 | A3 | Lean | 3 | 3 | 4 | 3 | 4 | 17 | **3.33** | existe pero debil |
| 23 | E07 | Cynefin | Ingenieria | 2 | 4 | 5 | 3 | 3 | 17 | **3.33** | existe pero debil |
| 24 | M06 | Pre-mortem (Klein) | Militar | 2 | 4 | 5 | 3 | 3 | 17 | **3.33** | bien cubierto |
| 25 | D07 | Analisis morfologico (Zwicky) | Decision | 4 | 3 | 3 | 3 | 3 | 16 | **3.25** | existe pero debil |
| 26 | L10 | SMED | Lean | 4 | 3 | 3 | 3 | 3 | 16 | **3.25** | no existe |
| 27 | M03 | MDMP | Militar | 4 | 3 | 3 | 3 | 3 | 16 | **3.25** | existe pero debil |
| 28 | M10 | Center of Gravity (CG-CC-CR-CV) | Militar | 4 | 3 | 3 | 3 | 3 | 16 | **3.25** | no existe |
| 29 | S02 | ARIZ-85 | Sovietica | 4 | 3 | 2 | 4 | 3 | 16 | **3.25** | existe pero debil |
| 30 | S04 | Leyes de evolucion de sistemas tecnicos | Sovietica | 4 | 3 | 2 | 4 | 3 | 16 | **3.25** | no existe |
| 31 | X11 | Bow-tie | Extra | 4 | 3 | 3 | 3 | 3 | 16 | **3.25** | existe pero debil |
| 32 | L05 | Genchi Genbutsu | Lean | 3 | 4 | 4 | 2 | 3 | 16 | **3.25** | existe pero debil |
| 33 | L07 | Ishikawa | Lean | 3 | 3 | 4 | 3 | 3 | 16 | **3.17** | existe pero debil |
| 34 | M09 | Wargaming (COA analysis) | Militar | 3 | 3 | 3 | 4 | 3 | 16 | **3.17** | existe pero debil |
| 35 | X09 | Matriz de Pugh | Extra | 3 | 3 | 5 | 2 | 3 | 16 | **3.17** | existe pero debil |
| 36 | X17 | Team A / Team B (CIA 1976) | Extra | 3 | 3 | 4 | 3 | 3 | 16 | **3.17** | existe pero debil |
| 37 | L02 | Poka-yoke | Lean | 2 | 4 | 4 | 3 | 3 | 16 | **3.17** | bien cubierto |
| 38 | D02 | Estimacion de Fermi | Decision | 2 | 3 | 5 | 3 | 3 | 16 | **3.08** | existe pero debil |
| 39 | M01 | OODA (Boyd) | Militar | 2 | 3 | 5 | 3 | 3 | 16 | **3.08** | bien cubierto |
| 40 | S01 | TRIZ (matriz de contradicciones) | Sovietica | 2 | 3 | 3 | 4 | 4 | 16 | **3.08** | existe pero debil |
| 41 | S03 | Su-Field | Sovietica | 4 | 2 | 3 | 3 | 3 | 15 | **3.0** | existe pero debil |
| 42 | X13 | Apollo Root Cause Analysis | Extra | 3 | 3 | 4 | 2 | 3 | 15 | **3.0** | existe pero debil |
| 43 | X15 | Causal Loop / System Dynamics | Extra | 3 | 3 | 3 | 3 | 3 | 15 | **3.0** | existe pero debil |
| 44 | X18 | Value Stream Mapping | Extra | 3 | 3 | 3 | 3 | 3 | 15 | **3.0** | existe pero debil |
| 45 | L06 | 5 Whys | Lean | 2 | 4 | 5 | 2 | 2 | 15 | **3.0** | bien cubierto |
| 46 | S05 | OTSM-TRIZ | Sovietica | 5 | 2 | 2 | 3 | 2 | 14 | **2.92** | no existe |
| 47 | X01 | Reflexive Control (Lefebvre) | Extra | 5 | 2 | 2 | 3 | 2 | 14 | **2.92** | no existe |
| 48 | M11 | IPB | Militar | 4 | 2 | 3 | 2 | 3 | 14 | **2.83** | no existe |
| 49 | X02 | Arte operacional sovietico (Svechin/Isserson) | Extra | 4 | 2 | 3 | 3 | 2 | 14 | **2.83** | no existe |
| 50 | E03 | NASA SE Handbook (V&V/RTM) | Ingenieria | 3 | 3 | 3 | 2 | 3 | 14 | **2.83** | existe pero debil |
| 51 | D06 | Seis sombreros | Decision | 2 | 2 | 5 | 3 | 3 | 15 | **2.83** | existe pero debil |
| 52 | L04 | Kaizen | Lean | 2 | 3 | 4 | 2 | 3 | 14 | **2.75** | existe pero debil |
| 53 | X08 | Axiomatic Design (Suh) | Extra | 4 | 2 | 3 | 2 | 2 | 13 | **2.67** | existe pero debil |
| 54 | X05 | Requisite Variety / VSM (Ashby; Beer) | Extra | 4 | 2 | 2 | 2 | 2 | 12 | **2.5** | no existe |
| 55 | X12 | Robust Decision Making (RAND) | Extra | 4 | 2 | 2 | 2 | 2 | 12 | **2.5** | no existe |
| 56 | E08 | Wardley Maps | Ingenieria | 1 | 3 | 3 | 3 | 3 | 13 | **2.5** | bien cubierto |
| 57 | L11 | PDCA | Lean | 1 | 3 | 5 | 2 | 2 | 13 | **2.5** | bien cubierto |
| 58 | L09 | Hoshin Kanri | Lean | 3 | 2 | 3 | 2 | 2 | 12 | **2.42** | existe pero debil |
| 59 | X14 | Critical Chain | Extra | 3 | 2 | 3 | 2 | 2 | 12 | **2.42** | existe pero debil |
| 60 | X16 | QFD (Casa de la calidad) | Extra | 3 | 2 | 3 | 2 | 2 | 12 | **2.42** | existe pero debil |
| 61 | X03 | Programacion lineal (Kantorovich) | Extra | 2 | 3 | 3 | 2 | 2 | 12 | **2.42** | bien cubierto |
| 62 | X19 | Taguchi (diseno robusto) | Extra | 3 | 2 | 2 | 2 | 2 | 11 | **2.25** | existe pero debil |
| 63 | S06 | Tectologia (Bogdanov) | Sovietica | 5 | 1 | 1 | 2 | 1 | 10 | **2.17** | no existe |

## Cómo se pasa del ranking al top 10

El ranking ordena **metodologías**; el producto se arma por **herramientas**. Dos fusiones documentadas (misma estructura de datos y misma herramienta, no es trampa de conteo):

- **D05 Key Assumptions Check → paso 0 de ACH.** Los supuestos son las hipótesis implícitas de partida; comparten el modelo de datos.
- **M02 Mission Command → parte de Commander's Intent.** Mission Command es la doctrina; el contrato de intención es su implementación.

**Regla de selección (revisada el 2026-11-25):** se toman las metodologías por puntaje ponderado, descontando las fusiones; el desempate es el del ranking (mayor N, luego mayor U, luego id). Dos exclusiones son **decisión del autor** y no dependen del puntaje: `fmea` y `stpa` pasan a v2, y `triz-matrix` queda como **método adicional fuera del ranking** (no ocupa plaza del top 10; está implementada y se publica con v0.1). Con eso, el top 10 de v1 queda así (ordenado por puntaje; el desempate es N, luego U, luego id):

| # | Herramienta de Clarent | Metodología(s) | Ponderado | Por qué entra |
|--:|------------------------|----------------|----------:|---------------|
| 1 | `ach` — Hipótesis competidoras (+ KAC) | D04, D05 | 4.42 | Máxima utilidad (debugging a diario) y motor determinista real; ningún repo tiene puntaje de inconsistencia + próxima prueba + evidencia citada. **Implementada (referencia).** |
| 2 | `spc` — Cartas de control para CI/DORA | L12 | 4.17 | Un gráfico se comparte solo; la herramienta previa está abandonada (2023) y sin CI. |
| 3 | `intent` — Contrato de delegación (Commander's Intent) | M07, M02 | 4.08 | Se usa cada vez que delegas a un subagente; 0 repos. |
| 4 | `rcf` — Estimar con tu propio historial (Reference Class) | X06 | 4.00 | "¿Cuánto tardará?" con distribución real; 0 repos OSS dev; muy demostrable. Absorbe la calibración de D03 (`log` y `score`). |
| 5 | `kt` — IS/IS-NOT diferencial sobre corridas de CI | E06 | 3.83 | Convierte un método de prompt en un cálculo de distinciones; utilidad 5 (flakes). |
| 6 | `redteam` — Ataque a diseños y PRs con catálogo fijo | M05 (+ X17 Team A/B, pendiente) | 3.83 | **Implementada (beta) el 2026-11-25.** Bajó de 4.25 (puesto 2) a 3.83 al corregir la novedad (el espacio está más poblado de lo que se creía: ver `novelty.md`) y la contribución (el catálogo de clases es fijo). Su hueco: un motor que rechaza hallazgos que no cita literalmente el texto, con matriz de supuestos y estado. |
| 7 | `gate` — Puerta de propuesta (Heilmeier) | X04 | 3.75 | Fácil, contribuible y completa el flujo PR/RFC. Menos novedad (3). |
| 8 | `fta` — Árbol de fallas con conjuntos mínimos de corte | E02 | 3.67 | **Reincorporada por puntaje** (había cedido su plaza a `triz-matrix` el 2026-11-24). Novedad 4 por el ángulo de incidentes de software; existen herramientas de confiabilidad (`scram` 168★, C++, 2023). Es el método más riesgoso de implementar (E=3). |
| 9 | `hazop` — Palabras guía sobre APIs y flujos de datos | X10 | 3.58 | **Entra por puntaje y por desempate** (N=4 frente a N=3 de los otros métodos con 3.58). Hueco confirmado con el re-escaneo del 2026-11-25: HAZOP existe en la industria de proceso; no hay nada para APIs ni flujos de datos de software. Especificación en `product-spec.md` §9. |
| 10 | `aar` — After Action Review desde git, CI e incidentes | M04 | 3.58 | **Decisión del autor (2026-11-25) sobre un empate exacto**: D03 y M04 tenían 3.58 con N=3 y U=4. Se elige M04 porque la calibración de D03 ya está en `rcf` (`log` y `score`). Hueco: AAR de equipos de software sobre evidencia de git/CI (`aar-loop`, 125★, es para sesiones de IA). Especificación en `product-spec.md` §10. |

**Fuera del ranking:** `triz-matrix` — matriz de contradicciones de TRIZ con ejemplos de software (S01, 3.08, puesto 40 de 63). **Implementada** (38 tests, 1 218 de 1 248 celdas verificadas contra la tabla de 1973). Se mantiene por decisión del autor, por identidad y base conceptual y no por ventaja competitiva: el escaneo de novedad encontró al menos 8 repos pequeños con la matriz como skill (`novelty.md`), y su ventaja real es el dataset verificado celda a celda y el motor con tests. Como no compite por plaza, ya no desplaza a nadie.

### Cambios del 2026-11-25 respecto de la versión del 2026-11-24

| Cambio | Antes | Ahora | Motivo |
|--------|-------|-------|--------|
| `fmea` (E01, 3.58) | puesto 6 del top 10 | **v2** | Decisión del autor. Aun sin ella habría quedado fuera por desempate: entre los métodos con 3.58 solo HAZOP (y A3, hasta su re-puntuación) tenían N=4; `fmea` tiene N=3. |
| `stpa` (E04, 3.50) | puesto 8 del top 10 | **v2** | Decisión del autor; por puntaje queda en el puesto 15, fuera del top 12. |
| `fta` (E02, 3.67) | v2 | **top 10, puesto 8** | Le corresponde por puntaje; solo había cedido su plaza a `triz-matrix`. |
| `triz-matrix` (S01, 3.08) | puesto 10 del top 10 | **método adicional fuera del ranking** | Decisión del autor; no ocupa plaza. |
| `hazop` (X10, 3.58) | candidato de v2 | **top 10, puesto 9** | Puntaje sin cambios; el re-escaneo con consultas cortas no encontró nada para APIs ni flujos de datos. |
| `redteam` (M05) | 4.25 (novedad 3, contribución 5), puesto 2 | **3.83 (novedad 2, contribución 4), puesto 6; implementada** | Re-escaneo con consultas cortas (`tools/github_scan3.py redteam`): al menos un repo de abogado del diablo con auditoría de supuestos, pre-mortem y hallazgos con severidad (`aaddrick/contrarian`, 43★) y tres revisores adversariales de PR (`magpie` 180★, `claude-code-gauntlet`, `adv-review`) cuya verificación es otro paso de LLM. Ninguno tiene un motor que rechace por cita literal. La contribución baja porque el catálogo de clases es fijo en código (decisión de diseño), no un archivo por lente. |
| `aar` (M04) | empatada en la plaza 10 con D03 (3.58) | **plaza 10, especificada** | Decisión del autor. D03 queda absorbida por `rcf`. |
| A3 (L08) | 3.58, novedad 4 ("no existe") | **3.33, novedad 3 ("existe pero débil"), puesto 22** | Re-escaneo con consultas cortas (`tools/github_scan3.py`): al menos 6 repos de 0–5★ (editores y generadores de A3 con IA); ninguno orientado a desarrollo ni con motor, pero ya no son "0 resultados". Es la misma corrección que sufrió TRIZ. |

### Quién queda fuera y por qué

| Metodología | Ponderado | Motivo |
|-------------|----------:|--------|
| **`fmea`** (E01), **`stpa`** (E04) | 3.58 / 3.50 | Pasan a v2 por decisión del autor (2026-11-25). `fmea` tiene el hueco de "FMEA de módulos de software con O y D tomados de git y cobertura" y `stpa` el de agentes/microservicios; ninguno está en el MVP. |
| **Pre-mortem** (M06) | 3.33 | **Bien cubierto**: 3 skills dedicadas (59–88★) y 2 colecciones. Ya está como clase `failure-modes` de `redteam` (el Handbook de UFMCS lo incluye, pp. 138–140), sin tool propia. |
| **A3** (L08) | 3.33 | Salió del top 12 al corregir la novedad (ver arriba). Sigue siendo candidato de v3; un ángulo posible es el A3 como reporte de incidente con evidencia citada. |
| **Superforecasting / calibración** (D03) | 3.58 | Empató con M04 por la plaza 10 y perdió por decisión del autor: su núcleo (registrar pronósticos y medir calibración) ya está en `rcf`. |
| **ARIZ-85** (S02) | 3.25 | Flujo largo con estado y compuertas (E=2). Primer bloque de v2 como "Pack Soviético" junto con Su-Field (ver `roadmap.md`). La matriz de TRIZ ya está en v1 como `triz-matrix`. |
| **Wardley, PDCA, 5 Whys, OODA, Poka-yoke** | 2.50–3.17 | Bien cubiertos; no competir. |
| **Tectología, OTSM, Control reflexivo** | 2.17–2.92 | Alto valor de marca/educativo, utilidad operativa difícil de demostrar. Útiles para el README ("de dónde viene"), no para el producto. |

## Robustez del ranking

Re-puntué con otras ponderaciones y los puntajes vigentes (tras las correcciones de A3 y de `redteam`). Se cuenta cuántas de las 10 herramientas quedan entre las 12 primeras del ranking (`ach` e `intent` cuentan por su mejor metodología fusionada). Ponderaciones (N/U/E/V/C): *Base* 1.5/1.5/1/1/1; *Igual* 1/1/1/1/1; *Utilidad x3* 1/3/1/1/1; *Novedad x3* 3/1.5/1/1/1. Recalculado el 2026-11-25 con el desempate N → U → id (con él, el puesto de `stpa` en *Igual* sale 15 y no 17 como figuraba antes).

| Ponderación | Herramientas dentro de las 12 primeras | Fuera | `redteam` | `hazop` | `aar` | `fta` | `triz-matrix` | `fmea` | `stpa` | A3 |
|-------------|---------------------------------------:|-------|----------:|--------:|------:|------:|--------------:|-------:|-------:|---:|
| Base | 9 / 10 | `aar` | 6 | 11 | 14 | 9 | 40 | 13 | 15 | 22 |
| Igual para todos | 9 / 10 | `aar` | 5 | 11 | 14 | 9 | 40 | 13 | 15 | 22 |
| Utilidad x3 | 8 / 10 | `hazop`, `aar` | 6 | 20 | 13 | 9 | 41 | 12 | 14 | 26 |
| Novedad x3 | 8 / 10 | `redteam`, `aar` | 19 | 7 | 18 | 5 | 50 | 17 | 9 | 31 |

(Las últimas siete columnas son el puesto entre las 63.)

Lectura: la selección **resiste** el cambio de ponderación en 8 de 10 herramientas. Las plazas frágiles son tres: `aar` (puesto 14 con los puntajes base: está dentro por una decisión del autor sobre un empate, no por holgura), `hazop` (cae si la utilidad pesa triple) y `redteam` (cae si la novedad pesa triple, porque tiene N=2). `stpa` sube hasta el puesto 9 cuando se premia la novedad, de modo que su paso a v2 es una decisión del autor y no una consecuencia del puntaje.

## Qué podría invalidar este ranking

- Que las colecciones de prompts (p. ej. `cc-thinking-skills`) agreguen motores deterministas: la novedad de N=4 bajaría. Revisar cada mes (`tools/github_scan2.py`, `tools/github_scan3.py`).
- Que mi estimación de E (facilidad) sea optimista para `fta` (conjuntos mínimos de corte) y `hazop` (generar nodos y parámetros desde OpenAPI); son los más riesgosos del top 10.
- Que aparezcan más repos competidores como en los casos de TRIZ y A3, donde el escaneo inicial subestimó la cobertura por usar consultas de varias palabras con semántica AND. **Los "0 resultados" del resto de `novelty.md` deben tratarse con la misma cautela** y repetirse con consultas cortas antes del lanzamiento público.
- Que las estrellas de los repos de referencia no reflejen uso real.
