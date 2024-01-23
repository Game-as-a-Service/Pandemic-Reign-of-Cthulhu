import asyncio
import pytest
from app.domain import Game
from app.adapter.repository.in_mem import InMemoryGameRepository


@pytest.fixture
def repo():
    return InMemoryGameRepository()


@pytest.fixture
def game():
    return Game()


@pytest.mark.asyncio
async def test_save_and_get(repo, game):
    await repo.save(game)
    assert await repo.get_game(game.id) == game


@pytest.mark.asyncio
async def test_get_not_exist_game(repo):
    assert await repo.get_game("not-exist") is None


@pytest.mark.asyncio
async def test_duplicate_save(repo, game):
    await repo.save(game)
    await repo.save(game)
    assert len(repo._games) == 1


@pytest.mark.asyncio
async def test_invalid_game(repo):
    with pytest.raises(ValueError):
        await repo.save("invalid")


@pytest.mark.asyncio
async def test_concurrent_access(repo):
    game = Game()
    game_id = game.id

    # Start task to call save()
    task = asyncio.create_task(repo.save(game))

    # Wait for save() to complete
    await task

    # Call get_game() in main thread
    result = await repo.get_game(game_id)

    # Assert that get_game() returned the game saved by save()
    assert result == game


@pytest.mark.asyncio
@pytest.mark.parametrize("game_id", ["game-1", "game-2"])
async def test_get_game(repo, game_id):
    repo._games[game_id] = Game()
    assert await repo.get_game(game_id) is not None
