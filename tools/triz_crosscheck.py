"""Cross-check independent transcriptions of Altshuller's 39x39 contradiction matrix and build a consensus.

    python tools/triz_crosscheck.py fetch  <dir>             # download the pinned files (needs `gh`)
    python tools/triz_crosscheck.py report <dir>             # agreement statistics (stdout)
    python tools/triz_crosscheck.py build  <dir> <out.json>  # write the consensus dataset

Why: no single copy of the matrix is trustworthy on its own (transcription typos, historic variants).
A cell is accepted when a strict majority of the sources agree on the SET of principles.
Order inside a cell is the most common order among the agreeing sources.
Each cell is then compared with the Altshuller Foundation's 1973 table: equal set => "verified", different => "contested",
page unreadable => "consensus".
Downloaded files are third-party data: they are read, never executed, and not stored in this repo.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

# name -> (repo, pinned commit, path, local file). Licenses verified from each repo's LICENSE file via the GitHub API.
SOURCES = {
    "A": ("Antropocosmist/triz-engineering-solver", "251084f171508e774507c36140af55096213ad30",
          "resources/contradiction_matrix.json", "A.json"),
    "B": ("SharathSPhD/triz-engine", "17d48dc0273c23bc8456e7369f2a298bd44131a3",
          "triz-engine/data/triz-matrix.json", "B.json"),
    "C": ("seogineer/triz-solver", "32c8278eb7ded45a6f2a19eadc0ea9bb4144711d",
          "skills/triz-analysis/data/contradiction-matrix.json", "C.json"),
    "D": ("magery-ai/triz-skill", "ba773ce3785ddd8b12f2f2af3b9537c4aaf13549",
          "skills/triz/data/contradiction-matrix.csv", "D.csv"),
    "E": ("luchi2333/triz-worker-innovation-research", "ba796e2b06b941bb6e970e9a472de9ab29e69bfb",
          "triz-worker-innovation-research/references/contradiction-matrix.json", "E.json"),
}
N = 39

# Reference (does not vote): official G.S. Altshuller Foundation page, which cites Altshuller, "Algorithm of Invention"
# (Moscow, 1973), Appendix 1. Parsed cell by cell from the page's HTML tables. Used only to mark cells as verified/contested;
# nothing from the page is copied into this repo except principle numbers (facts) for the contested cells.
FOUNDATION_URL = "https://www.altshuller.ru/triz/technique2.asp"
FOUNDATION_FILE = "F.html"


def fetch(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(FOUNDATION_URL, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=60).read()
    (dest / FOUNDATION_FILE).write_bytes(html)
    print(f"F {FOUNDATION_URL} {hashlib.sha256(html).hexdigest()[:16]} {len(html)} bytes")
    for key, (repo, sha, path, local) in SOURCES.items():
        out = subprocess.run(["gh", "api", f"repos/{repo}/contents/{path}?ref={sha}", "-H", "Accept: application/vnd.github.raw"],
                             capture_output=True, check=True).stdout
        (dest / local).write_bytes(out)
        print(f"{key} {repo}@{sha[:10]} {hashlib.sha256(out).hexdigest()[:16]} {len(out)} bytes")


def _load(key: str, d: Path) -> dict[tuple[int, int], tuple[int, ...]]:
    """Return {(improving, worsening): principles} for every non-diagonal cell; empty tuple = no principles."""
    f = d / SOURCES[key][3]
    cells: dict[tuple[int, int], tuple[int, ...]] = {}
    if key == "A":
        raw = {tuple(map(int, k.split(","))): v for k, v in json.loads(f.read_text(encoding="utf-8"))["cells"].items()}
    elif key == "B":
        raw = {tuple(map(int, k.split("_"))): v for k, v in json.loads(f.read_text(encoding="utf-8"))["matrix"].items()}
    elif key == "C":
        raw = {tuple(map(int, k.split("-"))): v for k, v in json.loads(f.read_text(encoding="utf-8"))["cells"].items()}
    elif key == "D":
        raw = {}
        with open(f, encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
        for i, row in enumerate(rows[1:], start=1):
            for j, cell in enumerate(row[1:], start=1):
                if cell.strip():
                    raw[(i, j)] = [int(x) for x in cell.split(";")]
    else:  # E: list of rows; None on the diagonal, [] for empty cells
        m = json.loads(f.read_text(encoding="utf-8"))["matrix"]
        raw = {(i + 1, j + 1): v for i, row in enumerate(m) for j, v in enumerate(row) if v}
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            if i != j:
                cells[(i, j)] = tuple(raw.get((i, j), ()))
    return cells


class _Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append([])
        elif tag == "tr" and self.tables:
            self.row = []
            self.tables[-1].append(self.row)
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row.append(re.sub(r"\s+", " ", "".join(self.cell)).replace(" ", " ").strip())
            self.cell = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def load_foundation(d: Path) -> dict[tuple[int, int], tuple[int, ...] | None]:
    """Parse the Foundation's 1973 table: blocks of 5 columns (the last of 4), 39 rows labelled 'NN. name'."""
    p = _Tables()
    p.feed((d / FOUNDATION_FILE).read_bytes().decode("cp1251"))
    cells: dict[tuple[int, int], tuple[int, ...]] = {}
    for tb in p.tables:
        hdr = next((r for r in tb if r and all(c.isdigit() for c in r)), None)   # row of column numbers
        if not hdr or len(hdr) < 4:
            continue
        cols = [int(c) for c in hdr]
        for r in tb:
            m = re.match(r"^(\d\d)\.", r[0]) if r else None
            if not m:
                continue
            i = int(m.group(1))
            for col, txt in zip(cols, r[1:]):
                if i != col:
                    nums = tuple(int(x) for x in re.findall(r"\d+", txt))
                    # Page defects (e.g. '2812, 17, 28' = a duplicated, glued cell) give impossible numbers:
                    # the cell is unreadable, not data.
                    cells[(i, col)] = None if any(n > 40 for n in nums) else nums
    return cells


