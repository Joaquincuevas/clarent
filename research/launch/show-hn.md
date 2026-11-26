# Show HN (borrador)

Reglas leídas el 2026-11-26 en <https://news.ycombinator.com/showhn.html>: se puede probar ya y sin registro, no trivial, el autor está para discutirlo, sin pedir votos. Un Show HN no es un post de blog: el enlace va al repo, no a un artículo.

## Título (≤ 80 caracteres)

```
Show HN: Clarent – CIA's ACH and other classic methods as debugging CLI tools
```

Alternativa más literal: `Show HN: Clarent – Analysis of Competing Hypotheses as a CLI for flaky bugs`

URL: `https://github.com/Joaquincuevas/clarent`

## Primer comentario (publicarlo uno mismo justo después de enviar)

```
Hi HN. Clarent turns a few classic methods (Heuer's Analysis of Competing
Hypotheses from the CIA, a red-team attack catalog from the US Army's UFMCS
handbook, Altshuller's TRIZ contradiction matrix) into small stdlib-only
Python tools. They also ship as manual-only Claude Code skills, but the CLI is
the point and works without any agent.

The rule I set myself: every method needs a deterministic core, something the
code computes or rejects without an LLM. A model (or you) proposes hypotheses
and evidence; the engine scores them, checks the evidence is anchored, and can
say no. Examples:

- `clarent ach score analysis.json` ranks competing causes by *inconsistency*
  (not probability), flags evidence that doesn't discriminate between them and
  proposes the next most informative test.
- `clarent redteam check findings.json` rejects attack findings that don't
  quote the document they attack.
- `clarent triz-matrix lookup latency "Device complexity"` returns the
  inventive principles for that contradiction; each matrix cell is checked
  against the 1973 table.

Try it with just pip:

    pip install clarent-methods
    clarent ach init a.json && clarent ach score a.json

(`init` writes an editable template; the worked flaky-test example is
methods/ach/examples/flaky-test.json in the repo, synthetic and labelled so). Python >= 3.11, no dependencies,
Apache-2.0. 144 tests across the three methods.

What it does not do, from the README: it does not claim to make an agent solve
more tasks (there is no eval yet; I will publish one, null or not), the TRIZ
data has an incomplete chain of title (29 of 1,248 cells are contested between
transcriptions; DATA_LICENSE.md has the details), and eight more methods are
specs only.

[Disclose here how the project was built, including any use of Claude Code.]

I'd especially like to hear: which method would you want next, and where the
"deterministic core" idea breaks down.
```

## Respuestas preparadas

- **"Isn't this just a prompt?"** No: the scoring, validation and rejection run with no LLM (`methods/*/clarent_*/engine.py`, tests in `methods/*/tests/`). The skill is a thin wrapper that tells an agent to use the CLI.
- **"Why would the CIA matter for debugging?"** ACH was designed against confirmation bias: you score evidence against *all* hypotheses and look at what is inconsistent, instead of collecting support for your favourite. Flaky bugs are the same trap.
- **"Does it make Claude better at fixing bugs?"** Not claimed. No eval yet; the README says so.
- **"Is the TRIZ matrix yours?"** It is Altshuller's (1973). Clarent ships transcriptions verified cell by cell against a public copy, with `DATA_LICENSE.md` explaining what is and is not established; you can pass your own with `--data`.
- **"Why not just use X (a bigger skills repo)?"** Those give an agent a checklist; this adds an engine that can refuse. They are complementary.

## Antes de enviar

- [ ] Rellenar la línea de divulgación (cómo se construyó).
- [ ] Comprobar que `pip install clarent-methods && clarent ach init a.json && clarent ach score a.json` funciona en un venv limpio el mismo día (verificado el 2026-11-26 con 0.1.0).
- [ ] Tener libre las 3–4 horas siguientes para contestar.
