# Arquitectura del repo

> Todo lo descrito como "implementado" existe en este repo y está probado (`python tools/test_all.py`, 77 tests; `clarent doctor`; `claude plugin validate` sobre el plugin y el marketplace). Lo marcado "diseño" aún no existe.

## 1. Principios

1. **Un método = una carpeta autocontenida** (ficha + manifiesto + motor + tests + ejemplo + skill). Se puede añadir o quitar sin tocar el resto.
2. **Núcleo determinista**: cada método calcula o valida algo sin LLM. El agente propone; el motor puntúa, valida y puede rechazar.
3. **Cero dependencias en tiempo de ejecución**: stdlib de Python ≥ 3.11. El plugin de Claude Code no requiere `pip install` (el motor viaja dentro de la skill).
4. **Una sola fuente de verdad**: `methods/<id>/`. El plugin de Claude Code (`plugins/claude-code/`) es **generado** y CI falla si está desactualizado.
5. **Honestidad verificable**: cada fuente declara cuánto se verificó; cada afirmación de novedad lleva fecha y caduca (advertencia a los 90 días).
6. **Coste de contexto explícito**: descripciones de skill ≤ 300 caracteres (Claude Code carga nombre y descripción de cada skill invocable por el modelo en todas las sesiones, según su documentación ✅); skills de uso ocasional con `disable-model-invocation: true`.

## 2. Estructura de carpetas

```text
clarent/
├── README.md  CONTRIBUTING.md  LICENSE (Apache-2.0)  pyproject.toml  .gitattributes
├── src/clarent/                  # núcleo (implementado)
│   ├── cli.py                    #   clarent list | doctor | <método> …
│   └── registry.py               #   descubrimiento + validación de métodos ("doctor")
├── methods/                      # un método por carpeta
│   ├── triz-matrix/              # ← implementado: matriz TRIZ con datos verificados (clarent_triz/data/)
│   └── ach/                      # ← implementado, es la referencia
│       ├── method.toml           #   manifiesto: id, familia, estado, superficies, fuentes, novedad
│       ├── CARD.md               #   ficha de metodología (11 secciones obligatorias)
│       ├── clarent_ach/          #   motor (stdlib): model · engine · render · cli · i18n
│       ├── skill/SKILL.md        #   skill de Claude Code
│       ├── tests/                #   unittest
│       └── examples/             #   ejemplos ejecutables (en/es)
├── plugins/claude-code/          # GENERADO por tools/build_plugin.py (no editar a mano)
│   ├── .claude-plugin/plugin.json
│   └── skills/ach/{SKILL.md, scripts/run.py, scripts/clarent_ach/}
├── .claude-plugin/marketplace.json   # marketplace "clarent" (valida con `claude plugin validate`)
├── templates/methodology-card.md # plantilla de contribución
├── tests/                        # tests del núcleo
├── tools/                        # test_all.py · build_plugin.py · rank.py · github_scan*.py
├── research/                     # estos 7 documentos + data/ (escaneos y puntajes)
└── .github/                      # CI, frescura de novedad, plantillas de issue/PR
```

Diseño (aún no existe), por orden de llegada: `evals/` (arnés con/sin skill), `methods/<id>/agents/` y `hooks/` para los métodos que los necesiten, `mcp/` (servidor), `actions/` (GitHub Actions compuestas), `docs/` (sitio).

## 3. Contrato de un método

`method.toml` (validado por `clarent doctor`):

| Campo | Regla |
|-------|-------|
| `id`, `name`, `version`, `summary` | `id` = nombre de la carpeta |
| `family` | `military · lean · soviet · systems · decision · extra` |
| `status` | `spec → beta → stable → reference` |
| `[python] module` | paquete importable que expone `main(argv) -> int` |
| `[surfaces]` | `cli, skill, agent, hook, mcp, action`: lo declarado `true` debe existir (el doctor lo comprueba para `cli` y `skill`) |
| `[[sources]]` | `title` + `url` o `citation` + `verification ∈ {read, exists, blocked, unverified}`; `read`/`blocked` exigen `url` |
| `[novelty]` | `checked_on` (ISO), `status ∈ {none, exists-but-weak, exists-but-abandoned, well-covered}`, `evidence` |

