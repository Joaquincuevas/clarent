# Catálogo de metodologías (63 entradas)

> Fecha de verificación de fuentes: 2026-11-24. Datos crudos de GitHub en `research/data/`.

## Cómo leer los estados de las fuentes

Ninguna cita de este documento está inventada. Cada fuente lleva un estado que dice **cuánto verifiqué**:

| Marca | Significado |
|:-----:|-------------|
| 📖 | **Leída**: descargué el documento o la página y leí el pasaje citado. |
| ✅ | **Existe**: la URL respondió 200 a un script, o una búsqueda web devolvió el documento/ficha bibliográfica coincidente. No leí el contenido completo. |
| 🔒 | **Existe pero no pude abrirla**: el servidor devuelve 403 a scripts (bloqueo de bots). La ficha bibliográfica es conocida; el contenido no se leyó. |
| ⚠ | **Sin verificar**: no se encontró fuente primaria. Se deja explícito; verifícala antes de citarla en el repo público. |

> **Segunda pasada de verificación (2026-11-24).** Cada cita ⚠ de la primera versión se buscó: libros contra Open Library, artículos contra Crossref (`tools/verify_citations.py`, evidencia en `research/data/citation-checks.json`), y afirmaciones de origen contra fuentes primarias o secundarias identificadas por búsqueda. **✅ aquí significa «existe un registro o fuente que coincide en título, autor y año»; no significa «leí el texto»**. El resumen de resultados, incluidas las correcciones de errores míos, está al final de este documento.

Los campos «Mapeo a programación» son **propuestas de diseño mías**, no afirmaciones de las fuentes.

### Correcciones a creencias populares (detectadas al verificar)

- **Pre-mortem, "+30 %"**: Klein (HBR 2007) dice que la "retrospectiva prospectiva" aumenta en 30 % la capacidad de identificar causas correctas. El estudio original (Mitchell, Russo & Pennington 1989) encontró que imaginar el evento como ya ocurrido aumentó **~30 % el número de razones generadas**, sin medir su calidad. Clarent no debe repetir "+30 % de precisión".
- **FMEA ≠ NASA**: nació en el ejército de EE. UU. (MIL-P-1629, 1949); NASA publicó su procedimiento FMECA para Apollo en 1966 (🔎 varias fuentes coinciden).
- **Cinco pasos de TOC**: fuentes discrepan sobre si ya estaban en *La Meta* (1984) o se formalizaron después; Clarent los cita como "TOC" sin atribuirlos a una edición.

---

## Familia 1 — Militar (11)

### M01 · OODA (Observe–Orient–Decide–Act)
- **Origen:** John Boyd, USAF; briefings 1976–1996.
- **Fuente:** Boyd, *Patterns of Conflict* (1986), PDF en coljohnboyd.com ✅ <https://www.coljohnboyd.com/static/documents/1986-12__Boyd_John_R__Patterns_of_Conflict__PDF_version.pdf>. *Destruction and Creation* (3 sep. 1976) ✅ (listado en el índice de Boyd de ausairpower.net; la URL de coljohnboyd.com sirve una página HTML, no el PDF); *The Essence of Winning and Losing* (primera edición 28 jun. 1995, última ene. 1996) 📖 <https://slightlyeastofnew.com/wp-content/uploads/2010/03/essence_of_winning_losing.pdf>.
- **Resuelve:** Decidir y adaptarse más rápido que el entorno/adversario; Boyd escribe en *Essence*: «orientation shapes observation, shapes decision, shapes action, and in turn is shaped by the feedback…» 📖; que ese sea *el* énfasis (más que la velocidad) es la lectura interpretativa habitual, no una cita.
- **Mapeo:** Incidentes (bucle on-call), debugging (observar → modelo → hipótesis → acción), diseño de bucles de agentes con paso explícito de "re-orientar".

### M02 · Auftragstaktik / Mission Command
- **Origen:** Doctrina prusiana/alemana del s. XIX. **El origen exacto es discutido** ✅: según el resumen de la búsqueda, ADP 6-0 (ed. 2019) lo traza a las reformas prusianas posteriores a Jena, y la ADP 6-0 de 2012 que leí **no** lo menciona; Herrera, «History, Mission Command, and the Auftragstaktik Infatuation» (*Military Review*, jul.–ago. 2022) ✅ <https://www.armyupress.army.mil/Journals/Military-Review/English-Edition-Archives/July-August-2022/Herrera/> sostiene que esa atribución es infundada; otros estudios atribuyen la idea a Federico el Grande o a Moltke, y señalan que Moltke no usó la palabra. Clarent no afirma un origen.
- **Fuente:** ADP 6-0 (ed. 2019 «Mission Command: Command and Control of Army Forces»; la búsqueda indica una edición de julio de 2026 titulada «Command and Control») ✅ <https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN47032-ADP_6-0-000-WEB-1.pdf>. Definición 2019 citada por Army.mil: «el enfoque del Ejército al mando y control que empodera la toma de decisiones subordinada y descentraliza la ejecución» ✅ <https://www.army.mil/article/225414/combined_arms_center_launches_new_mission_command_doctrine>.
- **Resuelve:** Coordinar sin microgestionar cuando el plan detallado quedará obsoleto.
- **Mapeo:** Delegación a subagentes y a humanos: orden = intención + estado final + restricciones + libertad de acción (ver M07).

