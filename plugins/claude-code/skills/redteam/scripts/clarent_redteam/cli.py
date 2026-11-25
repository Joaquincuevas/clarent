"""Red team command line. Two ways to use it:
  - standalone:  python -m clarent_redteam check findings.json
  - via core:    clarent redteam check findings.json   (the core calls `register`)

Exit codes: 0 ok · 1 something actionable (a finding was rejected, --fail-on reached, --strict with warnings) · 2 invalid input.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import engine, i18n, render
from .catalog import CATALOG, CLASSES, RUBRIC, SEVERITY_ORDER, at_least
from .i18n import t
from .model import MIN_QUOTE_CHARS, SCHEMA, RedTeamError, parse


def _load(a):
    try:
        data = json.loads(Path(a.path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RedTeamError(t("err_no_file", path=a.path))
    except json.JSONDecodeError as e:
        raise RedTeamError(t("err_bad_json", path=a.path, e=e))
    root = Path(a.root) if getattr(a, "root", None) else None
    return parse(data, Path(a.path).resolve().parent, root=root, targets=getattr(a, "target", None) or None)


def _add_common(p: argparse.ArgumentParser) -> None:
    p.add_argument("path", help="findings file (JSON)")
    p.add_argument("--target", action="append", metavar="FILE",
                   help="read this file as the target instead of target.files (repeatable)")
    p.add_argument("--root", help="folder where file:line refs are resolved (default: the file's \"root\", else its own folder)")


def register(sub: argparse._SubParsersAction) -> None:
    """Register the subcommands on a parser (core or standalone)."""
    p = sub.add_parser("init", help="create a findings template for a target file")
    p.add_argument("path")
    p.add_argument("--target", required=True, metavar="FILE", help="the design doc, description or diff to attack")
    p.add_argument("--kind", choices=("design", "pr"), default="design")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=_init)

    p = sub.add_parser("validate", help="parse the file and say which findings the engine would reject")
    _add_common(p)
    p.set_defaults(func=_validate)

    p = sub.add_parser("check", help="reject unbacked findings, score the rest and print the report")
    _add_common(p)
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--out", help="write the report to this file")
    p.add_argument("--strict", action="store_true", help="exit 1 also when there are warnings")
    p.add_argument("--fail-on", metavar="S1|S2|S3|S4", help="exit 1 if an accepted attack is at least this severe")
    p.set_defaults(func=_check)

    p = sub.add_parser("top", help="print only the top attacks, one line each")
    _add_common(p)
    p.set_defaults(func=_top)

    p = sub.add_parser("catalog", help="print the fixed attack classes, their guiding questions and the rating scales")
    p.set_defaults(func=_catalog)


def _out(text: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(text)


def _init(a) -> int:
    path = Path(a.path)
    if path.exists() and not a.force:
        print("error: " + t("err_exists", path=path), file=sys.stderr)
        return 2
    tgt = Path(a.target)
    try:
        text = tgt.read_text(encoding="utf-8", errors="replace")
    except OSError:
        raise RedTeamError(t("target_missing", path=a.target))
    quote = next((" ".join(l.split()) for l in text.splitlines() if len(" ".join(l.split())) >= MIN_QUOTE_CHARS), "")
    if not quote:
        raise RedTeamError(t("init_no_quote", path=a.target, n=MIN_QUOTE_CHARS))
    # root = the folder refs and target paths are resolved from: the current folder when the target is inside it
    # (the usual case: findings under .clarent/redteam/, run from the repo root), else the target's own folder.
    here = Path.cwd().resolve()
    try:
        tgt.resolve().relative_to(here)
        root_abs = here
    except ValueError:
        root_abs = tgt.resolve().parent
    try:
        root = os.path.relpath(root_abs, path.resolve().parent).replace("\\", "/")
    except ValueError:                      # different drive on Windows
        root = str(root_abs)
    rel = tgt.resolve().relative_to(root_abs).as_posix()
    data = {
        "schema": SCHEMA,
        "title": t("t_title"),
        "root": root,
        "target": {"kind": a.kind, "files": [rel]},
        "assumptions": [{"id": "A1", "text": t("t_assumption"), "quote": quote, "status": "unverified",
                         "check": t("t_check")}],
        "attacks": [{"id": "X1", "class": "failure-modes", "assumption": "A1", "quote": quote, "attack": t("t_attack"),
                     "impact": 3, "plausibility": 3, "check": t("t_check")}],
        "skipped_classes": [],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(t("template_created", path=path))
    return 0


def _validate(a) -> int:
    f = _load(a)
    res = engine.analyze(f)
    for w in res.warnings:
        print("warning: " + w)
    for r in res.rejections:
        print(f"rejected {t('kind_' + r.kind)} {r.id}: {r.detail}")
    print(t("valid_ok", a=len(res.assumptions), x=len(res.attacks), r=len(res.rejections)))
    return 1 if res.rejections else 0


def _check(a) -> int:
    if a.fail_on and a.fail_on.upper() not in SEVERITY_ORDER:
        raise RedTeamError(t("err_bad_severity"))
    f = _load(a)
    res = engine.analyze(f)
    out = (json.dumps(engine.to_dict(res, f.title), indent=2, ensure_ascii=False)
           if a.format == "json" else render.markdown(f, res))
    if a.out:
        Path(a.out).write_text(out, encoding="utf-8")
        print(t("report_written", path=a.out))
    else:
        _out(out)
    code = 1 if res.rejections else 0
    if a.strict and res.warnings:
        code = 1
    if a.fail_on and any(at_least(x.severity, a.fail_on.upper()) for x in res.attacks):
        code = 1
    return code


def _top(a) -> int:
    f = _load(a)
    res = engine.analyze(f)
    if not res.top:
        print(t("top_none"))
        return 1
    for x in res.top:
        print(t("top_line", rank=x.rank, id=x.id, sev=x.severity, risk=x.risk, cls=x.class_id, text=x.text))
    return 1 if res.rejections else 0


def _catalog(a) -> int:
    lang = i18n.get_lang()
    L = []
    for i, c in enumerate(CLASSES, 1):
        e = CATALOG[c]
        L.append(t("catalog_head", i=i, id=c, name=e[lang]["name"], origin=e["origin"]))
        L.append("   " + e[lang]["question"])
        L += ["   - " + p for p in e[lang]["prompts"]]
        L.append(t("catalog_source", pages=e["pages"]))
    for key in ("impact", "plausibility"):
        L += ["", t("rubric_head", key=key)]
        L += [f"   {n}: {txt}" for n, txt in RUBRIC[key][lang].items()]
    _out("\n".join(L))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="clarent-redteam", description="Red team: attack a design or a PR with a fixed catalog")
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
    except RedTeamError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
