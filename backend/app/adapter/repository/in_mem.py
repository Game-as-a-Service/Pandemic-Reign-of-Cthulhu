import asyncio
from typing import Optional

from app.domain import Game
from app.adapter.repository import AbstractGameRepository, AbstractRtcRoomRepository
from app.dto import RtcRoomMsgData


class InMemoryGameRepository(AbstractGameRepository):
    def __init__(self):
        self._lock = asyncio.Lock()
        self._games = {}

    async def save(self, game: Game):
        if not isinstance(game, Game):
            raise ValueError("game-must-be-a-Game-object")
        async with self._lock:
            self._games[game.id] = game

    async def get_game(self, game_id: str) -> Optional[Game]:
        async with self._lock:
            return self._games.get(game_id)


class InMemoryRtcRoomRepository(AbstractRtcRoomRepository):
    def __init__(self):
        self._lock = asyncio.Lock()
        self._rooms = {}

    async def save(self, data: RtcRoomMsgData):
        async with self._lock:
            self._rooms[data.gameID] = data

    async def get(self, game_id: str) -> Optional[RtcRoomMsgData]:
        async with self._lock:
            return self._rooms.get(game_id)
