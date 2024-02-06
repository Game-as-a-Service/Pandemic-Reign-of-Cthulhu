from typing import Dict, Union
import logging
import socketio

from app.dto import Investigator, Difficulty, RtcCharacterMsgData
from app.config import LOG_FILE_PATH, RTC_HOST, RTC_PORT
from app.constant import RealTimeCommConst as RtcConst, GameRtcEvent
from app.domain import Game

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)
_logger.addHandler(logging.FileHandler(LOG_FILE_PATH["REST"], mode="a"))


class AbsEventEmitter:
    async def create_game(self, game: Game):
        raise NotImplementedError("AbsEventEmitter.create_game")

    async def switch_character(
        self, game_id: str, player_id: str, new_invstg: Investigator
    ):
        raise NotImplementedError("AbsEventEmitter.switch_character")

    async def update_difficulty(self, game_id: str, level: Difficulty):
        raise NotImplementedError("AbsEventEmitter.update_difficulty")


class SocketIoEventEmitter(AbsEventEmitter):
    def __init__(self):
        self._url = "http://%s:%s" % (RTC_HOST, RTC_PORT)
        self._namespace = RtcConst.NAMESPACE
        self._client = socketio.AsyncSimpleClient(logger=True)

    async def create_game(self, game: Game):
        data = {"gameID": game.id, "players": [p.id for p in game.players]}
        await self.do_emit(data, evt=RtcConst.EVENTS.NEW_ROOM)

    async def switch_character(
        self, game_id: str, player_id: str, new_invstg: Investigator
    ):
        data = RtcCharacterMsgData.serialize(game_id, player_id, new_invstg)
        await self.do_emit(data, evt=RtcConst.EVENTS.CHARACTER)

    async def update_difficulty(self, game_id: str, level: Difficulty):
        data = {"gameID": game_id, "level": level.value}
        await self.do_emit(data, evt=RtcConst.EVENTS.DIFFICULTY)

    async def do_emit(self, data: Union[Dict, bytes], evt: GameRtcEvent):
        try:
            if not self._client.connected:
                await self._client.connect(self._url, namespace=self._namespace)
            await self._client.emit(evt.value, data=data)
        except Exception as e:
            _logger.error("emit event: %s", e)
            # TODO, reconnect if connection inactive

    async def deinit(self):
        try:
            await self._client.disconnect()
        except Exception as e:
            _logger.error("error on deinit: %s", e)