### M03 · MDMP (Military Decision-Making Process)
- **Origen:** Doctrina del Ejército de EE. UU.
- **Fuente:** ADP 5-0 *The Operations Process* ✅ <https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN18126-ADP_5-0-000-WEB-3.pdf>; CALL, *MDMP Handbook* (nov. 2023) ✅ <https://api.army.mil/e2/c/downloads/2023/11/17/f7177a3c/23-07-594-military-decision-making-process-nov-23-public.pdf>. Siete pasos: recepción de misión, análisis de misión, desarrollo de COA, análisis de COA (wargame), comparación de COA, aprobación, producción de órdenes ✅ (según ADP 5-0 vía búsqueda).
- **Resuelve:** Planificación iterativa con varios cursos de acción comparados con criterios explícitos.
- **Mapeo:** Planificar migraciones/refactors grandes: 3 COA, wargame contra modos de falla, matriz de comparación, "orden" final.

### M04 · After Action Review (AAR)
- **Origen:** US Army; el ARI (Army Research Institute) la implementó oficialmente hacia 1975 ✅ (según un artículo de la APA que cita a Morrison & Meliza, *Foundations of the After Action Review Process*, ARI Special Report 42, 1999, DTIC AD 368651; no abrí ese informe); guía formal TC 25-20 de 1993 📖.
- **Fuente:** TC 25-20, *A Leader's Guide to After-Action Reviews* (sept. 1993) 📖 <http://www.victoryprinciples.com/wp-content/uploads/2009/07/tc-25-20-ldrs-guide-aars.pdf>. Leído: define el AAR como «discusión profesional de un evento […] que permite descubrir qué pasó, por qué pasó, y cómo sostener fortalezas y mejorar debilidades»; secuencia incluye «misión/intención del comandante (lo que debía pasar)» y «resumen de eventos (lo que pasó)»; «un AAR no es una crítica».
- **Resuelve:** Comparar intención vs. resultado y extraer lecciones sin buscar culpables.
- **Mapeo:** Postmortem de incidente/PR/sprint generado desde evidencia (git, CI, logs). Cercano a la cultura de postmortems de Google SRE ✅ <https://sre.google/sre-book/postmortem-culture/>.

### M05 · Red Teaming (UFMCS)
- **Origen:** University of Foreign Military and Cultural Studies (US Army).
- **Fuente:** *Red Team Handbook* v5 (15 abr. 2011) 📖 <https://newandimproved.com/wp-content/uploads/2014/04/ufmcs_red_team_handbook_apr2011.pdf>; v9.0 (2019) ✅ <https://home.army.mil/wood/6115/8222/0759/RedTeamHB.pdf> (no descargué v9). Índice leído (v5): Key Assumptions Check, Quality of Information Check, Indicators, Deception Detection, ACH, Devil's Advocacy, Team A/Team B, High-Impact/Low-Probability, "What If?", Brainstorming, Outside-In Thinking, Red Team Analysis, Alternative Futures, Pre-mortem, Stakeholder Mapping.
- **Resuelve:** Contrarrestar sesgos de grupo y pensamiento único en planes y diseños.
- **Mapeo:** Agente adversario sobre un diseño/PR: ataca supuestos, "¿qué pasa si…?", escenarios de bajo-probabilidad/alto-impacto; salida = hallazgos reproducibles con severidad.

### M06 · Pre-mortem
- **Origen:** Gary Klein.
- **Fuente:** Klein, «Performing a Project Premortem», HBR sept. 2007 ✅ <https://hbr.org/2007/09/performing-a-project-premortem>. Base empírica: Mitchell, Russo & Pennington (1989), *J. Behavioral Decision Making* 2(1):25–38, doi:10.1002/bdm.3960020103 ✅ (registro de Crossref) (ver corrección arriba).
- **Resuelve:** Superar el optimismo del plan imaginando que ya fracasó.
- **Mapeo:** Gate previo a merge/rollout. **Ya cubierto** (ver novelty.md).

### M07 · Commander's Intent
- **Origen:** Doctrina del Ejército de EE. UU.
- **Fuente:** ADP 6-0 *Mission Command* (17 mayo 2012) 📖 <https://adamdrake.com/static/ADP-6-0-Mission-Command.pdf>. Texto leído: «The commander's intent is a clear and concise expression of the purpose of the operation and the desired military end state that supports mission command, provides focus to the staff, and helps subordinate and supporting commanders act to achieve the commander's desired results without further orders…». **Corrección:** esa definición menciona *propósito* y *estado final*; las «tareas clave» que yo había listado no están en ella, y el campo `key_tasks` del contrato `intent` es un añadido propio de Clarent.
- **Resuelve:** Que el subordinado pueda improvisar correctamente cuando el plan falla, porque conoce el *para qué*.
- **Mapeo:** **Contrato de delegación para subagentes**: `intent / end_state / constraints / freedom / stop_conditions`, con lint estructural y verificación de "deriva de intención" al recibir el resultado.

### M08 · CARVER
- **Origen:** Fuerzas Especiales de EE. UU. (época Vietnam, según resumen secundario ✅).
- **Fuente:** FM 34-36 (1991), Apéndice D «Target Analysis Process» ✅ <https://irp.fas.org/doddir/army/fm34-36/appd.htm>. Factores: Criticality, Accessibility, Recuperability, Vulnerability, Effect, Recognizability.
- **Resuelve:** Priorizar objetivos con una matriz de puntaje comparable.
- **Mapeo:** Priorizar qué endurecer en threat modeling (qué atacaría primero un adversario) o qué proteger/redundar.

### M09 · Wargaming (análisis de COA)
- **Origen:** Paso 4 del MDMP; tradición de juegos de guerra.
- **Fuente:** ADP 5-0 / CALL ✅ (ver M03). Perla, *The Art of Wargaming* (1990) ✅ (registro de Open Library, ISBN 9780870210501; no abierto).
- **Resuelve:** Probar un plan contra reacciones del adversario (acción–reacción–contra-acción).
- **Mapeo:** "Game day" en papel para una migración o un cambio de arquitectura; simular fallas y respuestas del equipo.

