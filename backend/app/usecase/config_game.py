import random
from typing import List, Dict, Callable, Iterable
from app.dto import (
    PlayerDto,
    CreateGameRespDto,
    Investigator,
    ListInvestigatorsDto,
    UpdateCommonRespDto,
    Difficulty,
)
from app.domain import Game, GameError, GameErrorCodes, GameFuncCodes


class AbstractUseCase:
    def __init__(self, repository, evt_emitter=None, settings: Dict = None):
        self.repository = repository
        self.evt_emitter = evt_emitter
        self.settings = settings


class CreateGameUseCase(AbstractUseCase):
    async def execute(
        self, data: List[PlayerDto], presenter: Callable[[Dict, str], CreateGameRespDto]
    ) -> CreateGameRespDto:
        game = Game()
        # Note this game backend interacts only with the Game Lobby
        # Platform in GaaS, the Lobby Platform backend is responsible
        # to send appropriate number of players to this game backend,
        # it does so by referring to the profile provided in game registration
        game.add_players(data)
        self.rand_select_investigator(game)
        await self.repository.save(game)
        if self.evt_emitter:
            await self.evt_emitter.create_game(game)
        return presenter(self.settings, game.id)

    def rand_select_investigator(self, game: Game):
        options = list(Investigator)
        random.shuffle(options)

        def fn1(p):
            c = options.pop(0)
            p.set_investigator(c)
            return game.assign_character(c)

        iterator = map(fn1, game.players)
        return list(iterator)


class GetAvailableInvestigatorsUseCase(AbstractUseCase):
    async def execute(
        self, game_id: str, presenter: Callable[[Iterable], ListInvestigatorsDto]
    ) -> ListInvestigatorsDto:
        game = await self.repository.get_game(game_id)
        unselected = game.filter_unselected_investigators(2) if game else []
        return presenter(unselected)


class SwitchInvestigatorUseCase(AbstractUseCase):
    async def execute(self, game_id: str, player_id: str, new_invstg: Investigator):
        game = await self.repository.get_game(game_id)
        if game is None:
            raise GameError(
                e_code=GameErrorCodes.GAME_NOT_FOUND,
                fn_code=GameFuncCodes.USE_CASE_EXECUTE,
            )
        # NOTE, the character state transition should be done atomically, typically
        # relational / non-relational databases can handle this for app developers due
        # to the ACID properties. However for in-memory data store, app developer
        # should be aware of race condition and data inconsistency issue .

        game.switch_character(player_id, new_invstg)
        await self.repository.save(game)
        if self.evt_emitter:
            await self.evt_emitter.switch_character(game_id, player_id, new_invstg)


class UpdateGameDifficultyUseCase(AbstractUseCase):
    async def execute(self, game_id: str, level: Difficulty) -> UpdateCommonRespDto:
        game = await self.repository.get_game(game_id)
        if game is None:
            raise GameError(
                e_code=GameErrorCodes.GAME_NOT_FOUND,
                fn_code=GameFuncCodes.USE_CASE_EXECUTE,
            )
        game.update_difficulty(level)
        await self.repository.save(game)
        if self.evt_emitter:
            await self.evt_emitter.update_difficulty(game_id, level)
        message = "Update Game {} Difficulty Successfully".format(game.id)
        return UpdateCommonRespDto(message=message)


class GameStartUseCase(AbstractUseCase):
    async def execute(self, game_id: str, player_id: str):
        game = await self.repository.get_game(game_id)
        if game is None:
            raise GameError(
                e_code=GameErrorCodes.GAME_NOT_FOUND,
                fn_code=GameFuncCodes.USE_CASE_EXECUTE,
            )
        game.start(player_id)
        await self.repository.save(game)
        if self.evt_emitter:
            await self.evt_emitter.start_game(game_id, player_id)
