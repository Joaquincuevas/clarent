"""ACH command line. Two ways to use it:
  - standalone:  python -m clarent_ach score file.json
  - via core:    clarent ach score file.json   (the core calls `register`)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import engine, i18n, render
from .i18n import t
from .model import ACHError, parse


def _template() -> dict:
    return {
        "title": t("t_title"),
        "question": t("t_question"),
        "hypotheses": [
            {"id": "H1", "text": t("t_h1")},
            {"id": "H2", "text": t("t_h2")},
            {"id": "H3", "text": t("t_h3"), "catch_all": True},
        ],
        "evidence": [
            {"id": "E1", "text": t("t_e1"), "status": "observed", "credibility": "high",
             "relevance": "high", "ref": t("t_e1_ref"), "ratings": {"H1": "C", "H2": "I", "H3": "N"}},
            {"id": "T1", "text": t("t_t1"), "status": "proposed", "cost": "low",
             "ratings": {"H1": "CC", "H2": "II", "H3": "N"}},
        ],
    }


def _load(path: str, strict: bool):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ACHError(t("err_no_file", path=path))
    except json.JSONDecodeError as e:
        raise ACHError(t("err_bad_json", path=path, e=e))
    return parse(data, strict=strict)


def register(sub: argparse._SubParsersAction) -> None:
    """Register ACH subcommands on a parser (core or standalone)."""
    p = sub.add_parser("init", help="create an analysis template")
    p.add_argument("path")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=_init)

    for name, hlp in (("validate", "validate the file"), ("score", "score and print the report"),
                      ("next", "list only the recommended tests")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("path")
        p.add_argument("--strict", action="store_true", help="treat warnings as errors")
        if name == "score":
            p.add_argument("--format", choices=("md", "json"), default="md")
            p.add_argument("--out", help="write the report to this file")
        p.set_defaults(func=globals()[f"_{name}"])


def _init(a) -> int:
    path = Path(a.path)
    if path.exists() and not a.force:
        print("error: " + t("err_exists", path=path), file=sys.stderr)
        return 2
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_template(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(t("template_created", path=path))
    return 0


def _validate(a) -> int:
    an = _load(a.path, a.strict)
    for w in an.warnings:
        print(t("warn_prefix", w=w))
    print(t("validate_ok", h=len(an.hypotheses), o=len(an.observed), p=len(an.proposed)))
    return 0


def _score(a) -> int:
    an = _load(a.path, a.strict)
    res = engine.score(an)
    out = (json.dumps(engine.to_dict(res), indent=2, ensure_ascii=False)
           if a.format == "json" else render.markdown(an, res))
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
        print(t("report_written", path=a.out))
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(out)
    return 0


def _next(a) -> int:
    an = _load(a.path, a.strict)
    res = engine.score(an)
    if not res.next_tests:
        print(t("no_tests"))
        return 1
    for x in res.next_tests:
        print(t("next_line", id=x.id, p=x.priority, f=",".join(x.separates) or "-",
                a=",".join(x.against) or "-") + f"\n    {x.text}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="clarent-ach", description="Analysis of Competing Hypotheses")
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
    except ACHError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
