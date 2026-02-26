from src.config.settings import Settings


def _make_settings(**overrides):
    base = {
        "gitlab_token": "test-token",
        "database_url": "sqlite+aiosqlite:///./test.db",
        "api_secret_key": "api-secret",
        "jwt_secret_key": "jwt-secret",
    }
    base.update(overrides)
    return Settings(**base)


def test_secure_defaults_enabled():
    settings = _make_settings()

    assert settings.mcp_auth_enabled is True
    assert settings.azuredevops_ssl_verify is True


def test_default_cors_origins_are_explicit_not_wildcard():
    settings = _make_settings()

    assert "*" not in settings.api_cors_origins
    assert "http://localhost:3000" in settings.api_cors_origins
    assert "http://127.0.0.1:3000" in settings.api_cors_origins