### M10 · Center of Gravity (CG–CC–CR–CV)
- **Origen:** Clausewitz; construcción CG–CC–CR–CV por Strange & Iron (2005).
- **Fuente:** Strange & Iron, «Understanding Centers of Gravity and Critical Vulnerabilities» ✅ <https://theforge.defence.gov.au/sites/default/files/adfwtc04_centres_of_gravity_and_critical_vulnerabilities_by_strange_and_iron.pdf> (parece Parte 2).
- **Resuelve:** Distinguir la fuente de poder (CG) de las capacidades (CC), requisitos (CR) y vulnerabilidades críticas (CV).
- **Mapeo:** Análisis estructurado de puntos únicos de falla: qué capacidad del producto depende de qué requisito, y cuál es frágil.

### M11 · IPB (Intelligence Preparation of the Battlefield)
- **Origen:** Doctrina de inteligencia del Ejército.
- **Fuente:** FM 34-36, cap. 10 (IPB para SOF) ✅ <https://irp.fas.org/doddir/army/fm34-36/ch10.htm>; ATP 2-01.3 *Intelligence Preparation of the Battlefield* (1 mar. 2019, reemplaza la edición de 2014) ✅ <https://home.army.mil/wood/8915/5751/8365/ATP_2-01.3_Intelligence_Preparation_of_the_Battlefield.pdf> (confirmado por búsqueda; no abierto).
- **Resuelve:** Entender el terreno y al adversario *antes* de planear.
- **Mapeo:** Reconocimiento previo al threat modeling: terreno = infraestructura y dependencias; adversario = actores y capacidades.

---

## Familia 2 — Industrial / Lean (12)

### L01 · Jidoka (autonomación)
- **Origen:** Toyota; sistematizado por Ohno ✅. La idea se atribuye al telar de Sakichi Toyoda que se detenía al romperse un hilo ✅ (fuentes secundarias coinciden; las fechas varían entre ~1896 y 1897 y una indica que el término *jidoka* se aplicó después; no abrí la página de Toyota).
- **Fuente:** Ohno, *Toyota Production System: Beyond Large-Scale Production* (Productivity Press, 1988) ✅ (Open Library, 1988); página del *lexicon* de lean.org ✅ (aparece en resultados de búsqueda; responde 403 a scripts, no leída).
- **Resuelve:** Que la máquina se detenga sola ante una anomalía en vez de producir defectos.
- **Mapeo:** Los agentes se detienen ante una anomalía (test rojo, diff inesperado) en vez de "taparla"; hooks de stop-the-line.

### L02 · Poka-yoke
- **Origen:** Shigeo Shingo, Toyota.
- **Fuente:** Shingo, *Zero Quality Control: Source Inspection and the Poka-Yoke System* (Productivity Press, 1986; ed. orig. japonesa 1985), ISBN 9780915299072 ✅.
- **Resuelve:** Diseñar para que el error sea imposible o inmediatamente visible.
- **Mapeo:** Diseño de APIs/tipos; guardarraíles de agentes. **Ya cubierto** (plugin dedicado, 26★).

### L03 · Andon
- **Origen:** Toyota.
- **Fuente:** Ohno 1988 ✅; lean.org *lexicon* ✅ (existe; 403 a scripts, no leída).
- **Resuelve:** Cualquiera puede detener la línea y la señal es visible para todos.
- **Mapeo:** "Cordón andon" del pipeline: cualquier persona/agente marca anomalía; tablero de estado; la línea se detiene hasta que se resuelve.

### L04 · Kaizen
- **Origen:** Toyota/Japón; Masaaki Imai, *Kaizen: The Key to Japan's Competitive Success* (1986) ✅ (Open Library: registro de 1986; otro registro del mismo título aparece fechado 1970, que parece un error de fecha del catálogo).
- **Resuelve:** Mejora continua incremental por todos.
- **Mapeo:** Registro de micro-mejoras ligado a retros; backlog de fricciones del desarrollador.

### L05 · Genchi Genbutsu
- **Origen:** Toyota; Liker, *The Toyota Way* (2004) ✅ (Open Library).
- **Resuelve:** Ir al lugar real y ver los hechos antes de decidir.
- **Mapeo:** Disciplina "observado vs. inferido": no diagnosticar sin leer el log real. Se incorpora como regla de evidencia en ACH.

### L06 · 5 Whys
- **Origen:** Toyota (atribuido a Ohno).
- **Fuente:** Ohno 1988 ✅. En el libro, Ohno presenta repetir «por qué» cinco veces como «la base del enfoque científico de Toyota» (resumen de fuente secundaria); la frase corta «Ask why five times about every matter» procede de material de Toyota (*Toyota Traditions*), y no se localizó página del libro. **Página exacta: sin verificar** (⚠).
- **Resuelve:** Llegar de un síntoma a una causa de proceso preguntando "¿por qué?" repetidamente.
- **Mapeo:** Postmortems. **Ya cubierto** (skill 66★ + colecciones). Limitación a documentar: cadena lineal, una sola causa raíz.

