from fastapi.testclient import TestClient
import pytest

from app.adapter.api import init_app_server


@pytest.fixture(scope="session")
def test_client():
    with TestClient(
        app=init_app_server(),
        base_url="http://localhost:8081",
        raise_server_exceptions=True,
    ) as _client:
        yield _client


class TestGame:
    def test_create_game_ok(self, test_client):
        url = "/games"
        reqbody = {"players": [{"id": "9487", "nickname": "cowbell"}]}
        response = test_client.post(url, headers={}, json=reqbody)
        assert response.status_code == 200
        respbody = response.json()
        assert respbody.get("url") is not None
