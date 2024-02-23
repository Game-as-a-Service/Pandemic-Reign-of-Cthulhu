from enum import Enum
from typing import List, Optional
from uuid import uuid4

from app.dto import PlayerDto, Investigator, Difficulty
from .player import Player


class GameErrorCodes(Enum):
    """
    Elements for each tuple
     - application-level error code
     - HTTP response status code
    """

    INCORECT_NUM_PLAYERS = (1001, 400)
    INVALID_INVESTIGATOR = (1002, 400)
    INVESTIGATOR_CHOSEN = (1003, 409)
    INVALID_PLAYER = (1004, 422)
    GAME_NOT_FOUND = (1005, 404)
    PLAYER_ALREADY_STARTED = (1006, 400)


class GameFuncCodes(Enum):
    ADD_PLAYERS = 1001
    ASSIGN_CHARACTER = 1002
    SWITCH_CHARACTER = 1003
    CLEAR_CHARACTER_SELECTION = 1004
    UPDATE_DIFFICULTY = 1005
    START_GAME = 1006
    ## TODO, rename the following members
    USE_CASE_EXECUTE = 1099
    RTC_ENDPOINT = 1098  ## for real-time communication like socket.io server endpoint


class GameError(Exception):
    def __init__(
        self, e_code: GameErrorCodes, fn_code: GameFuncCodes, msg: Optional[str] = None
    ):
        self.error_code: GameErrorCodes = e_code
        self.func_code: GameFuncCodes = fn_code
        self.message = msg


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

    def add_players(self, player_dtos: List[PlayerDto]):
        players = []

        for dto in player_dtos:
            player = Player(dto.id, dto.nickname)
            players.append(player)

        if len(players) < self.MIN_NUM_PLAYERS or len(players) > self.MAX_NUM_PLAYERS:
            raise GameError(
                e_code=GameErrorCodes.INCORECT_NUM_PLAYERS,
                fn_code=GameFuncCodes.ADD_PLAYERS,
            )

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

    def assign_character(self, investigator: Investigator):
        if investigator not in self._investigators:
            raise GameError(
                e_code=GameErrorCodes.INVALID_INVESTIGATOR,
                fn_code=GameFuncCodes.ASSIGN_CHARACTER,
            )

        if self._investigators[investigator]:
            raise GameError(
                e_code=GameErrorCodes.INVESTIGATOR_CHOSEN,
                fn_code=GameFuncCodes.ASSIGN_CHARACTER,
            )

        self._investigators[investigator] = True

    def _clear_character_selection(self, investigator: Investigator):
        # TODO, figure out better design options
        if investigator not in self._investigators:
            raise GameError(
                e_code=GameErrorCodes.INVALID_INVESTIGATOR,
                fn_code=GameFuncCodes.CLEAR_CHARACTER_SELECTION,
            )

        self._investigators[investigator] = False

    def switch_character(self, player_id: str, new_invstg: Investigator):
        player = self.get_player(player_id)
        if player is None:
            raise GameError(
                e_code=GameErrorCodes.INVALID_PLAYER,
                fn_code=GameFuncCodes.SWITCH_CHARACTER,
            )
        if player.started:
            raise GameError(
                e_code=GameErrorCodes.PLAYER_ALREADY_STARTED,
                fn_code=GameFuncCodes.SWITCH_CHARACTER,
            )
        old_invstg = player.get_investigator()
        try:
            if old_invstg:
                self._clear_character_selection(old_invstg)
            self.assign_character(new_invstg)
            player.set_investigator(new_invstg)
        except GameError as e:
            if old_invstg and e.func_code == GameFuncCodes.ASSIGN_CHARACTER:
                # roll back to previous state
                self.assign_character(old_invstg)
            raise

    def filter_unselected_investigators(self, num: int) -> List[Investigator]:
        invstgs = self._investigators
        unselected = [i_name for i_name, selected in invstgs.items() if not selected]
        return unselected[:num]

    def update_difficulty(self, difficulty: Difficulty):
        self._difficulty = difficulty

    def start(self, player_id: str):
        player = self.get_player(player_id)
        if player is None:
            raise GameError(
                e_code=GameErrorCodes.INVALID_PLAYER,
                fn_code=GameFuncCodes.START_GAME,
            )
        if player.get_investigator() is None:
            raise GameError(
                e_code=GameErrorCodes.INVALID_INVESTIGATOR,
                fn_code=GameFuncCodes.START_GAME,
            )
        player.start()
        all_started = all([p.started for p in self.players])
        if all_started:
            pass
        # TODO
        # - initialize all types of cards, card deck, map (number of cultists in each
        #   location), player status e.g. sanity points
