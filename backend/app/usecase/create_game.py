import random
from typing import List, Dict
from app.dto import PlayerDto, CreateGameRespDto
from app.domain import Game, GameError, Investigator


class AbstractUseCase:
    def __init__(self, repository, settings: Dict):
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
