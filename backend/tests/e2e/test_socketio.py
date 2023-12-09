from typing import List, Dict

import pytest
import socketio

SERVER_URL = "http://localhost:8082"


class MockClient:
    def __init__(self, nickname: str, toplvl_namespace="/game"):
        self._sio_client = socketio.AsyncSimpleClient(logger=False)
        self._toplvl_namespace = toplvl_namespace
        self._nickname = nickname
        self._msg_log: List[Dict] = []

    @property
    def sio(self):
        return self._sio_client

    @property
    def nickname(self):
        return self._nickname

    @property
    def messages_log(self):
        return self._msg_log

    async def connect(self, url: str):
        await self._sio_client.connect(url, namespace=self._toplvl_namespace)

    async def disconnect(self):
        await self._sio_client.disconnect()

    async def join(self, room_id: str):
        await self._sio_client.emit(
            "init", data={"client": self._sio_client.sid, "room": room_id}
        )

    async def leave(self, room_id: str):
        await self._sio_client.emit(
            "deinit", data={"client": self._sio_client.sid, "room": room_id}
        )

    async def chat(self, room_id: str, msg: str):
        item = {"nickname": self._nickname, "msg": msg}
        data = {"client": self._sio_client.sid, "gameID": room_id}
        data.update(item)
        await self._sio_client.emit("chat", data=data)
        self._msg_log.append(item)

    async def verify_join(self, expect_clients: List):
        expect_client_sid = [v.sio.sid for v in expect_clients]
        actual_client_sid = []
        for expect_sid in expect_client_sid:
            evts = await self._sio_client.receive(timeout=1)
            assert len(evts) == 2
            assert evts[0] == "init"
            assert evts[1]["succeed"]
            actual_client_sid.append(evts[1]["client"])
        assert set(actual_client_sid) == set(expect_client_sid)

    async def verify_chat(self, expect_sender, expect_error: Dict = None):
        evts: List = await self._sio_client.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == "chat"
        if expect_error:
            assert evts[1] == expect_error
            self.messages_log.pop()
        else:
            assert evts[1]["client"] == expect_sender.sio.sid
            assert evts[1]["nickname"] == expect_sender.nickname
            item = {"nickname": evts[1].pop("nickname"), "msg": evts[1].pop("msg")}
            self._msg_log.append(item)
            assert self.messages_log == expect_sender.messages_log


class TestRealTimeComm:
    @pytest.mark.asyncio
    async def test_chat(self):
        clients = [
            MockClient(nickname="Veronika"),
            MockClient(nickname="Satoshi"),
            MockClient(nickname="Mehlin"),
            MockClient(nickname="Jose"),
            MockClient(nickname="Raj"),
        ]
        game_rooms = {"a001": clients[:2], "b073": clients[2:]}

        for clients in game_rooms.values():
            for client in clients:
                await client.connect(SERVER_URL)

        for g_id, clients in game_rooms.items():
            for c in clients:
                await c.join(room_id=g_id)
        # receive the result right after emitting `init` event
        # Note `socket.io` does not gurantee the order of completion
        clients = game_rooms["b073"]
        await clients[0].verify_join([clients[2], clients[1], clients[0]])
        await clients[1].verify_join(clients[1:])
        await clients[2].verify_join([clients[2]])
        clients = game_rooms["a001"]
        await clients[0].verify_join([clients[1], clients[0]])
        await clients[1].verify_join([clients[1]])

        # one client sends chat event to others in the same room
        clients = game_rooms["a001"]
        await clients[0].chat(room_id="a001", msg="Bonjour")
        with pytest.raises(socketio.exceptions.TimeoutError):
            await clients[0].sio.receive(timeout=1)
        clients = game_rooms["b073"]
        await clients[0].chat(room_id="b073", msg="Merhaba")

        clients = game_rooms["a001"]

        await clients[0].chat(room_id="a001", msg=None)
        await clients[0].verify_chat(
            clients[0], expect_error={"missing_fields": ["msg"]}
        )

        await clients[1].verify_chat(clients[0])
        await clients[1].chat(room_id="a001", msg="Halo")

        clients = game_rooms["b073"]
        await clients[2].verify_chat(clients[0])
        await clients[1].verify_chat(clients[0])
        await clients[2].chat(room_id="b073", msg="Salam")
        await clients[1].verify_chat(clients[2])
        await clients[0].verify_chat(clients[2])

        clients = game_rooms["a001"]
        await clients[0].verify_chat(clients[1])

        for g_id, clients in game_rooms.items():
            for c in clients:
                await c.leave(room_id=g_id)
                await c.disconnect()
        # end of test_event_subscription
