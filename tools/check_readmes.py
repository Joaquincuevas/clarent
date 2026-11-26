"""Fail if README.md and README.es.md drift apart structurally.

    python tools/check_readmes.py

Headings are translated, so they are matched by an explicit id on each heading line:

    ## Install <!-- id: install -->

The check requires, in both files, the same sequence of (level, id) headings (headings inside code
fences are ignored), the same number of fenced code blocks, and the language links on the second line.
It compares structure, not wording: it cannot tell whether a translation is faithful.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {"en": ROOT / "README.md", "es": ROOT / "README.es.md"}
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
ID = re.compile(r"<!--\s*id:\s*([a-z0-9-]+)\s*-->")


def parse(path):
    headings, fences, problems, in_fence = [], 0, [], False
    lines = path.read_text(encoding="utf-8").splitlines()
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if not in_fence:
                fences += 1
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING.match(line)
        if not m:
            continue
        ident = ID.search(m.group(2))
        if not ident:
            problems.append(f"{path.name}:{n}: heading without '<!-- id: ... -->': {line.strip()}")
            continue
        headings.append((len(m.group(1)), ident.group(1), n))
    return headings, fences, lines, problems


def main():
    problems, parsed = [], {}
    for lang, path in FILES.items():
        if not path.is_file():
            problems.append(f"{path.name} is missing")
            continue
        parsed[lang] = parse(path)
        problems += parsed[lang][3]
    if len(parsed) == 2:
        (h_en, f_en, l_en, _), (h_es, f_es, l_es, _) = parsed["en"], parsed["es"]
        seq_en, seq_es = [(lv, i) for lv, i, _ in h_en], [(lv, i) for lv, i, _ in h_es]
        if seq_en != seq_es:
            only_en = [x for x in seq_en if x not in seq_es]
            only_es = [x for x in seq_es if x not in seq_en]
            if only_en:
                problems.append("only in README.md: " + ", ".join(f"{'#' * lv} {i}" for lv, i in only_en))
            if only_es:
                problems.append("only in README.es.md: " + ", ".join(f"{'#' * lv} {i}" for lv, i in only_es))
            if not (only_en or only_es):
                problems.append("same headings but a different order or level between README.md and README.es.md")
        if f_en != f_es:
            problems.append(f"fenced code blocks differ: README.md has {f_en}, README.es.md has {f_es}")
        if "README.es.md" not in " ".join(l_en[:4]):
            problems.append("README.md must link to README.es.md in its first lines")
        if "README.md" not in " ".join(l_es[:4]):
            problems.append("README.es.md must link to README.md in its first lines")
    if problems:
        print("README.md and README.es.md are out of sync:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"READMEs are in sync ({len(parsed['en'][0])} headings, {parsed['en'][1]} code blocks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
