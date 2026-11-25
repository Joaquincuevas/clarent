"""Regenerate docs/demo/ with the real output of the commands shown in the README.

Usage: python tools/gen_demo.py            # rewrite the files
       python tools/gen_demo.py --check    # fail if the files are out of date

The README quotes these outputs verbatim (or as marked excerpts); nothing in them is typed by hand.
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "demo"
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8", "CLARENT_LANG": "en"}

DEMOS = {
    "ach-score.md": ["ach", "score", "methods/ach/examples/flaky-test.json"],
    "ach-next.txt": ["ach", "next", "methods/ach/examples/flaky-test.json"],
    "triz-lookup.md": ["triz-matrix", "lookup", "latency", "Device complexity"],
    "triz-analyze.md": ["triz-matrix", "analyze", "methods/triz-matrix/examples/search-api.json"],
}


def run(args):
    r = subprocess.run([sys.executable, "-m", "clarent", *args], cwd=ROOT, env=ENV, capture_output=True,
                       text=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit(f"clarent {' '.join(args)} exited {r.returncode}:\n{r.stderr}")
    return r.stdout.replace("\r\n", "\n")


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for name, args in DEMOS.items():
        text = run(args)
        path = OUT / name
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(name)
        else:
            OUT.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8", newline="\n")
    if check:
        if stale:
            raise SystemExit("demo outputs out of date: " + ", ".join(stale) + " (run python tools/gen_demo.py)")
        print("demo outputs are up to date")


if __name__ == "__main__":
    main()
