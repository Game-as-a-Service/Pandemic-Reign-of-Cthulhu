from fastapi.testclient import TestClient
from app.adapter.api import init_app_server


class TestGame:
    def test_create_game_ok(self):
        app = init_app_server()
        client = TestClient(
            app=app, base_url="http://localhost:8081", raise_server_exceptions=True
        )
        url = "/games"
        reqbody = {"players": [{"id": "9487", "nickname": "cowbell"}]}
        response = client.post(url, headers={}, json=reqbody)
        assert response.status_code == 200
        respbody = response.json()
        assert respbody.get("url") is not None
