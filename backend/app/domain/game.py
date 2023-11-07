from enum import Enum, auto
from typing import List, Optional
from uuid import uuid4

from app.dto import PlayerDto, Investigator
from .player import Player


class Difficulty(Enum):
    # 教學難度
    INTRODUCTORY = auto()
    # 標準難度
    STANDARD = auto()
    # 專家難度
    EXPERT = auto()


class GameError(Exception):
    pass


class Game:
    MIN_NUM_PLAYERS = 2
    MAX_NUM_PLAYERS = 4

    def __init__(self, difficult_level: Difficulty = Difficulty.INTRODUCTORY):
        self._id = None
        # TODO, declare setter for difficulty level
        self._difficulty: Difficulty = difficult_level
        self._players: List[Player] = []
        # 紀錄每個調查員是否已經被選擇
        self._investigators = {}
        for i in Investigator:
            self._investigators[i] = False

    def add_players(self, player_dtos: List[PlayerDto]) -> Optional[GameError]:
        players = []

        for dto in player_dtos:
            player = Player(dto.id, dto.nickname)
            players.append(player)

        if len(players) < self.MIN_NUM_PLAYERS or len(players) > self.MAX_NUM_PLAYERS:
            raise GameError("incorrect-number-of-players")

        self._players = players

    @property
    def id(self) -> str:
        if self._id is None:
            self._id = str(uuid4())
        return self._id

    @property
    def players(self) -> List[Player]:
        return self._players

    def get_player(self, pid: str) -> Optional[Player]:
        def match_chk(p):
            return p.id == pid

        iterator = filter(match_chk, self._players)
        try:
            return next(iterator)
        except StopIteration:
            return None

    def assign_character(self, investigator: Investigator) -> Optional[GameError]:
        if investigator not in self._investigators:
            return GameError("invalid-investigator")

        if self._investigators[investigator]:
            return GameError("investigator-already-chosen")

        self._investigators[investigator] = True
        return None

    def _clear_character_selection(
        self, investigator: Investigator
    ) -> Optional[GameError]:
        # TODO, figure out better design options
        if investigator in self._investigators:
            self._investigators[investigator] = False
        else:
            return GameError("invalid-investigator")

    def switch_character(
        self, player_id: str, new_invstg: Investigator
    ) -> Optional[GameError]:
        player = self.get_player(player_id)
        if player is None:
            return GameError("invalid-player")
        old_invstg = player.get_investigator()
        error = self._clear_character_selection(old_invstg) if old_invstg else None
        if error is None:
            error = self.assign_character(new_invstg)
            if error is None:
                player.set_investigator(new_invstg)
            else:  # error happened, roll back to previous state
                if old_invstg:
                    assert self.assign_character(old_invstg) is None
        return error

    def filter_unselected_investigators(self, num: int) -> List[Investigator]:
        invstgs = self._investigators
        unselected = [i_name for i_name, selected in invstgs.items() if not selected]
        return unselected[:num]