`CARD.md` debe contener las 11 secciones de `templates/methodology-card.md`: *Origin · Sources · Problem it solves · When to use / when NOT to use · How it maps to software work · Inputs and outputs · Algorithm (what is deterministic) · Limitations · Prior art (GitHub scan) · Worked example · Evaluation*. La sección **Algorithm** obliga a responder qué calcula el código sin LLM; si la respuesta es "nada", el método no entra.

**Flujo de publicación (implementado)**: editar `methods/<id>/` → `python tools/test_all.py` → `clarent doctor` → `python tools/build_plugin.py` → commit. CI repite los tres y verifica `--check`.

## 4. Compatibilidad

| Superficie | Estado | Detalle |
|------------|--------|---------|
| **CLI standalone** | implementado | `clarent <método> …` o `python -m clarent_<id> …`. `--lang en\|es` / `CLARENT_LANG`. Salida `md`/`json`; códigos `0/1/2`. |
| **Claude Code: skills** | implementado | Plugin con `skills/<id>/SKILL.md`; se invoca como `/clarent-methods:<id>`. Verificado contra la documentación de Claude Code: manifiesto en `.claude-plugin/plugin.json`, campos de frontmatter `name`, `description`, `disable-model-invocation`, `argument-hint`, y `${CLAUDE_SKILL_DIR}` ✅. |
| **Claude Code: marketplace** | implementado | `.claude-plugin/marketplace.json` (`name`, `owner`, `plugins[].source = "./plugins/claude-code"`) ✅. Instalación: `/plugin marketplace add <owner>/clarent`. |
| **Claude Code: hooks** | diseño | Evento `SubagentStop` (matcher = tipo de agente) para `intent verify`: exit 2 mantiene al subagente trabajando ✅ (docs de hooks). Declarar en `hooks/hooks.json` del plugin con `${CLAUDE_PLUGIN_ROOT}`. |
| **Claude Code: subagentes** | diseño | `agents/red-team.md` (contexto aislado) para `redteam`. |
| **MCP server** | diseño | `clarent mcp` (stdio) exponiendo `clarent_<método>_<acción>` (los nombres de herramientas MCP en Claude Code son `mcp__<servidor>__<herramienta>` ✅). Extra opcional `[mcp]` para no contaminar el núcleo sin dependencias. |
| **GitHub Actions** | diseño | Acciones compuestas: `spc` (programada), `gate` (comentario en PR), `redteam --fail-on`. |
| **Cursor / Codex / otros** | diseño, **no probado** | El formato `SKILL.md` es el de Agent Skills (los campos `license`/`compatibility` aparecen en la documentación de Claude Code como "Agent Skills spec" ✅), y `obra/superpowers` documenta instalación en Cursor, Codex CLI, Gemini CLI y otros (📖 tabla de contenidos de su README). Plan: generar `AGENTS.md` por método que llame al CLI. Hasta probarlo, no se afirma compatibilidad. |

## 5. Datos y esquemas

- Un análisis = un archivo JSON en `.clarent/<método>/` (ignorado por git por defecto; el equipo decide commitearlo).
- Cada esquema lleva versión (`clarent.<método>/1`) y los cambios incompatibles suben el número; el motor rechaza versiones desconocidas con un mensaje claro.
- Los motores **nunca** escriben fuera del archivo indicado ni ejecutan el contenido de los datos (solo JSON; sin `eval`, sin plantillas).

## 6. Seguridad