### L07 · Diagrama de Ishikawa
- **Origen:** Kaoru Ishikawa. *Guide to Quality Control* ✅ (Open Library lista ediciones de 1972, 1976, 1982 y 1984; la inglesa de 1976 es la que se cita habitualmente, editorial APO **no confirmada**). **La fecha de creación del diagrama es conflictiva entre fuentes secundarias** (1943 en Kawasaki según varias; popularizado en los años 60; una dice 1952) y no encontré fuente primaria: ⚠ sin verificar.
- **Resuelve:** Organizar causas candidatas por categoría.
- **Mapeo:** Pre-paso para generar hipótesis amplias (alimenta ACH).

### L08 · A3
- **Origen:** Toyota.
- **Fuente:** Sobek & Smalley, *Understanding A3 Thinking* (2008) ✅ (Open Library, ISBN 1563273608; editorial no confirmada).
- **Resuelve:** Resolver problemas en una sola hoja: contexto, estado actual, objetivo, análisis, contramedidas, seguimiento.
- **Mapeo:** Plantilla de RFC/ADR de una página con campos obligatorios y verificación de seguimiento.

### L09 · Hoshin Kanri
- **Origen:** Japón; Akao, *Hoshin Kanri: Policy Deployment for Successful TQM* (1991) ✅ (Open Library, ISBN 0915299577).
- **Resuelve:** Alinear metas de la organización con "catchball" entre niveles.
- **Mapeo:** Cascada de objetivos; cubierto de facto por OKR (baja prioridad).

### L10 · SMED
- **Origen:** Shigeo Shingo; *A Revolution in Manufacturing: The SMED System* (1985) ✅ (Open Library, ISBN 9780915299034).
- **Resuelve:** Reducir el tiempo de cambio separando preparación interna de externa.
- **Mapeo:** Reducir el tiempo de despliegue/entorno: mover pasos "internos" (con servicio detenido) a "externos" (precalentables).

### L11 · PDCA (ciclo de Shewhart/Deming)
- **Origen:** Shewhart, *Statistical Method from the Viewpoint of Quality Control* (1939) ✅ (Open Library); fuentes secundarias coinciden en que ahí (p. 45) convierte especificación–producción–inspección en un ciclo y que Deming lo presentó a JUSE en Tokio en julio de 1950, donde se reformuló como Plan-Do-Check-Act; Deming prefería «Study» en lugar de «Check» (PDSA).
- **Resuelve:** Iterar con hipótesis explícita y verificación.
- **Mapeo:** Bucle de iteración. **Ya cubierto** (bkit 606★).

### L12 · SPC (Control Estadístico de Procesos)
- **Origen:** Walter Shewhart, Bell Labs; *Economic Control of Quality of Manufactured Product* (1931) ✅ (Open Library).
- **Fuente:** NIST/SEMATECH e-Handbook, cap. 6 «Process or Product Monitoring and Control» ✅ <https://www.itl.nist.gov/div898/handbook/pmc/pmc.htm>. Reglas Western Electric: *Statistical Quality Control Handbook* (Western Electric Co., Indianápolis, 1956) ✅ (varias fuentes secundarias; no abrí el manual). Coinciden en 4 reglas por zonas (1 punto más allá de 3σ; 2 de 3 más allá de 2σ del mismo lado; 4 de 5 más allá de 1σ del mismo lado; 8 seguidos del mismo lado), **pero una fuente da 9 en la última y algunas intercambian el orden de las reglas 2 y 3**: `spc` debe hacer configurable el largo de racha.
- **Resuelve:** Distinguir variación normal (causas comunes) de señales reales (causas especiales).
- **Mapeo:** Gráficos de control sobre duración de CI, tasa de tests flaky, lead time; alertar solo ante causas especiales.

---

## Familia 3 — Soviética / rusa (6)

### S01 · TRIZ
- **Origen:** Genrikh Altshuller y Rafael Shapiro, URSS, desde 1946.
- **Fuente:** Altshuller, *Creativity as an Exact Science* (Gordon & Breach, 1984; trad. A. Williams), ISBN 0-677-21230-5 ✅ <https://searchworks.stanford.edu/view/1223823>.
- **Resuelve:** Resolver contradicciones técnicas/físicas sin ceder una propiedad por otra, con patrones extraídos del análisis de patentes.
- **Mapeo:** Contradicciones de arquitectura (latencia vs. consistencia, flexibilidad vs. simplicidad) → principios de separación y de inventiva.
- **Aviso:** la matriz de contradicciones 39×39 es dato publicado, pero su licencia/transcripción debe verificarse antes de incluirla (ver architecture.md).

### S02 · ARIZ-85
- **Origen:** Altshuller; versiones anuales hasta 1985.
- **Fuente:** «Algorithm of Inventive Problem Solving © G.S. Altshuller, 1956–1985» (traducción no oficial, ARIZ-85C) ✅ <https://evolocus.com/Textbooks/ariz85c.pdf>.
- **Resuelve:** Problemas difíciles sin solución estándar: reformula hasta llegar a una contradicción física y al Resultado Final Ideal.
- **Mapeo:** Workflow con estado y compuertas (Partes 1–9) sobre un problema de arquitectura; una hoja persistente que impide saltar pasos.

### S03 · Análisis Su-Field (sustancia-campo)
- **Origen:** Altshuller; 76 Soluciones Estándar (1985).
- **Fuente:** Altshuller, *Standards on Inventive Problem Solving* (76 estándares, 1985, en ruso) ✅ solo por fuentes secundarias (Russo & Duci, TRIZ Future 2013, y listas de referencias en ResearchGate); otras fuentes los asocian al libro *To Find an Idea* (1986). **No abrí un texto primario** (⚠ para la cita primaria).
- **Resuelve:** Modelar un sistema mínimo (dos sustancias + un campo) y detectar interacciones insuficientes o dañinas.
- **Mapeo:** Módulos = sustancias; interfaz/evento = campo; localizar acoplamientos dañinos o insuficientes.

