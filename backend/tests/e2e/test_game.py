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


def extract_game_id(url: str):
    return url.split("/")[-1]


class TestGame:
    def create_game_common(self, test_client):
        url = "/games"
        reqbody = {
            "players": [
                {"id": "9487", "nickname": "Sheep"},
                {"id": "9527", "nickname": "Goat"},
            ]
        }
        response = test_client.post(url, headers={}, json=reqbody)
        assert response.status_code == 200
        respbody = response.json()
        url = respbody.get("url")
        assert url is not None
        return extract_game_id(url)

    def test_create_game_ok(self, test_client):
        self.create_game_common(test_client)

    def test_update_investigator_ok(self, test_client):
        game_id = self.create_game_common(test_client)
        url = "/games/{}/investigator"
        response = test_client.get(url.format(game_id), headers={})
        assert response.status_code == 200
        unselected_roles = response.json()
        assert len(unselected_roles) == 2
