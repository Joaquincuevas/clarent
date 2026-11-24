"""ACH — Analysis of Competing Hypotheses (Heuer) aplicado a debugging."""
from .cli import main, register  # noqa: F401
from .engine import score  # noqa: F401
from .model import ACHError, parse  # noqa: F401

__all__ = ["main", "register", "score", "parse", "ACHError"]
