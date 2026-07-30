"""Application entry point.

Run with ``python -m senscritique_cli`` or the installed ``senscritique_cli`` script.
"""

from __future__ import annotations

from .logger import build_logger


def main() -> int:
    logger = build_logger(__package__ or "senscritique_cli")
    logger.info("senscritique_cli started")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
