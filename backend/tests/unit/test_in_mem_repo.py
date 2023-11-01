import asyncio
import pytest
from app.domain import Game
from app.adapter.repository.in_mem import InMemoryRepository


@pytest.fixture
def repo():
    return InMemoryRepository()


@pytest.fixture
def game():
    return Game()


@pytest.mark.asyncio
async def test_save_and_get(repo, game):
    await repo.save(game)
    assert repo.get_game(game.id) == game


def test_get_not_exist_game(repo):
    assert repo.get_game("not-exist") is None


@pytest.mark.asyncio
async def test_duplicate_save(repo, game):
    await repo.save(game)
    await repo.save(game)
    assert len(repo.games) == 1


def test_invalid_game(repo):
    repo.save("invalid")
    assert "invalid" not in repo.games


@pytest.mark.asyncio
async def test_concurrent_access(repo):
    # Start task to call save()
    task = asyncio.create_task(repo.save(Game()))

    # Call get_game() in main thread
    repo.get_game("id")

    await task

    # Assert no exceptions raised
    assert True


@pytest.mark.parametrize("game_id", ["game-1", "game-2"])
def test_get_game(repo, game_id):
    repo.games[game_id] = Game()
    assert repo.get_game(game_id) is not None
