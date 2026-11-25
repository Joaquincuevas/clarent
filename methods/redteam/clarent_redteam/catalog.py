"""The fixed catalog of attack classes, the rating rubrics and the severity bands.

Everything here is data the engine and the report rely on; changing it changes results, so it is covered by tests.

Provenance is stated per class (`origin`):
  * "handbook": the class applies a technique that the UFMCS Red Team Handbook v5 (15 Apr 2011) describes; `pages`
    are the printed page numbers I read.
  * "clarent": the class is Clarent's own adaptation to software work; the Handbook has no technique by that name.
The questions and rubrics below are Clarent's wording, not the Handbook's.
"""
from __future__ import annotations

CLASSES = ("key-assumptions", "failure-modes", "abuse", "scale", "dependency", "reversibility")

CATALOG: dict[str, dict] = {
    "key-assumptions": {
        "origin": "handbook",
        "pages": "Key Assumptions Check, p. 151-152; Validating Assumptions, p. 85-88",
        "en": {
            "name": "Key assumptions",
            "question": "What must be true for this to work, and has each of those things been checked?",
            "prompts": [
                "What does the text take for granted without saying so: inputs, ordering, who calls it, volume, environment?",
                "Is each assumption a fact, an opinion or a preconception? Is it needed at all, or can the plan work without it?",
                "What would change if it were wrong, and what would you see first?",
            ],
        },
        "es": {
            "name": "Supuestos clave",
            "question": "¿Qué tiene que ser cierto para que esto funcione, y se ha comprobado cada cosa?",
            "prompts": [
                "¿Qué da el texto por sentado sin decirlo: entradas, orden, quién llama, volumen, entorno?",
                "¿Cada supuesto es un hecho, una opinión o un prejuicio? ¿Hace falta, o el plan funciona sin él?",
                "¿Qué cambiaría si fuera falso y qué verías primero?",
            ],
        },
    },
    "failure-modes": {
        "origin": "handbook",
        "pages": "Pre-mortem Analysis, p. 138-140; \"What If?\" Analysis, p. 166-167",
        "en": {
            "name": "Failure modes",
            "question": "How does it fail, and what happens next?",
            "prompts": [
                "Imagine it has already failed in production: write down the reasons (pre-mortem).",
                "Which partial failures (timeout, duplicate, reordering, crash half-way) leave the system in an inconsistent state?",
                "Who would notice the failure, and how long would it take?",
            ],
        },
        "es": {
            "name": "Modos de falla",
            "question": "¿Cómo falla y qué pasa después?",
            "prompts": [
                "Imagina que ya falló en producción: escribe las razones (pre-mortem).",
                "¿Qué fallas parciales (timeout, duplicado, reordenamiento, caída a medias) dejan el sistema inconsistente?",
                "¿Quién notaría la falla y cuánto tardaría?",
            ],
        },
    },
    "abuse": {
        "origin": "handbook",
        "pages": "Red Team Analysis, p. 173-174 (adapted: the adversary is a hostile or careless user, not a state)",
        "en": {
            "name": "Abuse",
            "question": "How can someone use it in a way its author did not intend?",
            "prompts": [
                "Think as the adversary or the careless user: which input, sequence or permission breaks the rules?",
                "Who can call this, and what limits apply to them?",
                "What is exposed if one client, credential or tenant is hostile?",
            ],
        },
        "es": {
            "name": "Abuso",
            "question": "¿Cómo puede alguien usarlo de una forma que su autor no pensó?",
            "prompts": [
                "Piensa como el adversario o el usuario descuidado: ¿qué entrada, secuencia o permiso rompe las reglas?",
                "¿Quién puede llamarlo y qué límites tiene?",
                "¿Qué queda expuesto si un cliente, credencial o inquilino es hostil?",
            ],
        },
    },
    "scale": {
        "origin": "clarent",
        "pages": "no Handbook technique; closest in spirit: High-Impact/Low-Probability Analysis, p. 165",
        "en": {
            "name": "Scale",
            "question": "What breaks at 10x or 100x?",
            "prompts": [
                "Volume, cardinality, concurrency, payload size, number of tenants: which one grows and what is its limit?",
                "What is quadratic or unbounded (queues, retries, fan-out, memory, cost)?",
                "What happens during a burst rather than on average?",
            ],
        },
        "es": {
            "name": "Escala",
            "question": "¿Qué se rompe a 10x o 100x?",
            "prompts": [
                "Volumen, cardinalidad, concurrencia, tamaño de carga, número de inquilinos: ¿cuál crece y cuál es su límite?",
                "¿Qué es cuadrático o sin cota (colas, reintentos, fan-out, memoria, costo)?",
                "¿Qué pasa en una ráfaga y no en el promedio?",
            ],
        },
    },
    "dependency": {
        "origin": "clarent",
        "pages": "no Handbook technique; related: ADSO \"String of Pearls\", p. 140 (dependencies not in place, 2nd and 3rd order effects)",
        "en": {
            "name": "Dependency",
            "question": "What does it depend on that it does not control?",
            "prompts": [
                "External services, libraries, configuration, other teams, deploy order, clocks, credentials: which are assumed to be there?",
                "What happens when a dependency is slow, wrong, rate-limited or gone?",
                "Does the change make something else depend on it without that other thing knowing?",
            ],
        },
        "es": {
            "name": "Dependencia",
            "question": "¿De qué depende que no controla?",
            "prompts": [
                "Servicios externos, bibliotecas, configuración, otros equipos, orden de despliegue, relojes, credenciales: ¿cuáles se dan por presentes?",
                "¿Qué pasa si una dependencia está lenta, equivocada, limitada o ausente?",
                "¿El cambio hace que otra cosa dependa de esto sin que esa otra cosa lo sepa?",
            ],
        },
    },
    "reversibility": {
        "origin": "clarent",
        "pages": "no Handbook technique",
        "en": {
            "name": "Reversibility",
            "question": "If this is wrong, how do you go back?",
            "prompts": [
                "Is there a point of no return (migration, deletion, external side effect, sent message)?",
                "Can it be rolled back without losing data, and who does it, how fast?",
                "Does the rollback path still work after the rollout is complete?",
            ],
        },
        "es": {
            "name": "Reversibilidad",
            "question": "Si esto está mal, ¿cómo se vuelve atrás?",
            "prompts": [
                "¿Hay un punto sin retorno (migración, borrado, efecto externo, mensaje enviado)?",
                "¿Se puede deshacer sin perder datos, quién lo hace y en cuánto tiempo?",
                "¿El camino de vuelta sigue funcionando cuando el despliegue ya terminó?",
            ],
        },
    },
}

