"""Application configuration sourced from environment variables."""

from __future__ import annotations

import logging
import os

_TRUTHY = {"1", "true", "t", "yes", "y", "on"}

_LOG_LEVELS: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def _as_bool(value: str | None, *, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in _TRUTHY


LOCAL_DEV: bool = _as_bool(os.getenv("LOCAL_DEV"))
GOOGLE_PROJECT_ID: str | None = os.getenv("GOOGLE_PROJECT_ID")
LOG_LEVEL: int = _LOG_LEVELS.get(os.getenv("LOG_LEVEL", "DEBUG").upper(), logging.DEBUG)
