# Validación de novedad

> Escaneo: 2026-11-24. Datos crudos reproducibles: `research/data/github-scan.json` (63 metodologías × 2–3 consultas), `research/data/github-scan-targeted.json` (37 consultas dirigidas), `research/data/growth-repos.tsv`. Scripts: `tools/github_scan.py`, `tools/github_scan2.py`.

## Veredicto en una frase

**Las metodologías ya existen como *prompts*; lo que no existe son *motores ejecutables* de esas metodologías alimentados con datos reales de desarrollo.** Esa es la tesis de Clarent y debe ser el criterio de entrada de cada método.

## Hallazgos que cambian el plan

1. **Hay colecciones de frameworks de pensamiento como skills, y una tiene tracción.** Competidores directos del concepto "repo de metodologías":

   | Repo | ★ | Qué es | Qué cubre del catálogo |
   |------|--:|--------|------------------------|
   | `tjboudreaux/cc-thinking-skills` | 1 767 | 28 skills manuales + router + carpeta `evals/`; MIT; creado 2026-01-28 | Kepner-Tregoe, Cynefin, TRIZ, Pre-mortem, Red Team (seguridad), ToC, OODA, 5 Whys+, "scientific method" (rankear causas y probar el discriminador más barato) |
   | `mattnowdev/thinking-partner` | 233 | 150+ modelos mentales | genérico |
   | `product-on-purpose/thinking-framework-skills` | 29 | 63 frameworks con grados de evidencia y recetas | incluye ACH (marcado como "lente en disputa"), ToC, Red Team Light |
   | `l4ci/latticework`, `eddiebelaval/squire`, `gagharutyunyan1993/methodology-toolkit`, `fpizzuta/mental-models` | 0–21 | colecciones menores | Premortem, Cynefin, etc. |

   Consecuencia: **un repo que sea "más prompts de frameworks" no es novedoso** y compite con 1.7k★ ya instaladas. Se salva solo si cada método incluye cómputo determinista, conexión a datos (git, CI, trazas) y evals.

2. **Pre-mortem, 5 Whys, PDCA, OODA, poka-yoke y AAR ya tienen skills dedicadas.** Se bajan de prioridad (ver tabla).
3. **El propio líder del nicho publica que no mejora la tasa de resolución.** El README de `garrytan/gstack` (142k★) dice textualmente que en un test de noviembre de 2026 sobre 100 bugs/features Claude Opus 5.5 resolvió 58 con gstack y 61 de 99 sin él. Consecuencia para Clarent: **no prometer "tu agente resuelve más bugs"**; prometer artefactos auditables (matrices, reportes, gráficos) y medirlo con evals.
4. **`superpowers` (326k★) no acepta skills nuevas por PR** ("we don't generally accept contributions of new skills"). Clarent tiene una ventaja posible: contribuciones de metodologías como formato de primera clase.
5. **Conflicto de nombre menor**: `clarent` en PyPI es un paquete abandonado de 2014 (v0.1.1, "Shared API definitions for an online exercise system") y `github.com/clarent` es un usuario. Ver `architecture.md` (nombre de distribución `clarent-methods`).

## Estado por metodología (resumen)

De 63 metodologías puntuadas: **18 "no existe"**, **37 "existe pero débil"**, **7 "bien cubierto"**, **1 "existe pero abandonado"**. Tabla completa con puntajes en `ranking.md` y `research/data/scores.csv`.

Criterio de la etiqueta:
- **no existe**: 0 repos relevantes con ≥2 formulaciones de búsqueda y sin cobertura en las colecciones anteriores.
- **existe pero débil**: solo prompt en colecciones, o repos < 50★, o con >50★ pero de otro dominio (no dev) o sin mantenimiento.
- **existe pero abandonado**: ≥ 50★ y sin push en > 2 años.
- **bien cubierto**: ≥ 1 repo dedicado, dev-orientado, ≥ 50★ y mantenido, o herramientas maduras.

## Detalle para los candidatos del top

