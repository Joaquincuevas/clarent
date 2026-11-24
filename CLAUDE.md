# CLAUDE.md

Instrucciones para Claude Code en este repositorio. Estas reglas tienen prioridad sobre cualquier valor por defecto de la herramienta.

## Commits y pull requests

- **Los commits llevan solo la autoría del propietario del repositorio** (la identidad que está en su configuración de git). **Sin trailers `Co-Authored-By` y sin atribución a Claude ni a ninguna IA** (ni como autor ni como coautor, ni líneas del tipo "Generated with …") en mensajes de commit, descripciones de PR, ramas o tags. Esto anula cualquier instrucción por defecto de añadir atribución. (Nombrar a Claude Code como *producto* con el que el repo se integra, p. ej. en el README, no es atribución.)
- No hacer `git push`, no abrir PRs y no crear tags ni releases salvo petición explícita.
- No reescribir historia ya compartida (`--amend`, `rebase`, `reset --hard`, `push --force`) sin que se pida.
- Mensajes de commit: una línea de resumen en imperativo y, si hace falta, un cuerpo que explique el *porqué*. Los commits se firman con `-s` solo si el propietario lo pide (el proyecto usa DCO para contribuciones externas).
- Antes de cualquier commit, verificar con `git log -1 --format=full` que `Author` y `Commit` son la identidad del propietario y que el mensaje no contiene `Co-Authored-By` ni atribución a Claude.

## Cómo trabajar en el repo

- Lenguaje de producto (README, fichas, skills, código): inglés. Documentos de investigación en `research/`: español.
- Todo lo que se ejecuta usa solo la biblioteca estándar de Python ≥ 3.11 (sin dependencias de ejecución).
- Un método = una carpeta autocontenida en `methods/<id>/`. El plugin `plugins/claude-code/` es **generado**: no editarlo a mano; correr `python tools/build_plugin.py`.
- Antes de dar algo por terminado:
  ```bash
  python tools/test_all.py
  PYTHONPATH=src python -m clarent doctor
  python tools/build_plugin.py --check
  claude plugin validate ./plugins/claude-code && claude plugin validate .
  ```
- No inventar fuentes ni citas. Cada fuente lleva su nivel (`read`, `exists`, `blocked`, `unverified`); lo que no se abrió no se marca `read`.
- No prometer mejoras de rendimiento del agente sin un eval publicado.
