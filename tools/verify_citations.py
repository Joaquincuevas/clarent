"""Check bibliographic citations against public registries and save the evidence.

    python tools/verify_citations.py research/data/citation-checks.json

Crossref (DOIs) and Open Library (books) accept scripts, unlike many publisher sites. A match means
"a bibliographic record with this title, author and year exists" (level `exists`); it does NOT mean the text was read.
A claim whose year or author does not match the record is reported as a MISMATCH and must be fixed in the catalog.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.parse
import urllib.request

UA = {"User-Agent": "clarent-citation-check/0.1 (open-source research tool)"}

# key: (kind, query, expected first-publication year or None, expected author fragment)
DOIS = {
    "mitchell-russo-pennington-1989": ("10.1002/bdm.3960020103", 1989, "mitchell"),
    "kantorovich-1960": ("10.1287/mnsc.6.4.366", 1960, "kantorovich"),
    "flyvbjerg-2006": ("10.1177/875697280603700302", 2006, "flyvbjerg"),
    "mellers-2014": ("10.1177/0956797614524255", 2014, "mellers"),
    "steward-1981": ("10.1109/TEM.1981.6448589", 1981, "steward"),
    "dalkey-helmer-1963": ("10.1287/mnsc.9.3.458", 1963, "dalkey"),
}
BOOKS = {
    "perla-art-of-wargaming": ("The Art of Wargaming", "Perla", 1990),
    "imai-kaizen": ("Kaizen", "Imai", 1986),
    "liker-toyota-way": ("The Toyota Way", "Liker", 2004),
    "ishikawa-guide-qc": ("Guide to Quality Control", "Ishikawa", 1976),
    "sobek-smalley-a3": ("Understanding A3 Thinking", "Sobek", 2008),
    "akao-hoshin-kanri": ("Hoshin Kanri", "Akao", 1991),
    "shingo-smed": ("A Revolution in Manufacturing", "Shingo", 1985),
    "shewhart-1931": ("Economic Control of Quality of Manufactured Product", "Shewhart", 1931),
    "shewhart-1939": ("Statistical Method from the Viewpoint of Quality Control", "Shewhart", 1939),
    "weinstein-adam-guesstimation": ("Guesstimation", "Weinstein", 2008),
    "tetlock-superforecasting": ("Superforecasting", "Tetlock", 2015),
    "debono-six-hats": ("Six Thinking Hats", "de Bono", 1985),
    "zwicky-morphological": ("Discovery, Invention, Research Through the Morphological Approach", "Zwicky", 1969),
    "beer-brain-of-the-firm": ("Brain of the Firm", "Beer", 1972),
    "suh-principles-of-design": ("The Principles of Design", "Suh", 1990),
    "pugh-total-design": ("Total Design", "Pugh", 1990),
    "gano-apollo-rca": ("Apollo Root Cause Analysis", "Gano", 1999),
    "goldratt-critical-chain": ("Critical Chain", "Goldratt", 1997),
    "forrester-industrial-dynamics": ("Industrial Dynamics", "Forrester", 1961),
    "akao-qfd": ("Quality Function Deployment", "Akao", 1990),
    "rother-shook-learning-to-see": ("Learning to See", "Rother", 1999),
    "taguchi-intro-quality-engineering": ("Introduction to Quality Engineering", "Taguchi", 1986),
    "ohno-tps": ("Toyota Production System", "Ohno", 1988),
    "shingo-zero-qc": ("Zero Quality Control", "Shingo", 1986),
    "heuer-pherson-sat": ("Structured Analytic Techniques for Intelligence Analysis", "Heuer", 2010),
    "altshuller-creativity": ("Creativity as an Exact Science", "Altshuller", 1984),
}


def get(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def check_doi(key, doi, year, author):
    try:
        m = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))["message"]
    except Exception as e:  # network or 404
        return {"key": key, "status": "ERROR", "detail": str(e)[:120]}
    issued = (m.get("issued", {}).get("date-parts") or [[None]])[0][0]
    authors = [a.get("family", "") for a in m.get("author", [])]
    ok = issued == year and any(author in a.lower() for a in authors)
    return {"key": key, "status": "MATCH" if ok else "MISMATCH", "doi": doi, "title": (m.get("title") or [""])[0],
            "year": issued, "authors": authors[:4], "journal": (m.get("container-title") or [""])[0]}


def check_book(key, title, author, year):
    q = urllib.parse.urlencode({"title": title, "author": author, "fields": "title,author_name,first_publish_year,key,isbn,publisher",
                                "limit": 15})
    try:
        docs = get("https://openlibrary.org/search.json?" + q).get("docs", [])
    except Exception as e:
        return {"key": key, "status": "ERROR", "detail": str(e)[:120]}
    stem = title.split(":")[0].strip().lower()

    def norm(t):
        return "".join(c for c in t.lower().split(":")[0] if c.isalnum() or c == " ").strip()

    has_author = lambda d: any(author.lower().replace("de bono", "bono") in a.lower() for a in d.get("author_name", []))
    exact = [d for d in docs if norm(d.get("title", "")) == norm(stem) and has_author(d)]
    loose = [d for d in docs if norm(stem) in norm(d.get("title", "")) and has_author(d)]
    hits = exact or loose
    if not hits:
        return {"key": key, "status": "NOT-FOUND", "title": title, "author": author, "expected_year": year}
    best = min(hits, key=lambda d: d.get("first_publish_year") or 9999)
    y = best.get("first_publish_year")
    return {"key": key, "status": "MATCH" if y == year else "YEAR-DIFFERS", "title": best["title"], "authors": best.get("author_name", [])[:3],
            "first_publish_year": y, "expected_year": year, "record": "https://openlibrary.org" + best["key"],
            "isbn_sample": (best.get("isbn") or [None])[0], "exact_title": bool(exact)}


def crossref_title(title, author):
    q = urllib.parse.urlencode({"query.bibliographic": f"{title} {author}", "rows": 3})
    return [(i["DOI"], (i.get("title") or [""])[0], (i.get("issued", {}).get("date-parts") or [[None]])[0][0],
             [a.get("family") for a in i.get("author", [])][:3]) for i in get("https://api.crossref.org/works?" + q)["message"]["items"]]


def main(out: str) -> int:
    results = []
    for k, (doi, y, a) in DOIS.items():
        results.append(check_doi(k, doi, y, a)); time.sleep(0.5)
    for k, (t, a, y) in BOOKS.items():
        results.append(check_book(k, t, a, y)); time.sleep(0.5)
    json.dump({"checked_on": time.strftime("%Y-%m-%d"), "results": results}, open(out, "w", encoding="utf-8", newline="\n"),
              indent=1, ensure_ascii=False)
    for r in results:
        print(f"{r['status']:<13} {r['key']:<38} {r.get('year') or r.get('first_publish_year') or ''} {r.get('title', '')[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