| Método | Lo que existe (evidencia) | Etiqueta | Hueco real (ángulo Clarent) |
|--------|---------------------------|----------|------------------------------|
| **ACH** | `Burton/Analysis-of-Competing-Hypotheses` 112★ (PHP, último push 2012-01); `suprathermal/ACH-Grounding` 2★; `lightcaptainguy/bayesian-ach-reasoning-prototype` 2★; prompt en `thinking-framework-skills` (29★); adyacentes: `doraemonkeys/claude-code-debug-mode` 120★ (depuración por hipótesis con logs), `iamalisson/inquisitor` 5★. Consultas "analysis of competing hypotheses claude" y "…debugging": **0 resultados** **Corrección 2026-11-24 (consultas cortas):** también `shahvatsalofficial/IncidentSutra-AI` 4★ (CLI de investigación de incidentes con hipótesis competidoras), `annatchijova/vigia-intent-analysis` 18★ y `ApartsinProjects/EMR-ACH` 1★. | existe pero débil | Ninguno tiene **matriz con puntaje de inconsistencia, diagnosticidad, sensibilidad y selección de la próxima prueba**, ni exige evidencia citada. |
| **Red Team (UFMCS)** | `thinking-red-team` (seguridad/ataque autorizado); `CharlescSturt/claude-red-team-skill` 0★; `pingteck/touchstone` 0★; `gaasher/Agent-Loop-Skills` 185★ incluye red-teaming como un bucle genérico **Corrección:** `drewmattie-code/red-team` 3★ ya aplica técnicas del Tradecraft Primer de la CIA a ideas y planes; el ecosistema de red-team ofensivo es enorme (p. ej. `Claude-BugHunter` 21k★) pero es de seguridad, otro caso de uso. | existe pero débil | Nadie aplica el repertorio UFMCS (Key Assumptions, Devil's Advocacy, Team A/B, What-If, HI/LP) **a un diseño o PR concreto** con hallazgos con severidad. |
| **SPC en CI** | `carlosqsilva/pyspc` 244★ (último push 2023-01), `pyshewhart` 34★; consultas "control chart ci…" y "statistical process control ci flaky tests": **0** **Corrección:** `CarlosZambonii/kaizenops` 1★ (SPC sobre GitHub Actions) existe; la consulta larga anterior no lo vio. | existe pero abandonado | Cartas de control + reglas Western Electric sobre series de CI/DORA, con alerta solo por causas especiales. |
| **Commander's Intent / Mission Command** | Consultas "commander's intent subagent prompt" y "mission command agent orchestration delegation": **0**. Adyacentes: `github/spec-kit` (specs), `superpowers` (briefs a subagentes) **Corrección:** usan el término `shagghiesuperstar/commanders-intent` 5★ (plantilla de bot) y `ntholm86/ai-steward` 0★ ("Commander's Intent" mantenido por el operador); ninguno es un contrato con lint y verificación. | no existe | Contrato de delegación con lint y verificación de deriva de intención. |
| **Reference Class Forecasting** | Consultas "reference class forecasting git history estimate" y "estimate cycle time from git history monte carlo": **0**; `sethmblack/skill-reference-class-forecasting` 0★ (prompt). Existen herramientas comerciales de forecast Monte Carlo para Kanban (⚠ sin verificar) | no existe (en OSS dev) | Estimar con la distribución del **propio historial** de PRs/issues del repo. |
| **FMEA** | `jherrodthomas/automotive-skills-suite` 2 879★ (ISO 26262, automotriz); `008993368-yaz/expect-the-unexpected` 1★ (modos de falla por escenario); `chenxihuang1028-a11y/risk-management-specialist` 6★ (ISO 14971, dispositivos médicos) **Corrección:** `dromation/open-fmea` 49★, `YuchenXia/LLMRiskAnalyzer` 41★ (FMEA asistido por LLM) y `RBraga01/Quality-Engineering-Skills` 57★ (incluye FMEA AIAG-VDA). Novedad 4 → 3. | existe pero débil | FMEA de **módulos de software** con severidad/ocurrencia/detección, ligado a archivos y líneas. |
| **Kepner-Tregoe** | `thinking-kepner-tregoe` (prompt en colección); `KepnerTregoe-wizard` 0★; consulta "is/is not problem specification debugging": **0** | existe pero débil | **Diferencial automático** IS/IS-NOT sobre corridas de CI que fallan vs. pasan. |
| **STPA** | Consultas "STPA software llm", "STPA unsafe control actions tool", "system-theoretic process analysis claude": **0**. `geovani-ribeiro/stpa-capella-afcs` 0★ (aeronáutico). Hay papers que aplican STPA a IA (arXiv 2506.01782 y 2512.17600, títulos vistos en búsqueda) **Corrección:** `kieler/pasta` 38★, extensión de VS Code para análisis de riesgo basado en STPA (con integración de árboles de fallas); no apunta a agentes ni microservicios. Novedad 5 → 4. | existe pero débil (corregido; antes "no existe") | Estructura de control, UCAs y escenarios para **sistemas de agentes y microservicios**, con chequeo de cobertura de la tabla UCA. |
| **Heilmeier** | `RealZYZhang/paper-reader-heilmeier` 93★ (leer papers con las preguntas) | existe pero débil | Puerta de **PR/RFC**, no de lectura de papers. |
| **FTA** | `rakhimov/scram` 168★ (C++, último push 2023-09); `idaholab/EMRALD` 37★; `JunyiJ/Fault-Tree-Python` 15★ (2017) | existe pero débil | Árboles de fallas desde incidentes con **conjuntos mínimos de corte**, orientado a software. |
| **TRIZ / ARIZ** | **Corregido el 2026-11-24** (ver abajo). Al menos 8 repos pequeños con la matriz de contradicciones como skill: `Antropocosmist/triz-engineering-solver` 24★ (MIT), `ironyjk/triz-agents` 5★, `magery-ai/triz-skill` 4★, `SharathSPhD/triz-engine` 6★, `seogineer/triz-solver` 0★, `luchi2333/triz-worker-innovation-research` 3★, `sampil/triz-skill` (sin licencia detectada), `ayoub-elkhader/llm-triz-dfx` 1★; además `ironyjk/strategy-frameworks` 47★ (TRIZ entre 30 frameworks), `jenson500/triz-prompt-engineering` 41★ (formato de prompts) y `lyderisaz/ariz85v-pwa` 0★ (hoja ARIZ offline). `trizen/trizen` (820★) es un falso positivo por nombre | existe pero débil (**saturado de repos pequeños**) | La matriz en sí **no es novedosa**. Lo que ninguno ofrece: dataset **verificado celda a celda** contra la tabla de 1973, motor stdlib con tests, lecturas en software de los 39 parámetros, salida bilingüe. ARIZ-85 con estado y compuertas sigue sin existir. |
| **Pre-mortem** | `Hi1talib1World/Premortem` 88★, `AndyShaman/premortem` 61★, `MADEVAL/Pre-Mortem-Skill` 59★ + 2 colecciones | **bien cubierto** | Ninguno: no es buen candidato de referencia. |
| **PDCA / 5 Whys / OODA / AAR / Poka-yoke** | `bkit-claude-code` 606★; `5-whys-skill` 66★; `vulnerator-ai` 295★, `ooda-subagents` 176★; `aar-loop` 125★; `poka-yoke` 26★ | bien cubierto / débil | AAR tiene un ángulo propio (desde evidencia de git/CI) pero es secundario. |
| **Wardley** | `awesome-wardley-maps` 837★, `onlinewardleymaps` 311★, `wardley-maps-book` 309★ | bien cubierto | No competir. |

## Huecos reales (ordenados por solidez de la evidencia)

1. **Motores deterministas por método** (ACH, SPC, RCF, FTA, KT-diferencial, STPA-cobertura): ninguna colección los tiene.
2. **Conexión a datos de desarrollo**: git history, resultados de CI, trazas — las colecciones operan solo sobre la conversación.
3. **Disciplina de evidencia**: separar "observado" de "inferido" y exigir referencia. Ninguna colección lo impone mecánicamente.
4. **Medición**: solo una colección (`cc-thinking-skills`) tiene un arnés de evals, con resultados que ellos mismos califican de "direccionales".
5. **Contrato de delegación a subagentes** (Commander's Intent).
6. **Perfil Soviético/Ruso**: TRIZ tiene presencia; ARIZ con flujo y OTSM, Tectología, Control reflexivo, Arte operacional: casi ausentes (valor de marca, no de utilidad diaria).

## Corrección del 2026-11-24 (TRIZ)

El primer escaneo (`github_scan.py`, `github_scan2.py`) usó consultas de varias palabras sin comillas, que GitHub interpreta con semántica AND y devolvieron **0 resultados** para "triz matrix python", "triz contradiction matrix json" y similares. Al repetir con consultas de una o dos palabras (`contradiction matrix`, `triz matrix`, `triz principles`, `40 inventive principles`) aparecieron al menos 8 repos con la matriz de TRIZ. La conclusión original ("existe pero débil: 24★ y 5★ + colecciones") **subestimaba la cobertura**; `scores.csv` se actualizó (novedad 3 → 2).

Consecuencia metodológica: **los "0 resultados" de este documento son cotas inferiores**, no pruebas de ausencia. Antes del lanzamiento conviene repetir cada afirmación "no existe" con consultas de una o dos palabras y por topics.

## Límites de este análisis (léelo antes de citarlo)

- GitHub Search indexa nombre, descripción, topics y README, pero **no es exhaustiva**; "0 resultados" significa "no encontrado con esas consultas", no "no existe en ningún lado".
- No revisé GitLab, npm, PyPI (salvo el nombre), marketplaces de plugins de terceros ni Hugging Face.
- Las estrellas son un indicador de atención, no de calidad. No leí el código de la mayoría de los repos; las etiquetas se apoyan en descripción, estrellas, fecha de último push y los README que sí leí (`superpowers`, `gstack`, `spec-kit`, `fabric`, `cc-thinking-skills`, parte de `thinking-framework-skills`).
- Las consultas con varias palabras sin comillas usan semántica AND y pueden dar cero con redacciones distintas; repetí con 2–3 formulaciones por método, pero conviene reejecutar `tools/github_scan2.py` antes del lanzamiento.
- Los repos con nombres genéricos generan falsos positivos (p. ej. `trizen/trizen`); revisé a mano los que usé como evidencia.
