"""Data model, loading and validation for the TRIZ contradiction matrix. Stdlib only.

Data files (see data/ and DATA_LICENSE.md):
  catalog.json  39 parameters and 40 principles, in English and Spanish, with software readings and examples
  matrix.json   cells "i,j" -> {p: [principle ids in order], n: sources agreeing, s: status, alt: 1973 reading}

Convention: i = parameter to IMPROVE (row), j = parameter that WORSENS (column).
"""
from __future__ import annotations

import difflib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from .i18n import get_lang, t

DATA_DIR = Path(__file__).resolve().parent / "data"
N_PARAMS, N_PRINCIPLES = 39, 40
STATUSES = ("verified", "contested", "consensus")


class TrizError(ValueError):
    """Invalid input or data (reported to the user without a traceback)."""


@dataclass(frozen=True)
class Param:
    id: int
    en: str
    es: str
    sw_en: str
    sw_es: str
    aliases: tuple[str, ...] = ()

    def name(self, lang: str | None = None) -> str:
        return self.es if (lang or get_lang()) == "es" else self.en

    def software(self, lang: str | None = None) -> str:
        return self.sw_es if (lang or get_lang()) == "es" else self.sw_en


@dataclass(frozen=True)
class Principle:
    id: int
    en: str
    es: str
    desc_en: str
    desc_es: str
    sw_en: str
    sw_es: str

    def name(self, lang: str | None = None) -> str:
        return self.es if (lang or get_lang()) == "es" else self.en

    def description(self, lang: str | None = None) -> str:
        return self.desc_es if (lang or get_lang()) == "es" else self.desc_en

    def example(self, lang: str | None = None) -> str:
        return self.sw_es if (lang or get_lang()) == "es" else self.sw_en


@dataclass(frozen=True)
class Cell:
    principles: tuple[int, ...]
    agree: int
    status: str
    alt: tuple[int, ...] | None = None


@dataclass(frozen=True)
class Matrix:
    params: dict[int, Param]
    principles: dict[int, Principle]
    cells: dict[tuple[int, int], Cell]
    meta: dict = field(default_factory=dict)
    source_dir: Path = DATA_DIR


def norm(s: str) -> str:
    """Lowercase, strip accents and punctuation, collapse spaces."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise TrizError(t("err_no_file", path=path))
    except json.JSONDecodeError as e:
        raise TrizError(t("err_bad_json", path=path, e=e))


def load(data_dir: Path | None = None) -> Matrix:
    """Load and validate the catalog and the matrix. `data_dir` may hold either or both files; missing ones fall back
    to the bundled data, so a user can supply only their own matrix.json."""
    d = Path(data_dir) if data_dir else DATA_DIR
    cat_path = d / "catalog.json" if (d / "catalog.json").is_file() else DATA_DIR / "catalog.json"
    mat_path = d / "matrix.json" if (d / "matrix.json").is_file() else DATA_DIR / "matrix.json"
    cat, raw = _read_json(cat_path), _read_json(mat_path)

    try:
        params = {p["id"]: Param(p["id"], p["en"], p["es"], p["sw_en"], p["sw_es"], tuple(p.get("aliases", ())))
                  for p in cat["parameters"]}
        principles = {p["id"]: Principle(p["id"], p["en"], p["es"], p["desc_en"], p["desc_es"], p["sw_en"], p["sw_es"])
                      for p in cat["principles"]}
    except (KeyError, TypeError) as e:
        raise TrizError(t("err_data", where=cat_path, msg=f"missing field {e}"))
    if sorted(params) != list(range(1, N_PARAMS + 1)):
        raise TrizError(t("err_data", where=cat_path, msg="parameters must have ids 1..39"))
    if sorted(principles) != list(range(1, N_PRINCIPLES + 1)):
        raise TrizError(t("err_data", where=cat_path, msg="principles must have ids 1..40"))

    cells: dict[tuple[int, int], Cell] = {}
    for key, c in raw.get("cells", {}).items():
        try:
            i, j = (int(x) for x in key.split(","))
            p = tuple(int(x) for x in c["p"])
            alt = tuple(int(x) for x in c["alt"]) if "alt" in c else None
            cell = Cell(p, int(c.get("n", 0)), c.get("s", "consensus"), alt)
        except (ValueError, KeyError, TypeError) as e:
            raise TrizError(t("err_data", where=f"{mat_path} cell {key!r}", msg=str(e)))
        if not (1 <= i <= N_PARAMS and 1 <= j <= N_PARAMS) or i == j:
            raise TrizError(t("err_data", where=mat_path, msg=f"cell {key!r} is outside the 39x39 off-diagonal grid"))
        if any(x not in principles for x in cell.principles + (cell.alt or ())):
            raise TrizError(t("err_data", where=mat_path, msg=f"cell {key!r} lists an unknown principle"))
        if len(set(cell.principles)) != len(cell.principles):
            raise TrizError(t("err_data", where=mat_path, msg=f"cell {key!r} repeats a principle"))
        if cell.status not in STATUSES:
            raise TrizError(t("err_data", where=mat_path, msg=f"cell {key!r} has unknown status {cell.status!r}"))
        cells[(i, j)] = cell
    return Matrix(params, principles, cells, raw.get("meta", {}), d)


def resolve(m: Matrix, query: str) -> tuple[Param, str]:
    """Map a user string to a parameter. Returns (param, how) with how in {'id','name','software'}.

    Order: number; exact name (either language, or alias); unique substring of a name; unique substring of the
    software reading. Anything ambiguous is an error that lists the candidates (never a silent guess).
    """
    q = str(query).strip()
    if q.isdigit():
        n = int(q)
        if n not in m.params:
            raise TrizError(t("err_param_id", q=q))
        return m.params[n], "id"
    nq = norm(q)
    if not nq:
        raise TrizError(t("err_param_not_found", q=q, close="-"))

    def names(p: Param) -> set[str]:
        return {norm(p.en), norm(p.es), *(norm(a) for a in p.aliases)}

    exact = [p for p in m.params.values() if nq in names(p)]
    if len(exact) == 1:
        return exact[0], "name"

    def pick(cands: list[Param], how: str):
        if len(cands) == 1:
            return cands[0], how
        if len(cands) > 1:
            raise TrizError(t("err_param_ambiguous", q=q, cands="; ".join(f"{p.id} {p.name()}" for p in cands)))
        return None

    sub = [p for p in m.params.values() if any(nq in n for n in names(p))]
    r = pick(sub, "name")
    if r:
        return r
    sw = [p for p in m.params.values() if nq in norm(p.sw_en) or nq in norm(p.sw_es)]
    r = pick(sw, "software")
    if r:
        return r
    pool = {norm(p.en): p for p in m.params.values()} | {norm(p.es): p for p in m.params.values()}
    close = [f"{pool[c].id} {pool[c].name()}" for c in difflib.get_close_matches(nq, pool, n=3, cutoff=0.4)]
    raise TrizError(t("err_param_not_found", q=q, close="; ".join(close) or "-"))
