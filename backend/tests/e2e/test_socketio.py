from typing import List, Dict

import pytest
import socketio

from app.config import RTC_HOST, RTC_PORT
from app.constant import RealTimeCommConst as RtcConst
from app.dto import (
    Investigator,
    Difficulty,
    RtcCharacterMsgData,
    RtcDifficultyMsgData,
    RtcGameStartMsgData,
)

SERVER_URL = "http://%s:%s" % (RTC_HOST, RTC_PORT)


class MockiAbstractClient:
    def __init__(self, toplvl_namespace: str):
        self._sio_client = socketio.AsyncSimpleClient(logger=False)
        self._toplvl_namespace = toplvl_namespace

    async def connect(self, url: str):
        await self._sio_client.connect(url, namespace=self._toplvl_namespace)

    async def disconnect(self):
        await self._sio_client.disconnect()


class MockClient(MockiAbstractClient):
    def __init__(self, nickname: str, player_id: str):
        super().__init__(toplvl_namespace=RtcConst.NAMESPACE)
        self._nickname = nickname
        self._player_id = player_id
        self._msg_log: List[Dict] = []

    @property
    def sio(self):
        return self._sio_client

    @property
    def player_id(self):
        return self._player_id

    @property
    def nickname(self):
        return self._nickname

    @property
    def messages_log(self):
        return self._msg_log

    async def join(self, room_id: str):
        await self._sio_client.emit(
            RtcConst.EVENTS.INIT.value,
            data={
                "player": {
                    "id": self._player_id,
                    "nickname": self._nickname,
                },
                "client": self._sio_client.sid,
                "gameID": room_id,
            },
        )

    async def leave(self, room_id: str):
        await self._sio_client.emit(
            RtcConst.EVENTS.DEINIT.value,
            data={
                "player": {
                    "id": self._player_id,
                    "nickname": self._nickname,
                },
                "client": self._sio_client.sid,
                "gameID": room_id,
            },
        )

    async def chat(self, room_id: str, msg: str):
        item = {"nickname": self._nickname, "msg": msg}
        data = {"client": self._sio_client.sid, "gameID": room_id}
        data.update(item)
        await self._sio_client.emit(RtcConst.EVENTS.CHAT.value, data=data)
        self._msg_log.append(item)

    async def verify_join(self, expect_clients: List, expect_join_success: bool):
        expect_client_sid = [v.sio.sid for v in expect_clients]
        actual_client_sid = []
        for expect_sid in expect_client_sid:
            evts = await self._sio_client.receive(timeout=1)
            assert len(evts) == 2
            assert evts[0] == RtcConst.EVENTS.INIT.value
            assert evts[1]["succeed"] == expect_join_success
            if expect_join_success:
                actual_client_sid.append(evts[1]["client"])
        if expect_join_success:
            assert set(actual_client_sid) == set(expect_client_sid)

    async def verify_chat(self, expect_sender, expect_error: Dict = None):
        evts: List = await self._sio_client.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == RtcConst.EVENTS.CHAT.value
        if expect_error:
            assert evts[1] == expect_error
            self.messages_log.pop()
        else:
            assert evts[1]["client"] == expect_sender.sio.sid
            assert evts[1]["nickname"] == expect_sender.nickname
            item = {"nickname": evts[1].pop("nickname"), "msg": evts[1].pop("msg")}
            self._msg_log.append(item)
            assert self.messages_log == expect_sender.messages_log

    async def verify_character_update(self, expect_player, expect_character: str):
        evts: List = await self._sio_client.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == RtcConst.EVENTS.CHARACTER.value
        obj = RtcCharacterMsgData.deserialize(evts[1])
        assert obj.player_id == expect_player.player_id
        assert obj.investigator.value == expect_character

    async def verify_difficulty(self, expect: str):
        evts: List = await self._sio_client.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == RtcConst.EVENTS.DIFFICULTY.value
        obj = RtcDifficultyMsgData.deserialize(evts[1])
        assert obj.level.value == expect

    async def verify_game_start(self, expect_player):
        evts: List = await self._sio_client.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == RtcConst.EVENTS.GAME_START.value
        obj = RtcGameStartMsgData.deserialize(evts[1])
        assert obj.player_id == expect_player.player_id


