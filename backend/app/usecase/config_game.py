import random
from typing import List, Dict, Optional, Callable, Iterable
from app.dto import PlayerDto, CreateGameRespDto, Investigator, ListInvestigatorsDto
from app.domain import Game, GameError


class AbstractUseCase:
    def __init__(self, repository, settings: Dict = None):
        self.repository = repository
        self.settings = settings


class CreateGameUseCase(AbstractUseCase):
    async def execute(self, data: List[PlayerDto]) -> CreateGameRespDto:
        game = Game()
        # Note this game backend interacts only with the Game Lobby
        # Platform in GaaS, the Lobby Platform backend is responsible
        # to send appropriate number of players to this game backend,
        # it does so by referring to the profile provided in game registration
        game.add_players(data)
        errors = self.rand_select_investigator(game)
        assert len(errors) == 0
        await self.repository.save(game)
        url = "https://{}/games/{}".format(self.settings["host"], game.id)
        return CreateGameRespDto(url=url)

    def rand_select_investigator(self, game: Game) -> List[GameError]:
        options = list(Investigator)
        random.shuffle(options)

        def fn1(p):
            c = options.pop(0)
            p.set_investigator(c)
            return game.assign_character(c)

        def fn2(err):
            return err is not None

        iterator = filter(fn2, map(fn1, game.players))
        return list(iterator)


class GetAvailableInvestigatorsUseCase(AbstractUseCase):
    async def execute(
        self, game_id: str, presenter: Callable[[Iterable], ListInvestigatorsDto]
    ) -> ListInvestigatorsDto:
        game = await self.repository.get_game(game_id)
        unselected = game.filter_unselected_investigators(2) if game else []
        return presenter(unselected)


class SwitchInvestigatorUseCase(AbstractUseCase):
    async def execute(
        self, game_id: str, player_id: str, new_invstg: Investigator
    ) -> Optional[GameError]:
        game = await self.repository.get_game(game_id)
        if game is None:
            return GameError("invalid-game")
        # NOTE, the character state transition should be done atomically, typically
        # relational / non-relational databases can handle this for app developers due
        # to the ACID properties. However for in-memory data store, app developer
        # should be aware of race condition and data inconsistency issue .

        result = game.switch_character(player_id, new_invstg)
        await self.repository.save(game)
        return result
