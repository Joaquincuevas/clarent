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
| 2 | M05 | Red Teaming (UFMCS) | Militar | 3 | 4 | 5 | 5 | 5 | 22 | **4.25** | existe pero debil |
| 3 | L12 | SPC (control charts) | Lean | 4 | 4 | 4 | 5 | 4 | 21 | **4.17** | existe pero abandonado |
| 4 | M07 | Commander's Intent | Militar | 4 | 5 | 4 | 4 | 3 | 20 | **4.08** | no existe |
| 5 | X06 | Reference Class Forecasting | Extra | 4 | 4 | 4 | 5 | 3 | 20 | **4.0** | no existe |
| 6 | E06 | Kepner-Tregoe (IS/IS-NOT) | Ingenieria | 3 | 5 | 4 | 4 | 3 | 19 | **3.83** | existe pero debil |
| 7 | D05 | Key Assumptions Check | Decision | 3 | 4 | 5 | 3 | 4 | 19 | **3.75** | existe pero debil |
| 8 | X04 | Heilmeier Catechism | Extra | 3 | 4 | 5 | 3 | 4 | 19 | **3.75** | existe pero debil |
| 9 | E02 | Fault Tree Analysis | Ingenieria | 4 | 4 | 3 | 4 | 3 | 18 | **3.67** | existe pero debil |
| 10 | M02 | Auftragstaktik / Mission Command | Militar | 4 | 4 | 4 | 3 | 3 | 18 | **3.67** | no existe |
| 11 | L08 | A3 | Lean | 4 | 3 | 4 | 3 | 4 | 18 | **3.58** | no existe |
| 12 | X10 | HAZOP (guidewords) | Extra | 4 | 3 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 13 | D03 | Superforecasting / calibracion | Decision | 3 | 4 | 4 | 4 | 3 | 18 | **3.58** | existe pero debil |
| 14 | E01 | FMEA/FMECA | Ingenieria | 3 | 4 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 15 | M04 | After Action Review (AAR) | Militar | 3 | 4 | 4 | 3 | 4 | 18 | **3.58** | existe pero debil |
| 16 | E04 | STAMP/STPA | Ingenieria | 4 | 4 | 3 | 3 | 3 | 17 | **3.5** | existe pero debil |
| 17 | X07 | Design Structure Matrix | Extra | 4 | 4 | 3 | 3 | 3 | 17 | **3.5** | existe pero debil |
| 18 | D01 | Delphi | Decision | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 19 | L03 | Andon | Lean | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 20 | M08 | CARVER | Militar | 4 | 3 | 4 | 3 | 3 | 17 | **3.42** | no existe |
| 21 | E05 | Theory of Constraints / DBR | Ingenieria | 3 | 4 | 3 | 4 | 3 | 17 | **3.42** | existe pero debil |
| 22 | L01 | Jidoka | Lean | 3 | 4 | 4 | 3 | 3 | 17 | **3.42** | existe pero debil |
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

Con eso, el top 10 de v1 queda así. El orden es el de la primera versión; la columna *Ponderado* ya está **actualizada con los puntajes corregidos del 2026-11-24**, por eso `fmea` y `stpa` aparecen con puntaje menor que herramientas listadas después. **El puesto 10 es una decisión del autor, no del puntaje** (ver el recuadro bajo la tabla):

