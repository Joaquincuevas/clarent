"""Red team: attack a design document or a PR with a fixed catalog; the engine rejects what it cannot anchor."""
from .cli import main, register  # noqa: F401
from .engine import analyze  # noqa: F401
from .model import RedTeamError, parse  # noqa: F401

__all__ = ["main", "register", "analyze", "parse", "RedTeamError"]
