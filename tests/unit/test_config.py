"""Unit tests for the config helpers."""

import importlib
import logging

import pytest


def test_as_bool_parses_truthy_and_falsy_values() -> None:
    from senscritique_cli import config

    assert config._as_bool("true") is True
    assert config._as_bool("YES") is True
    assert config._as_bool("0") is False
    assert config._as_bool(None) is False
    assert config._as_bool(None, default=True) is True


def test_log_level_defaults_to_debug(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    from senscritique_cli import config

    reloaded = importlib.reload(config)
    assert reloaded.LOG_LEVEL == logging.DEBUG
