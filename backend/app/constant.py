from enum import Enum


class GameRtcEvent(Enum):
    """
    events which synchronize game state in real-time communication
    """

    INIT = "init"
    DEINIT = "deinit"
    CHAT = "chat"
    NEW_ROOM = "new_room"
    CHARACTER = "character"
    DIFFICULTY = "difficulty"
    GAME_START = "game_start"


class RealTimeCommConst:
    EVENTS = GameRtcEvent
    NAMESPACE = "/game"
