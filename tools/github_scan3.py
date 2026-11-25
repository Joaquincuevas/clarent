"""Tercera pasada: consultas CORTAS (1-2 palabras, ver la corrección TRIZ de novelty.md).

Uso: python tools/github_scan3.py OUT.json [a3-hazop|redteam]      (por defecto: a3-hazop)
     p. ej. research/data/github-scan-a3-hazop.json, research/data/github-scan-redteam.json
Requiere `gh` autenticado. No envía nada salvo las cadenas de búsqueda.
"""
import datetime
import json
import subprocess
import sys
import time

QSETS = {
    "a3-hazop": [
        "a3 thinking", "a3 problem solving", "a3 report", "toyota a3",
        "hazop", "hazop api", "hazop software", "hazop guidewords", "hazop llm",
        "guide words deviation", "data flow hazop",
    ],
    "redteam": [
        "red team design", "red team skill", "red team review", "design review agent",
        "devil's advocate", "devils advocate skill", "key assumptions", "assumptions check",
        "premortem", "pre-mortem skill", "ufmcs", "red team handbook", "pr review adversarial",
    ],
}


def search(q):
    r = subprocess.run(
        ["gh", "api", "-X", "GET", "search/repositories", "-f", f"q={q}", "-f", "sort=stars", "-f", "per_page=8"],
        capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        return {"error": r.stderr[:200], "items": []}
    return {"total_count": json.loads(r.stdout)["total_count"],
            "items": [{"repo": i["full_name"], "stars": i["stargazers_count"], "pushed": i["pushed_at"][:10],
                       "archived": i["archived"], "lang": i["language"], "desc": (i["description"] or "")[:150]}
                      for i in json.loads(r.stdout)["items"]]}


if __name__ == "__main__":
    out = {"scanned_at": datetime.date.today().isoformat(), "results": {}}
    for q in QSETS[sys.argv[2] if len(sys.argv) > 2 else "a3-hazop"]:
        res = search(q)
        if "rate" in res.get("error", "").lower():
            time.sleep(60)
            res = search(q)
        out["results"][q] = res
        time.sleep(2.3)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
    print("DONE")
