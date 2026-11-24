"""Run the core tests and every method's tests, each in its own process. Usage: python tools/test_all.py"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
suites = [ROOT / "tests"] + sorted(p for p in (ROOT / "methods").glob("*/tests") if p.is_dir())
env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONIOENCODING": "utf-8", "CLARENT_LANG": "en"}
failed = []
for s in suites:
    name = s.relative_to(ROOT).as_posix()
    r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", str(s)], cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8")
    last = (r.stderr.strip().splitlines() or ["?"])[-1]
    print(f"{'ok  ' if r.returncode == 0 else 'FAIL'} {name}: {last}")
    if r.returncode:
        failed.append(name)
        print(r.stderr)
sys.exit(1 if failed else 0)