### S04 · Leyes de evolución de sistemas técnicos
- **Origen:** Altshuller.
- **Fuente:** *Creativity as an Exact Science* ✅ (ver S01).
- **Resuelve:** Predecir hacia dónde evoluciona un sistema (idealidad creciente, dinamización, transición al supersistema).
- **Mapeo:** Roadmaps y deuda técnica: ¿qué dirección natural tiene este componente?

### S05 · OTSM-TRIZ
- **Origen:** Nikolái Khomenko, desde 1985; nombre aprobado por Altshuller en 1997 (🔎 vía otsm-triz.org).
- **Fuente:** Khomenko, «General Theory on Powerful Thinking (OTSM)» ✅ <https://www.osaka-gu.ac.jp/php/nakagawa/TRIZ/eTRIZ/elinksref/eJTS/e6thTRIZSymp10/EI01eAE-Khomenko-100606.pdf>.
- **Resuelve:** Problemas mal definidos y multidisciplinarios: red de contradicciones.
- **Mapeo:** Requisitos en conflicto; descubrimiento de producto. Alto costo de implementación.

### S06 · Tectología (Bogdánov)
- **Origen:** Aleksandr Bogdánov, 1912–1917; precursor de la teoría de sistemas.
- **Fuente:** *Essays in Tektology* (trad. G. Gorelik, Intersystems, 1980) ✅ <https://www.coexploration.org/systems/isss-books/A_Bogdanov_-_Essays_In_Tektology.pdf>.
- **Resuelve:** Ciencia general de la organización (regularidades comunes entre sistemas).
- **Mapeo:** **Especulativo.** Valor educativo y narrativo, bajo valor operativo. No se prioriza.

---

## Familia 4 — Ingeniería de sistemas (8)

### E01 · FMEA / FMECA
- **Origen:** Ejército de EE. UU., MIL-P-1629 (9 nov. 1949); NASA/Apollo 1966; MIL-STD-1629A (1980) ✅ (🔎 varias fuentes).
- **Fuente:** <https://en.wikipedia.org/wiki/Failure_mode,_effects,_and_criticality_analysis> ✅ (secundaria). AIAG & VDA *FMEA Handbook* (1.ª ed., jun. 2019) reemplazó RPN por «Action Priority» (AP) ✅ (varias fuentes secundarias coinciden; el manual es de pago y no lo abrí).
- **Resuelve:** Enumerar modos de falla, su efecto y qué tan graves/probables/detectables son.
- **Mapeo:** FMEA automático de un módulo/endpoint: modos de falla ligados a líneas de código, severidad/ocurrencia/detección, acciones.

### E02 · Análisis de Árbol de Fallas (FTA)
- **Origen:** H. A. Watson, Bell Telephone Laboratories, 1961–62, bajo contrato de la USAF para el sistema de control de lanzamiento del Minuteman ✅ (varias fuentes; un artículo del JHU APL cita Watson, *Launch Control Safety Study*, vol. 1, Bell Labs, 1961). 📖 El *Fault Tree Handbook* de la NASA confirma que estos métodos nacieron a inicios de los años 60 en programas aeroespaciales y de misiles y usa el análisis del Minuteman como ejemplo, pero no nombra a Watson.
- **Fuente:** NASA, *Fault Tree Handbook with Aerospace Applications*, v1.1 (ago. 2002) ✅ <https://s3vi.ndc.nasa.gov/ssri-kb/static/resources/Fault%20Tree%20Handbook_NASA.pdf>.
- **Resuelve:** Descomponer un evento no deseado en combinaciones lógicas (AND/OR) de causas; obtener conjuntos mínimos de corte.
- **Mapeo:** Incidente → árbol; los *minimal cut sets* revelan puntos únicos de falla.

### E03 · NASA Systems Engineering Handbook
- **Fuente:** NASA SP-2016-6105 Rev2 ✅ <https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf>.
- **Resuelve:** Ciclo de vida, V&V, trazabilidad de requisitos, revisiones técnicas.
- **Mapeo:** Matriz de trazabilidad requisito → test; criterios de entrada/salida de revisión de release.

### E04 · STAMP / STPA
- **Origen:** Nancy Leveson, MIT.
- **Fuente:** Leveson & Thomas, *STPA Handbook* (2018) ✅ <http://psas.scripts.mit.edu/home/get_file.php?name=STPA_handbook.pdf>; Leveson, *Engineering a Safer World* (MIT Press, 2011) ✅ (Open Library, ISBN 9780262533690; no abierto). Pasos verificados por búsqueda: (1) propósito del análisis: pérdidas y peligros, (2) modelo de estructura de control, (3) acciones de control inseguras (UCA), (4) escenarios de pérdida ✅.
- **Resuelve:** Accidentes por interacciones entre componentes que funcionan "bien" individualmente (no solo por fallas).
- **Mapeo:** Estructura de control de microservicios/agentes: ¿qué acciones de control pueden ser inseguras (no dadas, dadas, tarde/temprano, duración incorrecta)?

### E05 · Theory of Constraints / Drum-Buffer-Rope
- **Origen:** Eliyahu Goldratt, *The Goal* (1984, con Jeff Cox) 🔎.
- **Resuelve:** El throughput del sistema lo fija una restricción; mejorar lo demás no ayuda.
- **Mapeo:** Encontrar la restricción del flujo PR→deploy (cola de revisión, CI, QA), subordinar, limitar WIP.

