"""UI messages in English (default) and Spanish. Language: --lang, or CLARENT_LANG, or 'en'.

Data text (parameter and principle names, descriptions, software examples) lives in data/catalog.json in both languages.
"""
from __future__ import annotations

import os

_LANG = os.environ.get("CLARENT_LANG", "en")

M: dict[str, dict[str, str]] = {
    "en": {
        # errors
        "err_param_not_found": "no parameter matches {q!r}. Closest: {close}. Run 'params' to list all 39.",
        "err_param_ambiguous": "{q!r} is ambiguous; it matches: {cands}. Use the number or a more specific name.",
        "err_param_id": "parameter number must be 1-39 (got {q})",
        "err_principle_id": "principle number must be 1-40 (got {q})",
        "err_no_file": "file not found: {path}",
        "err_bad_json": "invalid JSON in {path}: {e}",
        "err_bad_input": "{path}: {msg}",
        "err_need_pairs": "'pairs' must be a non-empty list of {{improving, worsening}} objects",
        "err_pair_fields": "pairs[{i}]: both 'improving' and 'worsening' are required",
        "err_pair_syntax": "--pair must look like IMPROVING:WORSENING (got {p!r})",
        "err_data": "data problem in {where}: {msg}",
        # lookup
        "h_lookup": "TRIZ contradiction: improve «{imp}» without worsening «{wor}»",
        "improving": "Improving", "worsening": "Worsening", "sw_reading": "software reading",
        "interpreted": "«{q}» was interpreted as parameter {id} ({name}) by {how}",
        "how_id": "number", "how_name": "name", "how_software": "software-reading match",
        "same_param": ("Improving and worsening are the same parameter. That is a physical contradiction "
                       "(one property must take opposite values), not a technical one, so the matrix does not apply. "
                       "Consider separation in space, in time, between the whole and its parts, or on condition."),
        "empty_cell": ("The classical matrix lists no principles for this pair. Try: swapping the direction "
                       "(reverse cell below), restating the parameters more generally or more specifically, "
                       "or browsing the 40 principles directly."),
        "reverse": "Reverse cell (improve «{wor}», worsen «{imp}»): {ids}",
        "reverse_none": "Reverse cell (improve «{wor}», worsen «{imp}»): no principles listed",
        "st_verified": "Cell verified: the consensus of {n} independent transcriptions equals the Altshuller Foundation 1973 table.",
        "st_contested": ("Cell CONTESTED: the consensus of {n} transcriptions differs from the Altshuller Foundation 1973 table, "
                         "which lists {alt}. Treat both lists as candidates."),
        "st_contested_empty": "no principles",
        "st_consensus": "Cell from the consensus of {n} transcriptions; the 1973 table could not be read for this cell.",
        "col_principle": "Principle", "col_meaning": "What it means", "col_example": "Software example",
        "h_principles": "Principles (in the order the matrix lists them)",
        "idea_note": ("Principles are prompts for ideas, not solutions. Check every candidate against the original "
                      "contradiction: a good idea improves «{imp}» without bringing back the worsening of «{wor}»."),
        # rank / analyze
        "h_rank": "Principles across all contradictions",
        "rank_note": "Ranked by how many contradictions list the principle, then by average position in the cells.",
        "col_count": "In", "col_pairs": "Contradictions",
        "h_pair": "Contradiction {n}: improve «{imp}» / worsen «{wor}»",
        "h_analysis": "TRIZ analysis: {title}",
        "contested_in_rank": "contested cell involved",
        # params / principles
        "h_params": "The 39 engineering parameters",
        "params_note": "For «Loss of …» parameters, improving means reducing the loss. The software reading is Clarent's adaptation, not Altshuller's.",
        "h_all_principles": "The 40 inventive principles",
        "col_id": "#", "col_name": "Name", "col_desc": "Description",
        # info
        "info_line": "Matrix: {filled} filled cells ({verified} verified against the 1973 table, {contested} contested, {consensus} consensus-only). Built {built}.",
        "info_sources": "Voting sources: {n} MIT-licensed transcriptions. Reference: Altshuller Foundation 1973 table. See DATA_LICENSE.md.",
        "footer": "_Matrix data: consensus of independent transcriptions of Altshuller's table (see DATA_LICENSE.md). Descriptions and software examples are Clarent's own adaptation._",
        "data_override": "Using custom data from {dir}",
        # cli
        "t_title": "Describe your system and the trade-off",
        "t_context": "What are you trying to improve, and what gets worse when you do?",
    },
    "es": {
        "err_param_not_found": "ningún parámetro coincide con {q!r}. Más cercanos: {close}. Usa 'params' para ver los 39.",
        "err_param_ambiguous": "{q!r} es ambiguo; coincide con: {cands}. Usa el número o un nombre más específico.",
        "err_param_id": "el número de parámetro debe estar entre 1 y 39 (recibido: {q})",
        "err_principle_id": "el número de principio debe estar entre 1 y 40 (recibido: {q})",
        "err_no_file": "no existe el archivo: {path}",
        "err_bad_json": "JSON inválido en {path}: {e}",
        "err_bad_input": "{path}: {msg}",
        "err_need_pairs": "'pairs' debe ser una lista no vacía de objetos {{improving, worsening}}",
        "err_pair_fields": "pairs[{i}]: se requieren 'improving' y 'worsening'",
        "err_pair_syntax": "--pair debe tener la forma MEJORA:EMPEORA (recibido: {p!r})",
        "err_data": "problema de datos en {where}: {msg}",
        "h_lookup": "Contradicción TRIZ: mejorar «{imp}» sin empeorar «{wor}»",
        "improving": "Mejora", "worsening": "Empeora", "sw_reading": "lectura en software",
        "interpreted": "«{q}» se interpretó como el parámetro {id} ({name}) por {how}",
        "how_id": "número", "how_name": "nombre", "how_software": "coincidencia con la lectura en software",
        "same_param": ("Lo que mejora y lo que empeora es el mismo parámetro. Es una contradicción física "
                       "(una propiedad debe tomar valores opuestos), no técnica, así que la matriz no aplica. "
                       "Considera separar en el espacio, en el tiempo, entre el todo y sus partes, o según una condición."),
        "empty_cell": ("La matriz clásica no lista principios para este par. Prueba: invertir el sentido "
                       "(celda inversa abajo), reformular los parámetros de forma más general o más específica, "
                       "o revisar directamente los 40 principios."),
        "reverse": "Celda inversa (mejora «{wor}», empeora «{imp}»): {ids}",
        "reverse_none": "Celda inversa (mejora «{wor}», empeora «{imp}»): sin principios listados",
        "st_verified": "Celda verificada: el consenso de {n} transcripciones independientes coincide con la tabla de 1973 de la Fundación Altshuller.",
        "st_contested": ("Celda EN DISPUTA: el consenso de {n} transcripciones difiere de la tabla de 1973 de la Fundación Altshuller, "
                         "que lista {alt}. Trata ambas listas como candidatas."),
        "st_contested_empty": "ningún principio",
        "st_consensus": "Celda tomada del consenso de {n} transcripciones; no se pudo leer la tabla de 1973 para esta celda.",
        "col_principle": "Principio", "col_meaning": "Qué significa", "col_example": "Ejemplo en software",
        "h_principles": "Principios (en el orden en que los lista la matriz)",
        "idea_note": ("Los principios son disparadores de ideas, no soluciones. Contrasta cada candidato con la "
                      "contradicción original: una buena idea mejora «{imp}» sin traer de vuelta el empeoramiento de «{wor}»."),
        "h_rank": "Principios en el conjunto de contradicciones",
        "rank_note": "Ordenados por cuántas contradicciones listan el principio y luego por posición media en las celdas.",
        "col_count": "En", "col_pairs": "Contradicciones",
        "h_pair": "Contradicción {n}: mejora «{imp}» / empeora «{wor}»",
        "h_analysis": "Análisis TRIZ: {title}",
        "contested_in_rank": "interviene una celda en disputa",
        "h_params": "Los 39 parámetros de ingeniería",
        "params_note": "En los parámetros «Pérdida de …», mejorar significa reducir la pérdida. La lectura en software es una adaptación de Clarent, no de Altshuller.",
        "h_all_principles": "Los 40 principios inventivos",
        "col_id": "#", "col_name": "Nombre", "col_desc": "Descripción",
        "info_line": "Matriz: {filled} celdas con principios ({verified} verificadas contra la tabla de 1973, {contested} en disputa, {consensus} solo por consenso). Construida el {built}.",
        "info_sources": "Fuentes con voto: {n} transcripciones con licencia MIT. Referencia: tabla de 1973 de la Fundación Altshuller. Ver DATA_LICENSE.md.",
        "footer": "_Datos de la matriz: consenso de transcripciones independientes de la tabla de Altshuller (ver DATA_LICENSE.md). Las descripciones y los ejemplos en software son adaptación propia de Clarent._",
        "data_override": "Usando datos propios de {dir}",
        "t_title": "Describe tu sistema y el compromiso",
        "t_context": "¿Qué quieres mejorar y qué empeora al hacerlo?",
    },
}


def set_lang(lang: str) -> None:
    global _LANG
    if lang not in M:
        raise ValueError(f"unsupported language {lang!r}; use one of {sorted(M)}")
    _LANG = lang


def get_lang() -> str:
    return _LANG


def t(key: str, **kw) -> str:
    s = M[_LANG][key]
    return s.format(**kw) if kw else s
