from typing import List

import pytest
import socketio

SERVER_URL = "http://localhost:8082"

toplvl_namespace = "/game"


class TestRealTimeComm:
    @pytest.mark.asyncio
    async def test_event_subscription(self):
        players = [socketio.AsyncSimpleClient(logger=False) for _ in range(0, 5)]
        game_rooms = {"a001": players[:2], "b073": players[2:]}

        for clients in game_rooms.values():
            for client in clients:
                await client.connect(SERVER_URL, namespace=toplvl_namespace)

        for g_id, clients in game_rooms.items():
            for c in clients:
                await c.emit("/init", data={"client": c.sid, "room": g_id})
        # receive the result right after emitting `init` event
        # Note `socket.io` does not gurantee the order of completion
        clients = game_rooms["a001"]
        await self.verify_init_response(
            receiver=clients[0], expect_client_sid=[clients[1].sid, clients[0].sid]
        )
        await self.verify_init_response(
            receiver=clients[1], expect_client_sid=[clients[1].sid]
        )
        clients = game_rooms["b073"]
        await self.verify_init_response(
            receiver=clients[0],
            expect_client_sid=[clients[2].sid, clients[1].sid, clients[0].sid],
        )
        await self.verify_init_response(
            receiver=clients[1], expect_client_sid=[clients[1].sid, clients[2].sid]
        )
        await self.verify_init_response(
            receiver=clients[2], expect_client_sid=[clients[2].sid]
        )

        # one client sends chat event to others in the same room
        for g_id, clients in game_rooms.items():
            await clients[0].emit(
                "/chat", data={"client": clients[0].sid, "gameID": g_id, "msg": "Hello"}
            )
            with pytest.raises(socketio.exceptions.TimeoutError):
                await clients[0].receive(timeout=1)

        clients = game_rooms["a001"]
        await self.verify_received_chat(receiver=clients[1], expect_sender=clients[0])
        await clients[1].emit(
            "/chat", data={"client": clients[1].sid, "gameID": "a001", "msg": "Halo"}
        )

        clients = game_rooms["b073"]
        await self.verify_received_chat(receiver=clients[2], expect_sender=clients[0])
        await self.verify_received_chat(receiver=clients[1], expect_sender=clients[0])
        await clients[2].emit(
            "/chat", data={"client": clients[2].sid, "gameID": "b073", "msg": "Hey"}
        )
        await self.verify_received_chat(receiver=clients[1], expect_sender=clients[2])
        await self.verify_received_chat(receiver=clients[0], expect_sender=clients[2])

        clients = game_rooms["a001"]
        await self.verify_received_chat(receiver=clients[0], expect_sender=clients[1])

        for g_id, clients in game_rooms.items():
            for c in clients:
                await c.emit("/deinit", data={"client": c.sid, "room": g_id})
                await c.disconnect()
        # end of test_event_subscription

    async def verify_init_response(
        self, receiver: socketio.AsyncSimpleClient, expect_client_sid: List[str]
    ):
        actual_client_sid = []
        for expect_sid in expect_client_sid:
            evts = await receiver.receive(timeout=1)
            assert len(evts) == 2
            assert evts[0] == "/init"
            assert evts[1]["succeed"]
            actual_client_sid.append(evts[1]["client"])
        assert set(actual_client_sid) == set(expect_client_sid)

    async def verify_received_chat(
        self,
        receiver: socketio.AsyncSimpleClient,
        expect_sender: socketio.AsyncSimpleClient,
    ):
        evts = await receiver.receive(timeout=3)
        assert len(evts) == 2
        assert evts[0] == "/chat"
        assert evts[1]["client"] == expect_sender.sid
