from typing import Optional

from app.domain import Game
from app.dto import RtcRoomMsgData


class AbstractGameRepository:
    async def save(self, game: Game):
        raise NotImplementedError("AbstractGameRepository.save")

    async def get_game(self, game_id: str) -> Game:
        raise NotImplementedError("AbstractGameRepository.get_game")


class AbstractRtcRoomRepository:
    async def save(self, data: RtcRoomMsgData):
        raise NotImplementedError("AbstractRtcRoomRepository.save")

    async def get(self, game_id: str) -> Optional[RtcRoomMsgData]:
        raise NotImplementedError("AbstractRtcRoomRepository.get")


def get_game_repository():
    # TODO
    # - make it configurable at runtime
    # - set max limit of concurrent and ongoing games to save
    from .in_mem import InMemoryGameRepository

    return InMemoryGameRepository()


def get_rtc_room_repository():
    from .in_mem import InMemoryRtcRoomRepository

    return InMemoryRtcRoomRepository()
