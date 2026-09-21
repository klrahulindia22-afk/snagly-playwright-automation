from dataclasses import replace

import pytest

from config.settings import Settings


def test_default_settings_use_safe_local_targets(monkeypatch):
    monkeypatch.delenv("BASE_URL", raising=False)
    monkeypatch.delenv("API_BASE_URL", raising=False)
    settings = Settings.from_environment()
    settings.validate()
    assert settings.environment == "local"


def test_malformed_url_is_rejected():
    settings = replace(Settings.from_environment(), base_url="not-a-url")
    with pytest.raises(ValueError, match="BASE_URL"):
        settings.validate()


def test_production_target_requires_explicit_authorization():
    settings = replace(
        Settings.from_environment(),
        environment="production",
        allow_production_tests=False,
    )
    with pytest.raises(ValueError, match="Production-like target blocked"):
        settings.validate()


def test_missing_role_credentials_fail_clearly(monkeypatch):
    monkeypatch.delenv("TEAM_USER_EMAIL", raising=False)
    monkeypatch.delenv("TEAM_USER_PASSWORD", raising=False)
    with pytest.raises(ValueError, match="Missing team"):
        Settings.from_environment().require_role("team")
