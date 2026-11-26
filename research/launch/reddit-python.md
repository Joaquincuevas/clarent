# r/Python (borrador)

> **Reglas sin verificar:** Reddit bloquea la lectura automática. Antes de publicar, lee las reglas y la barra lateral con tu sesión (ver [`README.md`](README.md)). De memoria, y **por confirmar**: r/Python pide un flair de proyecto ("Showcase") y un cuerpo con secciones del estilo *What My Project Does / Target Audience / Comparison*, y limita la autopromoción. Si hoy el formato es otro, ajusta; el borrador ya está redactado con esas secciones.

**Enfoque:** es un paquete Python, no un plugin. Claude solo se menciona de pasada. Lo que interesa a esta audiencia: stdlib-only, tests, diseño del motor.

## Título

```
Clarent: classic methods (ACH, red teaming, TRIZ) as stdlib-only Python CLI tools with deterministic engines
```

## Cuerpo

```
**What My Project Does**

Clarent packages three classic decision/engineering methods as command-line
tools that compute rather than just prompt:

- `clarent ach`: Heuer's Analysis of Competing Hypotheses (CIA). You give it
  hypotheses and evidence in a JSON file; it ranks hypotheses by inconsistency,
  flags evidence that doesn't discriminate, runs a sensitivity check, and
  recommends the next test.
- `clarent redteam`: checks attack findings against a design doc or PR; findings
  not quoted from the text are rejected.
- `clarent triz-matrix`: Altshuller's 1973 contradiction matrix lookup, with
  every cell verified against a public copy.

    pip install clarent-methods
    clarent ach init a.json && clarent ach score a.json

[GIF]

**Target Audience**

Developers who debug flaky tests or review designs and want a repeatable,
auditable procedure, and people building coding-agent tooling who want engines
an agent can't talk its way around. It is early (0.1.0), not production-critical.

**Comparison**

Collections of "thinking frameworks" exist, mostly as prompt files. The difference
here is a deterministic core per method (it scores, validates and can reject input)
with tests, and evidence discipline: every observed fact needs a reference. It also
ships as Claude Code skills, but the CLI works on its own.

**Details**

Python >= 3.11, standard library only (no runtime dependencies), Apache-2.0,
144 tests. Each method is a self-contained folder with a manifest, a card and
examples; `clarent doctor` validates them. Limits are in the README: no claim that
it makes an agent better at tasks, the TRIZ data has a documented incomplete chain
of title, and eight further methods are specs only.

https://github.com/Joaquincuevas/clarent

[Disclose here how it was built, including any use of AI tools.]

I'd like feedback on the engine/CLI structure (a method is a folder exposing
`register()` and `main(argv)`).
```

## Antes de publicar

- [ ] Confirmar reglas, flair y formato del cuerpo del subreddit.
- [ ] Rellenar la divulgación.
