"""TRIZ contradiction matrix: parameter pair -> inventive principles, with software examples."""
from .cli import main, register  # noqa: F401
from .engine import lookup, rank  # noqa: F401
from .model import TrizError, load, resolve  # noqa: F401

__all__ = ["main", "register", "lookup", "rank", "load", "resolve", "TrizError"]
