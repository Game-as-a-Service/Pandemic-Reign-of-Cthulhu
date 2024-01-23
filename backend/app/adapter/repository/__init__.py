from app.domain import Game


class AbstractGameRepository:
    async def save(self, game: Game):
        raise NotImplementedError("AbstractRepository.save")

    async def get_game(self, game_id: str) -> Game:
        raise NotImplementedError("AbstractRepository.get_game")


def get_game_repository():
    # TODO
    # - make it configurable at runtime
    # - set max limit of concurrent and ongoing games to save
    from .in_mem import InMemoryGameRepository

    return InMemoryGameRepository()
