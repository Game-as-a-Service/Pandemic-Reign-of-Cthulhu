from app.domain import Game
from app.adapter.repository import AbstractRepository


class InMemoryRepository(AbstractRepository):
    # TODO, use one-dimensional array to keep the game model instances
    async def save(self, game: Game):
        pass
