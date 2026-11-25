# Estrategia de crecimiento y comunidad

> Datos: API de GitHub, 2026-11-24 (`research/data/growth-repos.tsv`) y los README que leí (`obra/superpowers`, `garrytan/gstack`, `github/spec-kit`, `danielmiessler/fabric`, `hesreallyhim/awesome-claude-code`, `affaan-m/everything-claude-code`, `tjboudreaux/cc-thinking-skills`). Lo que no pude verificar está marcado ⚠.

## 1. Calibración honesta de expectativas

Velocidad media desde la creación (estrellas ÷ días; es un promedio, **no** una curva):

| Repo | ★ | Creado | ★/día | Tipo |
|------|--:|--------|------:|------|
| `affaan-m/ECC` (everything-claude-code) | 310 153 | 2026-01-18 | 1 000 | colección/harness |
| `obra/superpowers` | 325 720 | 2025-10-09 | 793 | metodología de desarrollo como skills |
| `garrytan/gstack` | 142 574 | 2026-03-11 | 553 | roles de equipo como skills; autor famoso |
| `anthropics/skills` | 199 907 | 2025-09-22 | 467 | oficial |
| `github/spec-kit` | 151 274 | 2025-08-21 | 329 | respaldado por GitHub |
| `punkpeye/awesome-mcp-servers` | 98 467 | 2024-11-30 | 136 | awesome-list |
| `hesreallyhim/awesome-claude-code` | 58 734 | 2025-04-19 | 101 | awesome-list |
| `danielmiessler/Fabric` | 44 761 | 2024-01-03 | 42 | prompts organizados + CLI |
| **`tjboudreaux/cc-thinking-skills`** (competidor temático más cercano) | **1 767** | 2026-01-28 | **5.9** | 28 frameworks como skills + evals |

Lectura honesta:
- Los números de arriba corresponden a repos con **autor famoso, respaldo institucional o un momento de ecosistema** (ver §2). No son una base de planificación para un proyecto independiente.
- El proyecto más parecido a Clarent lleva ~10 meses y 1.8k★. Una meta razonable para Clarent en 6 meses es **1 000–3 000★ y 10+ contribuidores externos**; superar eso depende de un golpe de difusión que **no se puede planificar**.
- "Alta adopción" se persigue con indicadores adelantados (§6), no con la cifra de estrellas.

## 2. Qué hicieron los repos que crecieron (hechos leídos, no inferidos)

| Repo | Táctica observable | Qué copiar | Qué NO copiar |
|------|--------------------|------------|---------------|
| **superpowers** | README abre con una frase de propuesta y un "How it works" en prosa; **lista de ~16 plataformas** de instalación (Claude Code, Cursor, Codex CLI, Gemini CLI, Copilot CLI, OpenCode…); sección *Philosophy*; enlace al post de lanzamiento (blog del autor, 2025-10-09, el mismo día de creación del repo); política explícita de contribuciones restrictiva ("no aceptamos nuevas skills en general") | Post de lanzamiento el día 0; matriz de instalación por agente | La política de no aceptar skills: Clarent crece justo por contribuciones de métodos |
| **gstack** | Autor con audiencia propia (presidente y CEO de Y Combinator, según su README); "Quick start" de **4 pasos** y "Stop there. You'll know if this is for you."; sección *What it doesn't do* con **resultado nulo propio** (58 vs 61 de 99 tareas) | Quick start corto; honestidad sobre lo que no hace; comandos con nombre memorable | Depender de la fama del autor (no replicable) |
| **spec-kit** | Respaldado por GitHub; tabla "**Choose your process**" (qué necesitas → proceso → resultado); README en 4 idiomas; sitio de documentación; gráfico de historial de estrellas | Tabla "elige tu método"; README multilingüe (Clarent ya tiene es/en) | — |
| **ECC** | Imagen hero, insignias de ranking de tendencias, selector de **17 idiomas** | Selector de idiomas visible | Volumen sin profundidad: no tengo evidencia sobre calidad (⚠ no leí el código) |
| **Fabric** | Posicionamiento como problema: "AI no tiene un problema de capacidades, tiene uno de **integración**"; prompts como unidades (patterns) con CLI | Frase de posicionamiento de una línea; la unidad contribuible es un archivo | — |
| **awesome-claude-code / awesome-mcp-servers** | Listas curadas con categorías y "Recently Added"; `awesome-mcp-servers` se creó el 2024-11-30, **11 días después** de `modelcontextprotocol/servers` (2024-11-19) | Llegar temprano a un ecosistema nuevo; categorías claras | — (son listas, no herramientas) |
| **cc-thinking-skills** | 28 skills + router + carpeta `evals/` + sección "Evidence" que califica su propio +4.0 pp como "direccional" | Arnés de evals público desde el inicio | Ser solo prompts (es justo el hueco que Clarent ocupa) |
| **prompts.chat** (awesome-chatgpt-prompts) | Creado 2022-12-05, días después del lanzamiento de ChatGPT (30-nov-2022, ⚠ fecha de memoria) | Entrar en el pico de un ecosistema | — |