### E06 · Kepner-Tregoe (Problem Analysis)
- **Origen:** Charles Kepner & Benjamin Tregoe, *The Rational Manager* (McGraw-Hill, 1965).
- **Fuente:** Extracto oficial de KT ✅ <https://kepner-tregoe.com/wp-content/uploads/2025/08/The-New-Rational-Manager-Chapters-1-2-PA.pdf>. Mecánica verificada por búsqueda: especificación IS / IS-NOT en qué, dónde, cuándo y magnitud; distinciones; cambios; toda causa candidata debe explicar *toda* la especificación ✅.
- **Resuelve:** Acotar el problema antes de buscar causas.
- **Mapeo:** Triage de tests flaky/incidentes: comparar corridas que fallan vs. las que pasan sobre dimensiones (SO, shard, hora, rama, orden…) y listar distinciones.

### E07 · Cynefin
- **Origen:** Dave Snowden.
- **Fuente:** Snowden & Boone, «A Leader's Framework for Decision Making», HBR nov. 2007 ✅ <https://hbr.org/2007/11/a-leaders-framework-for-decision-making>.
- **Resuelve:** Clasificar el contexto (claro/complicado/complejo/caótico) para elegir el tipo de respuesta.
- **Mapeo:** Router: qué metodología aplicar a una tarea (la "puerta de entrada" de Clarent).

### E08 · Wardley Maps
- **Origen:** Simon Wardley.
- **Fuente:** *Wardley Maps* (CC BY-SA 4.0) ✅ <https://learnwardleymapping.com/> y <https://medium.com/wardleymaps>.
- **Resuelve:** Situación estratégica por evolución de componentes (génesis → commodity).
- **Mapeo:** Build vs. buy. **Bien cubierto** (herramientas 300–800★).

---

## Familia 5 — Decisión y pronóstico (7)

### D01 · Delphi
- **Origen:** RAND; Dalkey & Helmer.
- **Fuente:** Dalkey & Helmer (1963), *Management Science* 9(3):458–467, doi:10.1287/mnsc.9.3.458 ✅ <https://pubsonline.informs.org/doi/10.1287/mnsc.9.3.458>.
- **Resuelve:** Consenso de expertos con cuestionarios anónimos y retroalimentación controlada.
- **Mapeo:** Estimación en rondas anónimas (humanos o varios agentes independientes) evitando anclaje.

### D02 · Estimación de Fermi
- **Fuente:** Weinstein & Adam, *Guesstimation: Solving the World's Problems on the Back of a Cocktail Napkin* (Princeton UP, 2008), doi:10.1515/9781400824441 ✅.
- **Resuelve:** Órdenes de magnitud descomponiendo en factores estimables.
- **Mapeo:** Capacidad, costos de infraestructura, tamaño de datos.

### D03 · Superforecasting / calibración
- **Fuente:** Tetlock & Gardner, *Superforecasting* (2015) ✅ (Open Library); Mellers et al. (2014), «Psychological Strategies for Winning a Geopolitical Forecasting Tournament», *Psychological Science*, doi:10.1177/0956797614524255 ✅ (registro de Crossref).
- **Resuelve:** Probabilidades calibradas, puntuadas contra resultados (Brier).
- **Mapeo:** Registrar predicciones del equipo ("¿se entrega el viernes?") y calibrarlas.

### D04 · Analysis of Competing Hypotheses (ACH)
- **Origen:** Richards J. Heuer Jr., CIA, años 70.
- **Fuente:** Heuer, *Psychology of Intelligence Analysis* (CSI/CIA, 1999) 📖 <https://www.cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis-2/> (leí la ficha: autor, año, 214 págs.). 📖 Leí una copia del libro alojada por IALEIA <https://www.ialeia.org/docs/Psychology_of_Intelligence_Analysis.pdf> (no es el sitio de la CIA): el **capítulo 8 es «Analysis of Competing Hypotheses», p. 95**, y el prefacio de Heuer lo llama «arguably the most important single chapter». El *Red Team Handbook* v5 describe ACH en p. 158 📖. Heuer & Pherson, *Structured Analytic Techniques for Intelligence Analysis* ✅.
- **Resuelve:** Evitar el sesgo de confirmación: evaluar toda la evidencia contra todas las hipótesis y **buscar refutar**, no confirmar.
- **Mapeo:** Debugging con causas competidoras; selección de la próxima prueba más discriminante. **Implementada como referencia** (`methods/ach/`).

### D05 · Key Assumptions Check (KAC)
- **Fuente:** CIA *Tradecraft Primer* (2009) ✅ <https://www.cia.gov/resources/csi/static/Tradecraft-Primer-apr09.pdf>; Red Team Handbook v5, p. 151 📖.
- **Resuelve:** Hacer explícitos y cuestionables los supuestos del modelo mental.
- **Mapeo:** Lista de supuestos de un diseño/PR con estado (respaldado / con reservas / sin respaldo) y señal de invalidación.

### D06 · Seis sombreros para pensar
- **Fuente:** de Bono, *Six Thinking Hats* (Little, Brown, 1985) ✅ (Open Library, Internet Archive y librerías; Open Library lo marca como edición de una obra anterior de 1981, *The Power of Focused Thinking: Six Thinking Hats*, y la metáfora del sombrero aparece desde 1971 en *Lateral Thinking for Management*).
- **Resuelve:** Separar modos de pensamiento en una discusión.
- **Mapeo:** Review multi-perspectiva; poca rigurosidad (prompt puro).

