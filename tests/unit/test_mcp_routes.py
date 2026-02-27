from dataclasses import dataclass

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.auth import get_current_user, get_current_user_mcp
from src.api.dependencies import get_db_session
from src.api.routes.mcp_http import router as mcp_http_router
from src.api.routes.mcp_test import router as mcp_test_router


@dataclass
class _Content:
    type: str
    text: str


def _build_app(*routers):
    app = FastAPI()
    for router, prefix in routers:
        app.include_router(router, prefix=prefix)
    app.dependency_overrides[get_current_user_mcp] = lambda: {"user_id": "test"}
    app.dependency_overrides[get_current_user] = lambda: {"user_id": "test"}

    async def _fake_db_session():
        class _DummySession:
            pass

        yield _DummySession()

    app.dependency_overrides[get_db_session] = _fake_db_session
    return app


def test_mcp_http_initialize_returns_capabilities():
    app = _build_app((mcp_http_router, "/api/v1"))
    client = TestClient(app)

    response = client.post(
        "/api/v1/mcp",
        json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["result"]["serverInfo"]["name"] == "axon-mcp-server"
    assert payload["result"]["protocolVersion"] == "2025-06-18"


def test_mcp_http_invalid_json_returns_parse_error():
    app = _build_app((mcp_http_router, "/api/v1"))
    client = TestClient(app)

    response = client.post(
        "/api/v1/mcp",
        data="{not-json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"]["code"] == -32700


def test_mcp_test_search_code_endpoint(monkeypatch):
    app = _build_app((mcp_test_router, "/api/v1"))
    client = TestClient(app)

    async def _fake_search_code(**kwargs):
        assert kwargs["query"] == "billing"
        return [_Content(type="text", text="ok")]

    import src.mcp_server.tools.search as search_tools

    monkeypatch.setattr(search_tools, "search_code", _fake_search_code)

    response = client.post(
        "/api/v1/mcp/tools/search_code",
        json={"query": "billing", "limit": 5},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["isError"] is False
    assert payload["content"][0]["text"] == "ok"
