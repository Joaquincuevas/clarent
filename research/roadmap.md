# Roadmap

> Supuesto de capacidad: **una persona a ~25–30 h/semana** (estudiante con otras obligaciones). Con 10–12 h/semana, duplica todos los plazos y recorta `intent` del MVP. Los esfuerzos vienen de `product-spec.md` (estimaciones mías, sin medir).

## Estado de partida (hoy)

| Hecho | Evidencia |
|-------|-----------|
| 2 métodos implementados de punta a punta: `ach` y `triz-matrix` | 23 + 38 tests, ejemplos en/es, fichas, skills, plugin generado con ambas |
| Núcleo con registro y `doctor` | 16 tests; valida manifiesto, ficha, skill, fuentes |
| Plugin (`clarent-methods`) y marketplace (`clarent`) válidos | `claude plugin validate` pasa en ambos |
| CI, plantillas, CONTRIBUTING | escritos; **el CI aún no se ejecutó en GitHub** (no hay remoto) |
| Catálogo (63), novedad, ranking, specs, arquitectura, crecimiento | `research/`; novedad y ranking corregidos el 2026-11-24 (ver `novelty.md`) |

Lo que **no** existe todavía: remoto en GitHub, evals, demo grabada, hooks/MCP/Actions, los otros 8 métodos del top 10 con especificación (más la plaza 10, aún sin especificar), tests de CI en Windows/Linux reales, y la verificación de las 29 celdas en disputa de la matriz TRIZ contra el libro.

---

## v1 — MVP en 4 semanas → `v0.2.0` (beta cerrada)

**Objetivo:** 3 métodos creíbles + un eval honesto + 5 personas externas que lo probaron. *No* es el lanzamiento público. Con `triz-matrix` ya implementada, el mínimo para lanzar es **`ach` + `triz-matrix` + `spc`**; `intent` pasa a ser lo primero que se recorta.

| Semana | Entregables | Criterio de salida |
|-------:|-------------|--------------------|
| **1** | **ACH a beta**: verificar el capítulo en el PDF de Heuer y corregir `CARD.md`; armar `evals/` (arnés con/sin skill) y reunir los primeros 5 casos reales cerrados; hook `PostToolUse` opcional que recuerde re-puntuar tras nuevas pruebas; subir el repo a GitHub y ver el CI verde en Linux y Windows. | CI verde; 5 casos con causa conocida y `ref`s; `ach` pasa a `beta`. |
| **2** | **`spc`**: carta XmR + reglas de detección (verificar definiciones exactas contra una fuente antes de publicar), carta p, SVG sin dependencias, fuente `gh run list`, ventana de commits candidatos, tests con series sintéticas (medir falsa alarma en 1 000 series con semilla fija). | Detecta desplazamiento conocido ≤ 3 puntos; tasa de falsa alarma medida y documentada; ficha completa. |
| **3** | **`intent`**: formato, `lint`, `verify` (diff vs rutas permitidas + comandos de verificación), hook `SubagentStop` con exit 2, skill. | Test con repo git temporal: un cambio fuera de `allowed_paths` es devuelto; plantilla mínima de 4 campos. |
| **4** | **Eval y beta**: completar los 10 casos del eval de `ach` y correrlo; grabar 2 demos (ACH, SPC); README con demo e instalación por agente (solo lo que se probó); beta con 5 desarrolladores externos; corregir lo que se rompa. Tag `v0.2.0`. | Resultado del eval publicado (nulo o no); ≥ 3 de 5 beta-testers completan el quick start sin ayuda. |

**Qué se recorta si se atrasa (en este orden):** `intent` → v1.1; demo de SPC; hook de ACH. **Lo que nunca se recorta:** el eval y la beta con externos.

**Riesgos de v1:** la estimación de `spc` es la más segura; `intent` depende de cómo se comporte el hook en sesiones reales (probar `SubagentStop` con un subagente real antes de dar nada por hecho).

---

## Lanzamiento público (semana 5)

Condiciones y secuencia en `growth-plan.md` §5: repo público, post con un caso real, Show HN (reglas verificadas), hilo en X, publicaciones en comunidades **tras leer sus reglas**. Retro a las 4 semanas contra los indicadores de §6.

