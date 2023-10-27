from enum import Enum, auto
from typing import List, Optional

from app.dto import PlayerDto
from .player import Player


class Difficulty(Enum):
    INTRODUCTORY = auto()


class Investigator(Enum):
    HUNTER = auto()
    DRIVER = auto()


class GameError(Exception):
    pass


class Game:
    MAX_NUM_PLAYERS = 4

    def __init__(self, difficult_level: Difficulty = Difficulty.INTRODUCTORY):
        # TODO, declare setter for difficulty level
        self._difficulty: Difficulty = difficult_level
        self._players: List[Player] = []

    def add_players(self, players: List[PlayerDto]):
        # TODO,
        # - convert to player domain models
        # - return error if necessary
        pass

    @property
    def id(self):
        # TODO, generate game ID
        return "x1234"

    @property
    def players(self) -> List[Player]:
        return self._players

    def assign_character(
        self, player: Player, investigator: Investigator
    ) -> Optional[GameError]:
        # TODO, possible errors are :
        # no-such-player, investigator-already-chosen, game-already-started
        pass