**Patrón común verificable**: (1) una frase que explica el problema, no la tecnología; (2) instalación en < 1 minuto con un solo comando; (3) un ejemplo que se entiende sin instalar; (4) un día-0 con post propio.

## 3. Posicionamiento

- **Una línea:** *"Classic decision and engineering methods as tools that compute — not prompts that sound smart."*
- **Contra la competencia directa:** las colecciones dan listas de verificación; Clarent da **motores deterministas + disciplina de evidencia + datos de tu repo**. Es la única afirmación que el código respalda y que el competidor no puede igualar con más prompts.
- **Contra el escepticismo (AI-slop):** Show HN excluye explícitamente "quickly generated one-offs: anybody can do that now" (📖 reglas de Show HN). La defensa es profundidad verificable: tests, fuentes marcadas, `doctor`, evals publicados incluso si son nulos.
- **Historia de marca** (opcional, no es el producto): "métodos de la tradición soviética, militar e industrial". Cuidado de tono: evitar glorificar o politizar; las técnicas de origen militar se presentan solo como análisis defensivo de **tus propios sistemas** (ver §7).

## 4. Anatomía objetivo del README (estado actual → falta)

| Elemento | Estado |
|----------|--------|
| Frase de propuesta + por qué existe | ✅ hecho |
| Tour de 60 segundos con comandos reales | ✅ hecho (ejemplo sintético, marcado) |
| Qué **no** afirmamos | ✅ hecho |
| Tabla de métodos con estado | ✅ hecho |
| **Demo visual de 10–15 s** (terminal grabada) | ❌ falta |
| Matriz de instalación por agente | ❌ falta (hoy solo Claude Code + CLI) |
| Tabla "elige tu método" (síntoma → herramienta) | ❌ falta (v0.2, tras 3 métodos) |
| README en español | ❌ falta (el CLI ya emite español) |
| Insignias (CI, licencia) | ❌ falta, trivial |
| Resultado de eval | ❌ falta; el más importante para credibilidad |

### Guiones de demo (cada uno ≤ 15 s, sin voz)

1. **ACH — flaky test:** `clarent ach score flaky-test.json` → se ve la matriz, tres hipótesis tachadas ("refutada") y la línea *"Próxima prueba: T1"*. Cierra con el comando de T1.
2. **SPC (cuando exista):** gráfico de control de duración de CI con un punto marcado "regla 4 — desde el run #3412" y los commits candidatos.
3. **RCF (cuando exista):** "tu estimación (1 d) cae bajo el P10 de 23 PRs similares".
Herramientas de grabación habituales: `asciinema` o `vhs` (⚠ no verifiqué su estado actual).

## 5. Plan de lanzamiento

**No lanzar hasta tener** (criterio de salida de "pre-lanzamiento"): ≥ 3 métodos funcionando (ACH + 2 de `spc`/`intent`/`rcf`), 1 eval publicado, README con demo, CI verde en Linux y Windows, y 5 desarrolladores externos que lo hayan probado.

| Semana | Acción | Detalle y restricción |
|-------:|--------|-----------------------|
| −4 a −2 | **Beta cerrada** | 5–10 desarrolladores; observar dónde se atascan en el quick start. Corregir antes de cualquier difusión. |
| −2 | **Eval inicial** | 10 casos reales cerrados (flakes/incidentes) con causa conocida; con y sin la skill; publicar métricas y el resultado aunque sea nulo. |
| −1 | **Post de lanzamiento** | Un caso real contado paso a paso ("encontré la causa de un flaky test con el método ACH de la CIA"), con la matriz. Publicado en el blog del autor el mismo día que el repo se hace público. |
| 0 | **Repo público + post + X** | Hilo corto con el GIF; enlazar el post. Un solo mensaje claro. |
| 0 (martes–jueves, ⚠ preferencia, no verificada) | **Show HN** | Título `Show HN: Clarent – CIA's ACH and other classic methods as debugging tools`. Reglas verificadas 📖: debe ser algo que se pueda **probar ya**, sin registro; **no pedir votos** a amigos; el autor debe quedarse respondiendo. Preparar respuestas a: "¿esto no es solo un prompt?" (respuesta: motor + tests) y "¿para qué sirve la CIA aquí?" (respuesta: sesgo de confirmación). |
| 0–1 | **Reddit** | Comunidades de agentes de código y de DevOps/testing. **Leer las reglas de autopromoción de cada subreddit antes de publicar** (⚠ no las verifiqué). Publicar el caso de estudio, no el repo. |
| +1 | **Listas curadas** | Enviar PR a las listas awesome de Claude Code/skills (⚠ revisar sus guías de contribución). |
| +2 | **Product Hunt** | Opinión: bajo retorno para una librería/CLI sin interfaz; hacerlo solo si hay landing con demo. No bloquea nada. |
| +4 | **Retro de lanzamiento** | Medir contra §6; decidir si continuar con v2. |

