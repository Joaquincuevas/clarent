"""Entry point called by the skill. Stdlib only; no installation required."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from clarent_redteam import main  # noqa: E402

sys.exit(main())