# Ratings the model assigns; both scales are 1..5. Clarent's own rubric (the Handbook has none).
RUBRIC = {
    "impact": {
        "en": {1: "cosmetic or a nuisance",
               2: "a feature degrades; users can work around it",
               3: "an incident with a known workaround",
               4: "data loss, a security exposure or a major outage, recoverable with effort",
               5: "irreversible data loss, a breach, or the whole product down"},
        "es": {1: "cosmético o una molestia",
               2: "una función se degrada; hay forma de evitarlo",
               3: "un incidente con solución conocida",
               4: "pérdida de datos, exposición de seguridad o caída mayor, recuperable con esfuerzo",
               5: "pérdida irreversible de datos, brecha, o todo el producto caído"},
    },
    "plausibility": {
        "en": {1: "needs several independent things to go wrong",
               2: "could happen, but nothing in the text suggests it",
               3: "plausible within a year of operation",
               4: "likely; a normal event for a system of this kind",
               5: "will happen, or is already happening"},
        "es": {1: "requiere que varias cosas independientes salgan mal",
               2: "podría pasar, pero nada en el texto lo sugiere",
               3: "plausible dentro de un año de operación",
               4: "probable; un evento normal en un sistema así",
               5: "va a pasar, o ya está pasando"},
    },
}

# risk = impact x effective plausibility (1..25). Severity bands: Clarent's own, not from any source.
SEVERITY_ORDER = ("S1", "S2", "S3", "S4")          # most to least severe
SEVERITY_MIN_RISK = {"S1": 20, "S2": 12, "S3": 6, "S4": 0}


def severity(risk: int) -> str:
    for s in SEVERITY_ORDER:
        if risk >= SEVERITY_MIN_RISK[s]:
            return s
    return "S4"


def at_least(sev: str, threshold: str) -> bool:
    """True if `sev` is as severe as `threshold` (S1 is the most severe)."""
    return SEVERITY_ORDER.index(sev) <= SEVERITY_ORDER.index(threshold)
