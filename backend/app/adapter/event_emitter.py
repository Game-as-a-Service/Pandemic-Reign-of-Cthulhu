import logging
import socketio

from app.config import LOG_FILE_PATH, RTC_HOST, RTC_PORT
from app.constant import RealTimeCommConst as RtcConst
from app.domain import Game

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)
_logger.addHandler(logging.FileHandler(LOG_FILE_PATH["REST"], mode="a"))


class AbsEventEmitter:
    async def create_game(self, game: Game):
        raise NotImplementedError("AbsEventEmitter.create_game")


class SocketIoEventEmitter(AbsEventEmitter):
    def __init__(self):
        self._url = "http://%s:%s" % (RTC_HOST, RTC_PORT)
        self._namespace = RtcConst.NAMESPACE
        self._client = socketio.AsyncSimpleClient(logger=True)

    async def create_game(self, game: Game):
        data = {"gameID": game.id, "players": [p.id for p in game.players]}
        try:
            if not self._client.connected:
                await self._client.connect(self._url, namespace=self._namespace)
            await self._client.emit(RtcConst.EVENTS.NEW_ROOM.value, data=data)
        except Exception as e:
            _logger.error("send new-room event: %s", e)
            # TODO, reconnect if connection inactive

    async def deinit(self):
        try:
            await self._client.disconnect()
        except Exception as e:
            _logger.error("error on deinit: %s", e)
