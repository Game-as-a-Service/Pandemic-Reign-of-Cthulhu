import threading
from contextlib import contextmanager
from typing import Dict
from app.domain import Game
from app.adapter.repository import AbstractRepository


class InMemoryRepository(AbstractRepository):
    def __init__(self):
        self.games = {}

    @contextmanager
    def games_dict(self) -> Dict[str, Game]:
        """Provide thread-safe access to the in-memory games dictionary.

        This context manager acquires a lock before yielding the games dict
        and releases it after, ensuring thread-safe access.

        Yields:
            Dict[str, Game]: The in-memory games dictionary.
        """
        lock = threading.Lock()
        lock.acquire()
        try:
            yield self.games
        finally:
            lock.release()

    async def save(self, game: Game):
        if not isinstance(game, Game):
            raise ValueError("game-must-be-a-Game-object")
        with self.games_dict() as games:
            games[game.id] = game

    def get_game(self, game_id):
        with self.games_dict() as games:
            return games.get(game_id)