- Las skills y los hooks se ejecutan con los privilegios del usuario (la documentación de Claude Code advierte que un plugin puede ejecutar código con tus permisos ✅). Por eso: motores solo con stdlib, sin red, sin subprocesos salvo los que el método declare (p. ej. `git`, `gh` en `spc`/`rcf`/`kt`), y revisión humana obligatoria de cualquier cambio en `scripts/`.
- Dependencias fijadas y mínimas; `[mcp]` es el único extra previsto.
- `SECURITY.md` y política de divulgación: pendiente (ver roadmap).

## 7. Nombre y distribución

| Hecho verificado el 2026-11-24 | Consecuencia |
|--------------------------------|--------------|
| `pypi.org/project/clarent` **existe**: paquete abandonado de 2014 ("Shared API definitions for an online exercise system", v0.1.1) | Distribución como **`clarent-methods`** (libre en PyPI); el comando y el import siguen siendo `clarent`. Alternativa lenta: reclamar `clarent` por PEP 541 (⚠ no evaluado). |
| `npm` `clarent` **libre**; `@clarent/core` libre | Sin plan de paquete npm en v1. |
| `github.com/clarent` es un **usuario** (cuenta de 2012, 1 repo) y `clarent-dev` también existe | El repo vive bajo la cuenta del autor. Organización: `clarent-tools`, `clarent-hq`, `clarent-methods`, `clarentdev`, `getclarent` y `clarent-labs` aparecen libres en GitHub, PyPI y npm. |
| Búsqueda en GitHub de repos llamados `clarent`: 33 resultados, todos ≤ 5★ y sin relación | Sin colisión relevante. **No hice una búsqueda de marca registrada**; hazla antes de gastar en identidad visual. |

## 8. Licencia recomendada: Apache-2.0

**Por qué:**
- **Concesión explícita de patentes** y cláusula de **no uso de marca**: protege el nombre "Clarent" y da tranquilidad a empresas que adoptan metodologías con herramientas derivadas.
- Compatible con adopción corporativa y con contribuciones bajo DCO (sin CLA que frene a los contribuidores).
- Hay precedente en el nicho: `Aider-AI/aider` usa Apache-2.0 (50k★, consultado vía API). Los repos más grandes de skills usan MIT (`obra/superpowers`, `garrytan/gstack`, `github/spec-kit`, `wshobson/agents`), de modo que **MIT también sería defendible** y es más corto de leer; la diferencia práctica es la patente y la marca.
- Un archivo `NOTICE` atribuirá las fuentes de las metodologías.

**Cuidados de licencia de contenido (pendientes de verificar caso a caso):**
- Documentos del gobierno de EE. UU. (CIA, Army, NASA) suelen ser de dominio público en EE. UU. ⚠ pero **no todo lo alojado en un sitio .mil/.gov es obra del gobierno**; solo se citan con enlace, no se redistribuyen.
- El libro *Wardley Maps* es **CC BY-SA 4.0** ✅: incorporar texto o figuras obligaría a compartir igual; basta con enlazar.
- La **matriz de contradicciones de TRIZ (39×39)**: **resuelta parcialmente** (2026-11-24). Se incluye un consenso de 5 transcripciones cuyos repos tienen archivo `LICENSE` MIT leído; los avisos de copyright viajan en `clarent_triz/data/DATA_LICENSE.md`. **No** está establecida la cadena de titularidad anterior (el repo upstream `kamil-szczepanik/TRIZ-Agents` dice "MIT" en el README pero no tiene archivo LICENSE; la transcripción original de 2007 y triz40.com tienen términos desconocidos), ni si la compilación de resultados de Altshuller está protegida. Quien necesite una cadena limpia usa `--data DIR`. Las 76 soluciones estándar no se incluyen.
- Las traducciones no oficiales (p. ej. ARIZ-85C) se enlazan, no se copian.

## 9. Decisiones abiertas para el autor

1. ¿Licencia Apache-2.0 (recomendada) o MIT (más habitual en el nicho)?
2. ¿Organización nueva en GitHub o cuenta personal? (nombres libres arriba).
3. ¿Idioma: inglés primero (recomendado, el nicho es global) con español como segunda lengua ya soportada por la ficha/CLI?