## 6. Indicadores y criterios de parada

| Indicador (semanal) | Meta v1 (6 meses) | Señal de alarma |
|---------------------|-------------------|-----------------|
| ★ netas/semana tras el pico de lanzamiento | > 15 | < 3 durante 6 semanas |
| Issues abiertos por **personas externas** | ≥ 2/semana | 0 durante 4 semanas |
| PRs de contribuidores externos fusionados | ≥ 10 acumulados | 0 a los 3 meses |
| Tiempo a primera respuesta a issue/PR | < 72 h | > 7 días |
| Métodos con eval publicado | 100 % de los `stable` | métodos `stable` sin eval |
| Reaparición de uso (instalaciones que vuelven a ejecutar) | no medible sin telemetría; usar encuesta de 3 preguntas en el repo | — |

**Criterio de parada o pivote:** si a los 3 meses del lanzamiento no hay ningún contribuidor externo y los evals son nulos, reducir el alcance a 3–4 métodos excelentes en vez de 10, o convertir el repo en un conjunto de artículos con código.

## 7. Sistema de contribuciones

- **Unidad contribuible pequeña:** un *ejemplo real* de redteam, una *regla* (spc), una *traducción*, una *verificación de fuente*. Cada una es un archivo y la revisa `clarent doctor` + CI, lo que filtra PRs de baja calidad (también los generados masivamente con IA).
- **Etiquetas:** `good first issue` (≤ 2 h, con archivo y criterio de aceptación escritos), `new-method`, `verify-source`, `needs-eval`, `help wanted`.
- **Lista inicial de good first issues (concretos):**
  1. Traducir los mensajes de `clarent_ach` a pt-BR (copiar el bloque `es` de `i18n.py`).
  2. Añadir un ejemplo ACH real (bug público cerrado, con enlace al issue).
  3. Verificar el capítulo de ACH en el PDF de Heuer y corregir `CARD.md` (hoy marcado ⚠).
  4. Verificar 5 fuentes `unverified` del catálogo y subirlas a `read`.
  5. Añadir `--format csv` al informe de `ach next`.
  6. Añadir un ejemplo real de `redteam`: un diseño o PR público y sus hallazgos aceptados por el motor.
  7. Añadir test de propiedades (aleatorios con semilla) a `engine.score`.
  8. README en español.
- **Hoja de ruta pública:** `research/roadmap.md` + un GitHub Project con las mismas columnas.
- **Cadencia "una metodología nueva por semana": no es sostenible con calidad.** Las specs estiman 3 días–2 semanas por método. Propuesta realista: **una entrega pública por semana, de tamaño variable** — semanas impares: una lente/regla/ejemplo/verificación de la comunidad; semanas pares: un método nuevo (el autor) o un avance de él. El "método de la semana" es la tarjeta del catálogo a verificar, que sí es semanal.
- **Gobernanza ligera:** `CODEOWNERS` por método, SLA de revisión 72 h, tabla de contribuidores en cada ficha, y reconocimiento explícito en las notas de versión.
- **Salvaguardas éticas:** las técnicas de origen militar (CARVER, Red Team, Wargaming, IPB) se documentan como análisis **defensivo de sistemas propios o autorizados**; ninguna herramienta ejecuta ataques ni automatiza acceso. El control reflexivo y otras técnicas de influencia permanecen como conceptos de modelado, sin herramientas operativas.

## 8. Riesgos

| Riesgo | Mitigación |
|--------|-----------|
| Una colección con tracción añade motores deterministas | Moverse rápido en `ach`, `spc`, `rcf`; revisar la novedad cada 90 días (`doctor --fail-on-stale` en CI programado). |
| "Es solo prompts/AI-slop" | Tests, evals, fuentes con nivel de verificación, motores, demo reproducible. |
| Agotamiento del mantenedor único | Alcance v1 de 4 métodos; unidades contribuibles pequeñas; no prometer cadencia semanal de métodos. |
| Citas inexactas sobre doctrina o autores | Niveles de verificación; PR de corrección bienvenido; sección de "correcciones a creencias populares" en el catálogo. |
| Sensibilidad del tema (militar/soviético) | Tono técnico y neutral; solo uso defensivo; sin glorificación. |
| Nombre | Distribución `clarent-methods`; verificar marca antes de invertir en identidad. |