### D07 · Análisis morfológico (Zwicky)
- **Fuente:** Ritchey, «General Morphological Analysis» ✅ <https://www.swemorph.com/pdf/gma.pdf>; Zwicky, *Discovery, Invention, Research Through the Morphological Approach* (1969) ✅ (Open Library).
- **Resuelve:** Enumerar el espacio de diseño y podar combinaciones inconsistentes.
- **Mapeo:** Opciones de arquitectura (almacenamiento × cola × despliegue × auth) con matriz de consistencia cruzada; cómputo real.

---

## Familia 6 — Adicionales poco conocidas (19)

| ID | Metodología | Origen y fuente | Problema | Mapeo a programación |
|----|-------------|-----------------|----------|----------------------|
| X01 | **Control reflexivo** | Vladimir Lefebvre (URSS); *The Algebra of Conscience* (Reidel, 1982), ISBN 9027713014 ✅ <https://archive.org/details/algebraofconscie0026lefe>; *Parameters* (US Army War College) ✅ | Modelar cómo el adversario modela al agente para influir su decisión | Simulación de actores adversarios en seguridad/negociación; especulativo |
| X02 | **Arte operacional soviético** | Svechin, *Strategy* (1927; East View, 1992) ✅; Isserson, *The Evolution of Operational Art* (1936; trad. B. Menning, CSI) ✅ <https://www.armyupress.army.mil/Portals/7/combat-studies-institute/csi-books/OperationalArt.pdf> | Nivel intermedio entre táctica y estrategia que enlaza acciones en campañas | Descomponer un objetivo grande en "operaciones" secuenciadas y apoyadas mutuamente |
| X03 | **Programación lineal (Kantorovich)** | Kantorovich, folleto de la Univ. Estatal de Leningrado (1939) ✅ (MacTutor y artículo de Cambridge); trad. de R. W. Campbell y W. H. Marlow, *Management Science* 6(4):366–422, 1960, doi:10.1287/mnsc.6.4.366 ✅ (Crossref) | Asignación óptima de recursos | Asignar trabajo/recursos; resolvers maduros ya existen |
| X04 | **Heilmeier Catechism** | DARPA ✅ <https://www.darpa.mil/about/heilmeier-catechism> | Ocho preguntas para validar una propuesta (qué, por qué importa, riesgos, éxito…) | Puerta de PR/RFC: no se avanza sin responder las preguntas |
| X05 | **Variedad requerida / VSM** | Ashby, *An Introduction to Cybernetics* (1956) ✅ <http://pespmc1.vub.ac.be/books/IntroCyb.pdf>; Beer, *Brain of the Firm* (1972) ✅ (Open Library) | Un regulador necesita al menos la variedad de lo regulado | Cuándo un equipo/sistema de control es insuficiente para la variedad de fallas |
| X06 | **Reference Class Forecasting** | Kahneman & Tversky, «Intuitive prediction: biases and corrective procedures», *TIMS Studies in Management Science* 12:313–327 (1979) ✅ (cita coincidente en fuentes secundarias; sin registro de Crossref); Flyvbjerg, «From Nobel Prize to Project Management: Getting Risks Right», *Project Management Journal* (2006), doi:10.1177/875697280603700302 ✅ (Crossref; **corregido**: el DOI que había escrito antes apuntaba a otro artículo) | Estimar con la distribución de proyectos similares (vista externa) | "¿Cuánto tardará?" desde el historial de git/PRs del propio repo |
| X07 | **Design Structure Matrix** | Steward, «The design structure system: A method for managing the design of complex systems», *IEEE Trans. Eng. Mgmt* (1981), doi:10.1109/TEM.1981.6448589 ✅ (Crossref) | Matriz de dependencias, partición y agrupamiento | DSM desde el grafo de imports; módulos candidatos a separar, ciclos |
| X08 | **Diseño axiomático** | Nam P. Suh, *The Principles of Design* (1990) ✅ (Open Library) | Axioma de independencia y de información | Independencia de requisitos funcionales ↔ parámetros de diseño |
| X09 | **Matriz de Pugh** | Stuart Pugh, *Total Design* (Addison-Wesley, 1991; versión previa de la Univ. de Strathclyde, 1988) ✅ (Open Library; **corregido**: antes escribí 1990) | Comparar alternativas contra un dato de referencia | Elección de librería/arquitectura |
| X10 | **HAZOP (palabras guía)** | ICI (Reino Unido), años 60 (una fuente de la NTNU da 1963); Lawley (*CEP*, 1974); Kletz, *Hazop and Hazan* (1983); las fuentes discrepan sobre cuánto se debe a Kletz ✅ | Revisar desviaciones con palabras guía (no, más, menos, inverso, otro que…) | Revisión de APIs/flujos de datos: palabra guía × parámetro |
| X11 | **Bow-tie** | Primera mención en 1979, en apuntes de ICI en la Universidad de Queensland; adoptado por Shell a inicios de los años 90 tras Piper Alpha (1988) ✅ (varias fuentes secundarias; el origen exacto es incierto) | Barreras preventivas y de mitigación alrededor de un evento tope | Controles de seguridad de un servicio |
| X12 | **Robust Decision Making** | RAND (Lempert, Popper & Bankes), *Shaping the Next One Hundred Years* (2003), MR-1626 ✅ (Open Library, ISBN 9780833032751) <https://www.rand.org/pubs/monograph_reports/MR1626.html> (403 a scripts, no leída) | Decidir bajo incertidumbre profunda buscando robustez, no óptimo | Decisiones de plataforma con futuro incierto |
| X13 | **Apollo Root Cause Analysis** | Dean Gano, *Apollo Root Cause Analysis* (1999) ✅ (Open Library) | Causa-efecto con múltiples causas por efecto | Alternativa a 5 Whys |
| X14 | **Critical Chain** | Goldratt, *Critical Chain* (1997) ✅ (Open Library) | Buffers agregados al final del proyecto en vez de por tarea | Planificación con buffer de proyecto |
| X15 | **Diagramas de lazos causales / Dinámica de sistemas** | Forrester, *Industrial Dynamics* (1961) ✅ (Open Library) | Realimentación y retardos | Efectos de segundo orden de políticas de equipo |
| X16 | **QFD** | Yoji Akao (ed.), *Quality Function Deployment* (Productivity Press, 1990) ✅ (Open Library, ISBN 0915299410); el origen histórico del método no se verificó | Traducir voz del cliente a requisitos técnicos | Priorizar requisitos |
| X17 | **Team A / Team B** | CIA, experimento de 1976 ✅ (en *Tradecraft Primer*); Red Team Handbook p. 163 📖 | Dos equipos analizan por separado y confrontan | Dos agentes independientes proponen y se confrontan |
| X18 | **Value Stream Mapping** | Rother & Shook, *Learning to See* (Lean Enterprise Institute, 1999, ISBN 0966784308) ✅ (librerías; Open Library solo registra la versión 1.3 de 2003) | Mapear flujo de valor y esperas | Mapear idea→producción con tiempos de espera |
| X19 | **Taguchi (diseño robusto)** | Genichi Taguchi, *Introduction to Quality Engineering* (1986) ✅ (Open Library) | Reducir sensibilidad al ruido de las variables | Pruebas de robustez de configuración |

