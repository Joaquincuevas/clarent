"""Genera la tabla de ranking desde research/data/scores.csv.

Puntaje ponderado = (1.5*N + 1.5*U + 1*E + 1*V + 1*C) / 6  (escala 1-5).
Desempate: mayor novedad, luego mayor utilidad, luego id.
Uso: python tools/rank.py research/data/scores.csv > tabla.md
"""
import csv
import sys

W = {"N": 1.5, "U": 1.5, "E": 1.0, "V": 1.0, "C": 1.0}


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in W:
            r[k] = int(r[k])
            assert 1 <= r[k] <= 5, (r["id"], k)
        r["total"] = round(sum(W[k] * r[k] for k in W) / sum(W.values()), 2)
        r["raw"] = sum(r[k] for k in W)
    rows.sort(key=lambda r: (-r["total"], -r["N"], -r["U"], r["id"]))
    return rows


def table(rows, limit=None):
    out = ["| # | ID | Metodología | Familia | N | U | E | V | C | Σ | Ponderado | Estado en GitHub |",
           "|--:|----|-------------|---------|--:|--:|--:|--:|--:|--:|----------:|------------------|"]
    for i, r in enumerate(rows[:limit], 1):
        out.append(f"| {i} | {r['id']} | {r['metodologia']} | {r['familia']} | {r['N']} | {r['U']} | {r['E']} | "
                   f"{r['V']} | {r['C']} | {r['raw']} | **{r['total']}** | {r['estado']} |")
    return "\n".join(out)


if __name__ == "__main__":
    rows = load(sys.argv[1])
    sys.stdout.reconfigure(encoding="utf-8")
    print(table(rows))
