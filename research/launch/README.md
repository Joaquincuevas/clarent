# Lanzamiento: borradores (nada de esto está publicado)

Estado al 2026-11-26: el repo es público y `clarent-methods` 0.1.0 está en PyPI. Estos archivos son **borradores**; no se publicó nada.

| Archivo | Qué es |
|---|---|
| [`show-hn.md`](show-hn.md) | Título, texto y primer comentario para Show HN, con respuestas preparadas |
| [`reddit-claudeai.md`](reddit-claudeai.md) | Post para r/ClaudeAI |
| [`reddit-claudecode.md`](reddit-claudecode.md) | Post para r/ClaudeCode |
| [`reddit-python.md`](reddit-python.md) | Post para r/Python |
| [`social-preview.md`](social-preview.md) | Texto y diseño de la imagen de 1280×640 (no subida) |

## Qué está verificado y qué no

- **Show HN:** las reglas se leyeron en <https://news.ycombinator.com/showhn.html> el 2026-11-26 (se puede probar sin registro; no trivial; el autor debe estar para discutirlo; no pedir votos).
- **Reddit:** **no pude leer las reglas** de r/ClaudeAI, r/ClaudeCode ni r/Python (Reddit devuelve 403 a clientes automáticos, tanto en `about/rules.json` como en `old.reddit.com`). Lo que dicen los borradores sobre ellas es **memoria sin verificar**. Antes de publicar en cada una:
  1. abre `https://www.reddit.com/r/<sub>/about/rules` con tu sesión y lee la barra lateral y el wiki;
  2. busca reglas sobre autopromoción (proporción de posts propios, hilos semanales de proyectos), flair obligatorio, formato de "showcase", y divulgación de contenido hecho con IA;
  3. ajusta el borrador a lo que diga y borra el aviso "sin verificar" de arriba.

## Orden sugerido y cautelas

1. Un solo día, una sola cola de respuestas: publicar y quedarse a contestar (HN lo exige; Reddit lo premia).
2. Show HN primero (martes a jueves es preferencia no verificada). Reddit el mismo día o el siguiente, con textos distintos; no copiar y pegar el mismo post en tres comunidades.
3. No pedir votos a nadie, ni en privado.
4. Si el proyecto se construyó con ayuda de Claude Code, decirlo en el primer comentario: el repo ya declara el producto como integración con Claude Code, y que lo descubran después cuesta más que decirlo.
5. No prometer mejoras de rendimiento del agente (CLAUDE.md y el README lo prohíben sin un eval publicado). Todos los borradores se limitan a lo que el código hace y a lo que el README declara que no afirma.

## Hechos que los borradores usan (comprobables en el repo)

- 3 métodos implementados: `ach` (24 tests), `redteam` (82), `triz-matrix` (38); 8 más especificados, sin fecha.
- Solo biblioteca estándar, Python ≥ 3.11, sin dependencias de ejecución.
- `pip install clarent-methods`; plugin: `/plugin marketplace add Joaquincuevas/clarent`.
- Los ejemplos son sintéticos y están marcados.
- Matriz TRIZ: 29 de 1 248 celdas discutidas entre transcripciones; `DATA_LICENSE.md` documenta la cadena de titularidad incompleta.
- Las skills son de invocación manual (`disable-model-invocation`).