---

## v1.1 — semanas 6–9 → `v0.3.0`

| Entregable | Nota |
|------------|------|
| `redteam` (subagente + lentes + `check` con verificación de citas literales) | mayor potencial de contribución: 1 lente = 1 archivo |
| `rcf` (clase de referencia desde git, cuantiles, libro de pronósticos) | demo fuerte; riesgos de datos documentados |
| `intent` si se recortó | |
| Servidor MCP mínimo para `ach` (extra `[mcp]`) | solo si hay demanda real en issues |
| `ach` → `stable` con el eval publicado | congelar esquema `clarent.ach/1` |
| Responder a los issues del lanzamiento | prioridad sobre funcionalidades nuevas |

## v2 — meses 3–5 → `v0.5.0`

| Bloque | Contenido |
|--------|-----------|
| **Pack Soviético** (identidad de marca; ver `ranking.md`) | `ariz`: ARIZ-85 con estado y compuertas (partes 1–9) sobre contradicciones de arquitectura, y Su-Field. La matriz de TRIZ ya está en v1 (`triz-matrix`); en v2 queda pendiente **comparar las 29 celdas en disputa con el libro** y **resolver con asesoría la licencia de los datos** (`DATA_LICENSE.md`) |
| **Ingeniería** | `kt` (diferencial IS/IS-NOT sobre CI, con puente a ACH), `fta` (conjuntos mínimos de corte; reincorporada al top 10 el 2026-11-25) y `hazop` (palabras guía × parámetros de API/flujos de datos; entra al top 10 el 2026-11-25; especificación en `product-spec.md` §9) |
| **Gobernanza de propuestas** | `gate` (Heilmeier) + Action que comenta el PR |
| **Aplazadas fuera del top 10** (decisión del autor, 2026-11-25) | `fmea` (Python vía `ast`) y `stpa` (la apuesta de mayor novedad; empezar por `--lite`). Se retoman después del bloque de Ingeniería; sus especificaciones siguen en `product-spec.md` |
| **Plataforma** | router de métodos (Cynefin), `AGENTS.md` generado por método y pruebas reales en Cursor/Codex antes de afirmar compatibilidad, sitio de documentación, `SECURITY.md`, `CODE_OF_CONDUCT.md` |

## v3 — meses 6–12 → `v1.0.0`

| Bloque | Contenido |
|--------|-----------|
| **Cobertura** | siguientes por ranking: la plaza 10 si queda sin cubrir (AAR desde evidencia de git/CI o calibración, empatadas en 3.58), A3 (3.33 tras re-puntuar), Design Structure Matrix desde el grafo de imports, Delphi con varios agentes independientes, calibración (Brier) sobre el libro de pronósticos de `rcf` |
| **Ecosistema** | métodos de terceros vía *entry points* `clarent.methods` (hoy el descubrimiento es por carpeta); registro público de métodos con su estado de verificación y novedad |
| **Calidad** | panel de evals por método con/sin skill; ficha con resultado visible |
| **Estabilidad** | congelar contratos (`method.toml`, esquemas `clarent.<método>/N`, códigos de salida); política de versiones |
| **Comunidad** | segundo y tercer mantenedor; rotación de "steward" por método |

**Criterio para declarar 1.0:** ≥ 8 métodos `stable` con eval publicado, ≥ 10 contribuidores externos con PR fusionado, contratos congelados y 3 meses sin cambios incompatibles.

---

## Puntos de decisión

| Cuándo | Decisión | Insumo |
|--------|----------|--------|
| Fin de semana 4 | ¿Lanzar o seguir en beta? | Resultado de la beta y del eval |
| +4 semanas del lanzamiento | ¿Continuar con v1.1 completo o reducir alcance? | Indicadores de `growth-plan.md` §6 |
| Mes 3 | ¿Pivote a "pocos métodos excelentes"? | ¿Hay contribuidores externos y evals no nulos? |
| Antes de v2 | ¿ARIZ/TRIZ como identidad o como método más? | Tracción de v1; decisión del autor |
| Cada 90 días | Reverificar novedad (`doctor --fail-on-stale`) | Escaneo GitHub |