---

## Candidatas descartadas por falta de fuente verificable en esta sesión

F3EAD / kill chain, VSM de Beer como entrada propia (se subsume en X05), Gilb/Planguage y Event Tree Analysis. Se pueden reincorporar cuando haya fuente primaria comprobada.

## Recuento

| Familia | Entradas |
|---------|---------:|
| Militar | 11 |
| Industrial / Lean | 12 |
| Soviética / rusa | 6 |
| Ingeniería de sistemas | 8 |
| Decisión / pronóstico | 7 |
| Adicionales | 19 |
| **Total** | **63** |

---

## Resultado de la verificación de citas (2026-11-24)

La primera versión de este catálogo tenía **39 citas o afirmaciones marcadas ⚠** y **8 marcadas 🔒** (existen pero el servidor las bloquea). Recuento exacto tras la segunda pasada:

| Resultado | Cantidad | Detalle |
|-----------|---------:|---------|
| ⚠ → confirmadas (✅ o 📖) | **36** de 39 | Libros contra Open Library, artículos contra Crossref y afirmaciones de origen contra fuentes primarias o secundarias coincidentes (ver cada entrada) |
| …de ellas, leídas en el documento primario (📖) | 4 documentos | ADP 6-0 (2012), Heuer cap. 8 (copia de IALEIA), Boyd *Essence of Winning and Losing*, NASA *Fault Tree Handbook* |
| ⚠ que **siguen sin verificar** | **3** de 39 | (a) página exacta de Ohno (1988) para los «cinco porqués»; (b) fecha de creación del diagrama de Ishikawa (fuentes secundarias en conflicto: 1943 / años 60 / 1952); (c) texto primario ruso de los 76 estándares de Altshuller (solo hay fuentes secundarias) |
| 🔒 → confirmadas | **8** de 8 | Mitchell *et al.*, Mellers *et al.*, Kantorovich y Flyvbjerg por Crossref; Leveson y RAND MR-1626 por Open Library; las páginas de lean.org (2 entradas) existen según las búsquedas pero no se pudieron leer. Ninguna queda marcada 🔒 |
| Citas **eliminadas** | 0 | Las que no se pudieron confirmar se dejaron como ⚠ explícito en vez de borrarlas |
| Errores **corregidos** | 4 | (1) el DOI de Flyvbjerg tenía un dígito equivocado y apuntaba a otro artículo; (2) las «tareas clave» **no** están en la definición de intención del comandante de ADP 6-0 (2012); (3) *Total Design* de Pugh es de 1991 (Addison-Wesley; 1988 Strathclyde), no 1990; (4) *Guide to Quality Control* de Ishikawa tiene ediciones desde 1972 y la editorial APO no se confirmó |
| Hechos **matizados** por fuentes que discrepan | 3 | Auftragstaktik (origen discutido; Herrera 2022 contradice la atribución de ADP 6-0 2019 según el resumen), Western Electric (última regla de 8 puntos según la mayoría, 9 según una fuente), Jidoka/Toyoda (fechas ~1896–1897; el término se aplicó después) |

**Qué comprueba el script** (`python tools/verify_citations.py research/data/citation-checks.json`): 32 referencias, 26 libros en Open Library y 6 DOIs en Crossref. Resultado: 26 coincidencias exactas de título, autor y año; **6 con año distinto**, que se resolvieron a mano: Imai (el registro de 1986 existe; otro está mal fechado en 1970), Ishikawa (ediciones desde 1972), Weinstein & Adam (2008 confirmado por DOI de De Gruyter/Princeton; Open Library solo tiene *Guesstimation 2.0*), de Bono (1985 confirmado por Internet Archive y librerías), Pugh (corregido a 1991) y Rother & Shook (1999 confirmado por librerías; Open Library solo tiene la versión 1.3 de 2003).

**Límite que conviene recordar:** un ✅ de registro prueba que el libro o artículo *existe con ese autor y año*; no prueba que diga lo que el catálogo le atribuye. Solo los 4 documentos marcados 📖 (y los leídos en la primera pasada: TC 25-20, Red Team Handbook v5, extractos de Kepner-Tregoe y de la Fundación Altshuller) se leyeron.
