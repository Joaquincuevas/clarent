"""`clarent` command: list methods, check their health, and delegate to a method's own CLI.

    clarent list [--format json]
    clarent doctor [method ...]
    clarent [--lang en|es] <method> <args...>     e.g.  clarent ach score analysis.json
"""
from __future__ import annotations

import json
import os
import sys

from . import __version__, registry

USAGE = """usage: clarent [--lang en|es] {list,doctor,<method>} ...

commands:
  list [--format json]     show the available methods
  doctor [method ...] [--fail-on-stale]
                           validate manifests, cards, skills and sources
  <method> ...             run a method's own CLI (try: clarent list)
"""


def _pop_lang(argv: list[str]) -> list[str]:
    out, i = [], 0
    while i < len(argv):
        if argv[i] == "--lang" and i + 1 < len(argv):
            os.environ["CLARENT_LANG"] = argv[i + 1]
            i += 2
        else:
            out.append(argv[i])
            i += 1
    return out


def _list(args: list[str]) -> int:
    methods = registry.discover()
    if args[:2] == ["--format", "json"]:
        print(json.dumps([{"id": m.id, "status": m.manifest.get("status"), "family": m.manifest.get("family"),
                           "summary": m.manifest.get("summary")} for m in methods], indent=2))
        return 0
    if not methods:
        print("no methods found (set CLARENT_METHODS_DIR?)", file=sys.stderr)
        return 1
    width = max(len(m.id) for m in methods)
    for m in methods:
        print(f"{m.id:<{width}}  {m.manifest.get('status', '?'):<9}  {m.manifest.get('summary', '')}")
    return 0


def _doctor(args: list[str]) -> int:
    fail_on_stale = "--fail-on-stale" in args
    args = [a for a in args if a != "--fail-on-stale"]
    methods = registry.discover()
    if args:
        methods = [m for m in methods if m.id in args]
        unknown = set(args) - {m.id for m in methods}
        if unknown:
            print(f"error: unknown method(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
    bad = 0
    for m in methods:
        problems, stale = registry.doctor(m), registry.stale_claims(m)
        print(f"{'FAIL' if problems or (stale and fail_on_stale) else 'ok  '} {m.id}")
        for p in problems:
            print(f"     - {p}")
        for w in stale:
            print(f"     ! {w}")
        bad += bool(problems) or (bool(stale) and fail_on_stale)
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    argv = _pop_lang(list(sys.argv[1:] if argv is None else argv))
    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        return 0
    if argv[0] == "--version":
        print(__version__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "list":
        return _list(rest)
    if cmd == "doctor":
        return _doctor(rest)
    for m in registry.discover():
        if m.id == cmd:
            return registry.get_main(m)(rest)
    print(f"error: unknown command or method {cmd!r}\n{USAGE}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