class MockiHttpServer(MockiAbstractClient):
    async def new_room(self, room_id: str, members: List[str]):
        await self._sio_client.emit(
            RtcConst.EVENTS.NEW_ROOM.value,
            data={
                "players": members,
                "gameID": room_id,
            },
        )

    async def switch_character(
        self, room_id: str, player: str, character: Investigator
    ):
        data = RtcCharacterMsgData.serialize(room_id, player, character)
        await self._sio_client.emit(RtcConst.EVENTS.CHARACTER.value, data=data)

    async def set_difficulty(self, room_id: str, level: Difficulty):
        data = RtcDifficultyMsgData.serialize(room_id, level)
        await self._sio_client.emit(RtcConst.EVENTS.DIFFICULTY.value, data=data)

    async def confirm_start(self, room_id: str, player: str):
        data = RtcGameStartMsgData.serialize(room_id, player)
        await self._sio_client.emit(RtcConst.EVENTS.GAME_START.value, data=data)


class TestRealTimeComm:
    @pytest.mark.asyncio
    async def test_chat_ok(self):
        http_server = MockiHttpServer(RtcConst.NAMESPACE)
        clients = [
            MockClient(nickname="Veronika", player_id="u0011"),
            MockClient(nickname="Satoshi", player_id="u0012"),
            MockClient(nickname="Mehlin", player_id="u0013"),
            MockClient(nickname="Jose", player_id="u0014"),
            MockClient(nickname="Raj", player_id="u0015"),
        ]
        game_rooms = {"a001": clients[:2], "b073": clients[2:]}

        await http_server.connect(SERVER_URL)
        for clients in game_rooms.values():
            for client in clients:
                await client.connect(SERVER_URL)

        for g_id, clients in game_rooms.items():
            await http_server.new_room(g_id, members=[c.player_id for c in clients])
            for c in clients:
                await c.join(room_id=g_id)
        # receive the result right after emitting `init` event
        # Note `socket.io` does not gurantee the order of completion
        clients = game_rooms["b073"]
        await clients[0].verify_join([clients[2], clients[1], clients[0]], True)
        await clients[1].verify_join(clients[1:], True)
        await clients[2].verify_join([clients[2]], True)
        clients = game_rooms["a001"]
        await clients[0].verify_join([clients[1], clients[0]], True)
        await clients[1].verify_join([clients[1]], True)

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
            clients[0],
            expect_error=[
                {
                    "type": "string_type",
                    "loc": ["msg"],
                    "msg": "Input should be a valid string",
                }
            ],
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
        await http_server.disconnect()
        # end of test_event_subscription

    @pytest.mark.asyncio
    async def test_enter_room(self):
        http_server = MockiHttpServer(RtcConst.NAMESPACE)
        client = MockClient(nickname="Asuka", player_id="u0016")
        await http_server.connect(SERVER_URL)
        await client.connect(SERVER_URL)
        await http_server.new_room("de056", members=["another-player"])
        await http_server.new_room("c0034", members=[client.player_id])
        await client.join(room_id="de056")
        await client.verify_join([client], False)
        await client.join(room_id="c0034")
        await client.verify_join([client], True)
        await client.leave(room_id="c0034")
        await client.disconnect()
        await http_server.disconnect()

    @pytest.mark.asyncio
    async def test_forward_game_state_msg(self):
        http_server = MockiHttpServer(RtcConst.NAMESPACE)
        clients = [
            MockClient(nickname="Fabio", player_id="u0017"),
            MockClient(nickname="Von Mc", player_id="u0018"),
        ]
        game_room = "a0020"

        await http_server.connect(SERVER_URL)
        await http_server.new_room(game_room, members=[c.player_id for c in clients])
        for client in clients:
            await client.connect(SERVER_URL)
            await client.join(room_id=game_room)

        await clients[0].verify_join(clients[:], True)
        await clients[1].verify_join(clients[1:], True)

        await http_server.switch_character(
            game_room, clients[1].player_id, character=Investigator.MAGICIAN
        )
        await clients[0].verify_character_update(clients[1], "magician")
        await clients[1].verify_character_update(clients[1], "magician")
        await http_server.switch_character(
            game_room, clients[0].player_id, character=Investigator.DRIVER
        )
        await clients[0].verify_character_update(clients[0], "driver")
        await clients[1].verify_character_update(clients[0], "driver")

        await http_server.set_difficulty(game_room, level=Difficulty.EXPERT)
        await clients[0].verify_difficulty("expert")
        await clients[1].verify_difficulty("expert")
        await http_server.set_difficulty(game_room, level=Difficulty.STANDARD)
        await clients[0].verify_difficulty("standard")
        await clients[1].verify_difficulty("standard")

        await http_server.confirm_start(game_room, clients[1].player_id)
        await clients[0].verify_game_start(clients[1])
        await clients[1].verify_game_start(clients[1])
        await http_server.confirm_start(game_room, clients[0].player_id)
        await clients[0].verify_game_start(clients[0])
        await clients[1].verify_game_start(clients[0])

        for client in clients:
            await client.leave(room_id=game_room)
            await client.disconnect()
        await http_server.disconnect()