| # | Herramienta de Clarent | Metodología(s) | Ponderado | Por qué entra |
|--:|------------------------|----------------|----------:|---------------|
| 1 | `ach` — Hipótesis competidoras (+ KAC) | D04, D05 | 4.42 | Máxima utilidad (debugging a diario) y motor determinista real; ningún repo tiene puntaje de inconsistencia + próxima prueba + evidencia citada. **Referencia end-to-end implementada.** |
| 2 | `redteam` — Agente adversario sobre diseños/PRs | M05 (+ X17 Team A/B) | 4.25 | Mayor puntaje de demo y contribución (cada técnica/persona es un archivo). Hueco: aplicar el repertorio UFMCS a un artefacto concreto. |
| 3 | `spc` — Cartas de control para CI/DORA | L12 | 4.17 | Un gráfico se comparte solo; la herramienta previa está abandonada (2023) y sin CI. |
| 4 | `intent` — Contrato de delegación (Commander's Intent) | M07, M02 | 4.08 | Se usa cada vez que delegas a un subagente; 0 repos. |
| 5 | `rcf` — Estimar con tu propio historial (Reference Class) | X06 | 4.00 | "¿Cuánto tardará?" con distribución real; 0 repos OSS dev; muy demostrable. |
| 6 | `fmea` — FMEA de un módulo de software | E01 | 3.58 | Existe en automotriz/médico y hay herramientas genéricas (open-fmea 49★, LLMRiskAnalyzer 41★); el hueco es el FMEA de **módulos de software** con O y D tomados de git y cobertura. **Con el puntaje corregido cae al puesto 14: ya no entra por puntaje.** |
| 7 | `kt` — IS/IS-NOT diferencial sobre corridas de CI | E06 | 3.83 | Convierte un método de prompt en un cálculo de distinciones; utilidad 5 (flakes). |
| 8 | `stpa` — Análisis de estructura de control (agentes/microservicios) | E04 | 3.50 | Hay una extensión de VS Code para STPA (`kieler/pasta`, 38★), pero nada para agentes/microservicios. **Con el puntaje corregido cae al puesto 16: ya no entra por puntaje.** Más difícil (E=3). |
| 9 | `gate` — Puerta de propuesta (Heilmeier) | X04 | 3.75 | Fácil, contribuible y completa el flujo PR/RFC. Menos novedad (3). |
| 10 | `triz-matrix` — Matriz de contradicciones de TRIZ con ejemplos de software | S01 | 3.08 | **Decisión del autor (2026-11-24): reemplaza a `fta`.** Es la base conceptual elegida y aporta identidad al proyecto. **Implementada** (38 tests, 1 218 de 1 248 celdas verificadas contra la tabla de 1973). |

> **Decisión del autor que contradice el puntaje.** `triz-matrix` (3.08, puesto 40 de 63) reemplaza a `fta` (3.67, puesto 9 con los puntajes corregidos). El puntaje de TRIZ **bajó** al incorporar evidencia nueva: el escaneo inicial subestimó la cobertura (hay al menos 8 repos pequeños con la matriz como skill; ver `novelty.md`, corrección del 2026-11-24), de modo que la novedad pasa de 3 a 2. La razón para incluirla es de identidad y de base conceptual, no de ventaja competitiva; la ventaja real es el dataset verificado celda a celda y el motor con tests. `fta` pasa a v2.

### Quién queda fuera y por qué

| Metodología | Ponderado | Motivo |
|-------------|----------:|--------|
| **Pre-mortem** (M06) | 3.33 | **Bien cubierto**: 3 skills dedicadas (59–88★) y 2 colecciones. Se puede incluir como *paso* dentro de `redteam`, sin tool propia. |
| **A3** (L08), **HAZOP** (X10) | 3.58 | Siguientes en la lista; HAZOP (palabras guía × parámetros de API) es un buen candidato de v2. |
| **AAR** (M04) | 3.58 | Hay un repo con 125★; ángulo propio (AAR desde git/CI) válido para v2. |
| **ARIZ-85** (S02) | 3.25 | Flujo largo con estado y compuertas (E=2). Primer bloque de v2 como "Pack Soviético" junto con Su-Field (ver `roadmap.md`). La matriz de TRIZ ya está en v1 como `triz-matrix`. |
| **Fault Tree Analysis** (E02) | 3.67 | Habría sido el décimo por puntaje; **cedió su lugar a `triz-matrix` por decisión del autor**. Pasa al primer bloque de v2; su especificación sigue en `product-spec.md`. |
| **Wardley, PDCA, 5 Whys, OODA, Poka-yoke** | 2.50–3.17 | Bien cubiertos; no competir. |
| **Tectología, OTSM, Control reflexivo** | 2.17–2.92 | Alto valor de marca/educativo, utilidad operativa difícil de demostrar. Útiles para el README ("de dónde viene"), no para el producto. |

## Robustez del ranking

Re-puntué con otras ponderaciones y con los **puntajes corregidos** (ver la corrección del 2026-11-24 en `novelty.md`). Se cuenta cuántas de las 10 herramientas elegidas quedan entre las 12 primeras del ranking (`ach` y `intent` cuentan por su mejor metodología fusionada):

| Ponderación | Herramientas del top 10 final dentro de las 12 primeras | `triz-matrix` | `fta` | `fmea` | `stpa` |
|-------------|--------------------------------------------------------:|--------------:|------:|-------:|-------:|
| Base (1.5/1.5/1/1/1) | 7 / 10 | 40 | 9 | 14 | 16 |
| Igual para todos | 7 / 10 | 40 | 9 | 14 | 17 |
| Utilidad x3 | 8 / 10 | 41 | 9 | 12 | 14 |
| Novedad x3 | 7 / 10 | 50 | 6 | 19 | 11 |

(Las últimas cuatro columnas son el puesto de cada una entre las 63.)

Lectura: tras la corrección, **ACH, red team, SPC, Intent, RCF, KT y Heilmeier siguen resistiendo; `triz-matrix` (decisión del autor), `fmea` y `stpa` no.** Con puntajes puros, el décimo puesto sería `fta`, y A3 y HAZOP (3.58) estarían por delante de `fmea` y `stpa`. No reordené la lista más allá de lo que pediste (`fta` → `triz-matrix`); queda abierta una decisión sobre `fmea`/`stpa` (ver informe final). Ninguna de las dos está en el MVP de 4 semanas, así que la decisión no bloquea nada.

## Qué podría invalidar este ranking

- Que las colecciones de prompts (p. ej. `cc-thinking-skills`) agreguen motores deterministas: la novedad de N=4 bajaría. Revisar cada mes (`tools/github_scan2.py`).
- Que mi estimación de E (facilidad) sea optimista para `stpa` y `fta`; son los más riesgosos.
- Que aparezcan más repos competidores como el caso de TRIZ, donde el escaneo inicial subestimó la cobertura por usar consultas de varias palabras con semántica AND. Los "0 resultados" del resto de `novelty.md` deben tratarse con la misma cautela.
- Que las estrellas de los repos de referencia no reflejen uso real.
