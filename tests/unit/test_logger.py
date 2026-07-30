"""Unit tests for logger construction."""

import logging

from senscritique_cli.logger import build_logger


def test_build_logger_returns_configured_logger() -> None:
    logger = build_logger("test-logger")

    assert isinstance(logger, logging.Logger)
    assert logger.name == "test-logger"
    assert logger.handlers, "expected at least one handler to be attached"
