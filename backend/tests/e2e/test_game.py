from fastapi.testclient import TestClient
import pytest

from app.config import REST_HOST, REST_PORT
from app.adapter.api import init_app_server
from app.domain import GameErrorCodes


@pytest.fixture(scope="session")
def test_client():
    with TestClient(
        app=init_app_server(),
        base_url="http://%s:%s" % (REST_HOST, REST_PORT),
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

    def test_update_investigator_nonexist_game(self, test_client):
        url = "/games/{}/investigator"
        reqbody = {
            "investigator": "doctor",
            "player_id": "104",
        }
        response = test_client.patch(url.format("xxxxx"), headers={}, json=reqbody)
        assert response.status_code == 404
        error_detail = response.json()
        assert error_detail["reason"] == GameErrorCodes.GAME_NOT_FOUND.value[0]

    def test_update_investigator_ok(self, test_client):
        game_id = self.create_game_common(test_client)
        url = "/games/{}/investigator"
        response = test_client.get(url.format(game_id), headers={})
        assert response.status_code == 200
        unselected_roles = response.json()
        assert len(unselected_roles) == 2
        reqbody = {
            "investigator": unselected_roles[0]["investigator"],
            "player_id": "9527",
        }
        response = test_client.patch(url.format(game_id), headers={}, json=reqbody)
        assert response.status_code == 200
        reqbody = {
            "investigator": unselected_roles[1]["investigator"],
            "player_id": "9487",
        }
        response = test_client.patch(url.format(game_id), headers={}, json=reqbody)
        assert response.status_code == 200
        reqbody = {
            "investigator": unselected_roles[1]["investigator"],
            "player_id": "9527",
        }
        response = test_client.patch(url.format(game_id), headers={}, json=reqbody)
        assert response.status_code == 409
        error_detail = response.json()
        assert error_detail["reason"] == GameErrorCodes.INVESTIGATOR_CHOSEN.value[0]

    def test_update_game_difficulty_ok(self, test_client):
        game_id = self.create_game_common(test_client)
        url = "/games/{}/difficulty"
        reqbody = {"level": "standard"}
        response = test_client.patch(url.format(game_id), headers={}, json=reqbody)
        assert response.status_code == 200
        respbody = response.json()
        message = respbody.get("message")
        assert message == "Update Game {} Difficulty Successfully".format(game_id)

    def test_update_game_difficulty_nonexist_game(self, test_client):
        url = "/games/{}/difficulty"
        reqbody = {"level": "standard"}
        response = test_client.patch(url.format("xxxxx"), headers={}, json=reqbody)
        assert response.status_code == 404
        error_detail = response.json()
        assert error_detail["reason"] == GameErrorCodes.GAME_NOT_FOUND.value[0]