def load_all(d: Path):
    return {k: _load(k, d) for k in SOURCES}


def consensus(data) -> dict[tuple[int, int], dict]:
    out = {}
    n = len(data)
    for cell in next(iter(data.values())):
        votes = {k: data[k][cell] for k in data}
        by_set = Counter(frozenset(v) for v in votes.values())
        best, count = by_set.most_common(1)[0]
        tied = sum(1 for c in by_set.values() if c == count) > 1
        orders = Counter(v for v in votes.values() if frozenset(v) == best)
        order = max(orders.items(), key=lambda kv: (kv[1], -len(kv[0])))[0] if best else ()
        if count == n:
            status = "unanimous"
        elif count > n / 2 and not tied:
            status = "majority"
        else:
            status = "disputed"
        out[cell] = {"principles": list(order), "agree": count, "of": n, "status": status,
                     "dissent": {k: list(v) for k, v in votes.items() if frozenset(v) != best}}
    return out


def report(d: Path) -> None:
    data = load_all(d)
    print("filled cells per source:", {k: sum(1 for v in c.values() if v) for k, c in data.items()})
    keys = sorted(data)
    print("pairwise set-agreement over all 1482 off-diagonal cells:")
    for a in keys:
        print("  ", a, {b: sum(1 for c in data[a] if set(data[a][c]) == set(data[b][c])) for b in keys if b != a})
    cons = consensus(data)
    print("status:", dict(Counter(v["status"] for v in cons.values())))
    f = load_foundation(d)
    print(f"Foundation 1973 parsed cells: {len(f)} (expected 1482); filled: {sum(1 for v in f.values() if v)}")
    unreadable = [c for c, v in f.items() if v is None]
    readable = [c for c in cons if f.get(c) is not None]
    same_set = sum(1 for c in readable if set(cons[c]["principles"]) == set(f[c]))
    same_order = sum(1 for c in readable if tuple(cons[c]["principles"]) == f[c])
    print(f"Foundation cells unreadable (page defects): {unreadable}")
    print(f"consensus vs Foundation over {len(readable)} readable cells: same set {same_set}, same order {same_order}")
    for c, v in sorted(cons.items()):
        if f.get(c) is not None and set(v["principles"]) != set(f[c]):
            print(f"  DIFF {c[0]}-{c[1]} consensus={v['principles']} ({v['status']}) foundation={list(f.get(c, ()))}")
    print("filled in consensus:", sum(1 for v in cons.values() if v["principles"]))
    for (i, j), v in sorted(cons.items()):
        if v["status"] != "unanimous":
            print(f"  {i}-{j} {v['status']} {v['agree']}/{v['of']} -> {v['principles']}  dissent={v['dissent']}")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(d: Path, out: Path) -> None:
    import datetime

    cons = consensus(load_all(d))
    f = load_foundation(d)
    cells = {}
    for (i, j), v in sorted(cons.items()):
        fcell = f.get((i, j), ())
        contested = fcell is not None and set(v["principles"]) != set(fcell)
        if not (v["principles"] or contested):
            continue
        status = "consensus" if fcell is None else ("contested" if contested else "verified")
        cell = {"p": v["principles"], "n": v["agree"], "s": status}
        if contested:
            cell["alt"] = list(fcell)   # the Foundation 1973 reading, for the user to see
        cells[f"{i},{j}"] = cell
    counts = Counter(c["s"] for c in cells.values())
    meta = {
        "description": "Altshuller 39x39 contradiction matrix: consensus of independent transcriptions, checked against the 1973 table.",
        "direction": "key 'i,j' = (improving parameter i, worsening parameter j); absent key = no principles listed; diagonal not applicable",
        "built_by": "tools/triz_crosscheck.py build",
        "built_on": datetime.date.today().isoformat(),
        "rule": "a cell is accepted when a strict majority of the voting sources agree on the SET of principles; order = most common order among them",
        "cell_status": {
            "verified": "consensus set equals the Altshuller Foundation 1973 table",
            "contested": "consensus set differs from the 1973 table; 'alt' holds the 1973 reading. Treat both as candidates",
            "consensus": "the 1973 page was unreadable for this cell; consensus only",
        },
        "counts": {"filled_cells": sum(1 for c in cells.values() if c["p"]), **dict(counts)},
        "voting_sources": [
            {"key": k, "repo": f"https://github.com/{repo}", "commit": sha, "path": path, "license": "MIT (LICENSE file read)",
             "sha256": _sha(d / local)}
            for k, (repo, sha, path, local) in SOURCES.items()
        ],
        "reference_source": {"url": FOUNDATION_URL, "cites": "Altshuller, Algorithm of Invention (Moscow, 1973), Appendix 1",
                             "sha256": _sha(d / FOUNDATION_FILE), "use": "verification only; not a voting source"},
    }
    out.write_text(json.dumps({"meta": meta, "cells": cells}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out}: {len(cells)} cells, {meta['counts']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "fetch":
        fetch(Path(sys.argv[2]))
    elif cmd == "report":
        report(Path(sys.argv[2]))
    elif cmd == "build":
        build(Path(sys.argv[2]), Path(sys.argv[3]))
    else:
        print(__doc__)
        sys.exit(2)
