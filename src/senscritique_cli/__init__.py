"""Senscritique Cli package."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("senscritique_cli")
except PackageNotFoundError:  # pragma: no cover - not installed
    __version__ = "0.0.0"

__all__ = ["__version__"]
