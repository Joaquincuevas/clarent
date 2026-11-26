# r/ClaudeAI (borrador)

> **Reglas sin verificar:** Reddit bloquea la lectura automática. Antes de publicar, lee las reglas del subreddit con tu sesión (ver [`README.md`](README.md)). Lo siguiente es lo que esperaría encontrar y debes confirmar: flair obligatorio para proyectos propios, límite o formato para autopromoción, y divulgación de que lo construiste con Claude. Si el subreddit tiene un hilo semanal de proyectos y exige usarlo, publica ahí.

**Enfoque:** público general de Claude, no necesariamente desarrolladores. Contar el *problema* (un agente que confirma su primera hipótesis) y mostrar el GIF; el repo va en el cuerpo, no en el título.

## Título

```
I made a Claude Code skill that makes the agent score competing bug causes with the CIA's ACH method (plus a CLI that refuses to be talked into things)
```

## Cuerpo

```
When I debug flaky tests with an agent, it tends to pick the first plausible
cause and then collect evidence that agrees with it. Intelligence analysts have
a method designed against exactly that: Analysis of Competing Hypotheses
(Heuer, CIA). You list *all* the rival causes, rate each piece of evidence
against *every* one of them, and look at what is inconsistent rather than what
is supportive.

I turned it into a small tool: a manual-only Claude Code skill plus a plain CLI.
The agent proposes hypotheses and gathers evidence by running commands; the CLI
does the scoring, flags evidence that doesn't discriminate, and suggests the
next test most worth running. The scoring runs in code, no LLM involved, and the
report says what it is: a ranking of inconsistencies, not a probability.

[GIF: clarent ach on the flaky-test example]

There are two more methods (a red-team pass over a design doc or PR, and a
TRIZ contradiction matrix lookup). Install:

    pip install clarent-methods
    # in Claude Code:
    /plugin marketplace add Joaquincuevas/clarent
    /plugin install clarent-methods@clarent

Honest limits: I have no eval showing it makes Claude fix more bugs, and the
README says so. The skills are manual-only (they cost no context until you call
them). It has only been validated with Claude Code, not Cursor/Codex.

Repo: https://github.com/Joaquincuevas/clarent
[Disclose here: built with / without Claude Code, and how.]

Which classic method would you want as a tool next?
```

## Antes de publicar

- [ ] Confirmar reglas y flair del subreddit.
- [ ] Subir el GIF (`docs/demo/ach.gif`) como imagen del post si el subreddit lo permite; si no, enlazarlo.
- [ ] Rellenar la divulgación.
