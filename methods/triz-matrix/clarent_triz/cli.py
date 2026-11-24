"""TRIZ contradiction-matrix command line. Two ways to use it:
  - standalone:  python -m clarent_triz lookup Speed "Device complexity"
  - via core:    clarent triz-matrix lookup Speed "Device complexity"

Commands: lookup, rank, analyze, params, principles, info.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import engine, i18n, render
from .i18n import t
from .model import TrizError, load


def _template() -> dict:
    return {
        "title": t("t_title"),
        "context": t("t_context"),
        "pairs": [{"improving": "Speed", "worsening": "Device complexity", "note": ""}],
    }


def register(sub: argparse._SubParsersAction) -> None:
    def common(p, fmt=True):
        p.add_argument("--data", metavar="DIR", help="folder with your own matrix.json and/or catalog.json")
        if fmt:
            p.add_argument("--format", choices=("md", "json"), default="md")

    p = sub.add_parser("lookup", help="principles for one contradiction")
    p.add_argument("improving", help="parameter to improve: number, name (en/es) or a software word like 'latency'")
    p.add_argument("worsening", help="parameter that gets worse")
    common(p)
    p.set_defaults(func=_lookup)

    p = sub.add_parser("rank", help="rank principles across several contradictions")
    p.add_argument("--pair", action="append", required=True, metavar="IMPROVING:WORSENING")
    common(p)
    p.set_defaults(func=_rank)

    p = sub.add_parser("analyze", help="analyze a JSON file with several contradictions")
    p.add_argument("path")
    p.add_argument("--out", help="write the report to this file")
    common(p)
    p.set_defaults(func=_analyze)

    p = sub.add_parser("init", help="create an analysis template")
    p.add_argument("path")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=_init)

    for name, hlp in (("params", "list the 39 parameters"), ("principles", "list the 40 principles"),
                      ("info", "describe the bundled data and its provenance")):
        p = sub.add_parser(name, help=hlp)
        common(p, fmt=(name != "info"))
        p.set_defaults(func=globals()[f"_{name}"])


def _emit(a, text: str) -> int:
    out = getattr(a, "out", None)
    if out:
        Path(out).write_text(text, encoding="utf-8", newline="\n")
        print(f"report written to {out}")
    else:
        print(text)
    return 0


def _matrix(a):
    m = load(Path(a.data) if getattr(a, "data", None) else None)
    return m


def _lookup(a) -> int:
    m = _matrix(a)
    lk = engine.lookup(m, a.improving, a.worsening)
    if a.format == "json":
        return _emit(a, json.dumps(engine.lookup_dict(lk), indent=2, ensure_ascii=False))
    return _emit(a, render.lookup_markdown(lk, (a.improving, a.worsening)))


def _pairs_from_args(specs: list[str]) -> list[tuple[str, str]]:
    out = []
    for p in specs:
        if ":" not in p:
            raise TrizError(t("err_pair_syntax", p=p))
        a, b = p.split(":", 1)
        out.append((a.strip(), b.strip()))
    return out


def _rank(a) -> int:
    m = _matrix(a)
    pairs = _pairs_from_args(a.pair)
    an = engine.rank(m, pairs)
    if a.format == "json":
        return _emit(a, json.dumps(engine.analysis_dict(an), indent=2, ensure_ascii=False))
    return _emit(a, render.analysis_markdown(an, queries=pairs))


def _analyze(a) -> int:
    try:
        data = json.loads(Path(a.path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise TrizError(t("err_no_file", path=a.path))
    except json.JSONDecodeError as e:
        raise TrizError(t("err_bad_json", path=a.path, e=e))
    pairs_raw = data.get("pairs") if isinstance(data, dict) else None
    if not isinstance(pairs_raw, list) or not pairs_raw:
        raise TrizError(t("err_bad_input", path=a.path, msg=t("err_need_pairs")))
    pairs, notes = [], []
    for i, p in enumerate(pairs_raw):
        if not isinstance(p, dict) or not p.get("improving") or not p.get("worsening"):
            raise TrizError(t("err_bad_input", path=a.path, msg=t("err_pair_fields", i=i)))
        pairs.append((str(p["improving"]), str(p["worsening"])))
        notes.append(str(p.get("note", "")))
    an = engine.rank(_matrix(a), pairs)
    if a.format == "json":
        d = engine.analysis_dict(an)
        d["title"], d["context"] = data.get("title", ""), data.get("context", "")
        return _emit(a, json.dumps(d, indent=2, ensure_ascii=False))
    return _emit(a, render.analysis_markdown(an, str(data.get("title", "")), str(data.get("context", "")), notes, pairs))


def _init(a) -> int:
    path = Path(a.path)
    if path.exists() and not a.force:
        print(f"error: {path} already exists (use --force)", file=sys.stderr)
        return 2
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_template(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"template created: {path}")
    return 0


def _params(a) -> int:
    m = _matrix(a)
    if a.format == "json":
        return _emit(a, json.dumps([{"id": p.id, "name": p.name(), "software_reading": p.software()}
                                    for p in m.params.values()], indent=2, ensure_ascii=False))
    return _emit(a, render.params_markdown(m))


def _principles(a) -> int:
    m = _matrix(a)
    if a.format == "json":
        return _emit(a, json.dumps([engine.principle_dict(p) for p in m.principles.values()], indent=2, ensure_ascii=False))
    return _emit(a, render.principles_markdown(m))


def _info(a) -> int:
    m = _matrix(a)
    c = m.meta.get("counts", {})
    print(t("info_line", filled=c.get("filled_cells", len(m.cells)), verified=c.get("verified", 0),
            contested=c.get("contested", 0), consensus=c.get("consensus", 0), built=m.meta.get("built_on", "?")))
    print(t("info_sources", n=len(m.meta.get("voting_sources", []))))
    for s in m.meta.get("voting_sources", []):
        print(f"  {s['key']}  {s['repo']}  @{s['commit'][:10]}  {s['license']}")
    ref = m.meta.get("reference_source")
    if ref:
        print(f"  ref {ref['url']}  ({ref['cites']})")
    if getattr(a, "data", None):
        print(t("data_override", dir=a.data))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="clarent-triz", description="TRIZ contradiction matrix")
    ap.add_argument("--lang", choices=sorted(i18n.M), default=i18n.get_lang(),
                    help="output language (default: $CLARENT_LANG or en)")
    register(ap.add_subparsers(dest="cmd", required=True))
    args = ap.parse_args(argv)
    i18n.set_lang(args.lang)
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        return args.func(args)
    except TrizError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
