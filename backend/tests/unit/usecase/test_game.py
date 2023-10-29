import pytest
from app.dto import PlayerDto
from app.domain import Game
from app.adapter.repository import AbstractRepository
from app.usecase import CreateGameUseCase


class MockRepository(AbstractRepository):
    def __init__(self, save_error=None):
        self._save_error = save_error

    async def save(self, game: Game):
        if self._save_error:
            raise self._save_error


class UnitTestError(Exception):
    pass


class TestCreateGame:
    @pytest.mark.asyncio
    async def test_ok(self):
        repository = MockRepository()
        settings = {"host": "unit.test.app.com"}
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
            PlayerDto(id="8e1u3g", nickname="Lamb"),
            PlayerDto(id="h4oOp0", nickname="Llama"),
            PlayerDto(id="R0fj1B", nickname="Goat"),
        ]
        uc = CreateGameUseCase(repository, settings)
        resp = await uc.execute(data)
        assert resp.url is not None

    @pytest.mark.asyncio
    async def test_repo_error(self):
        repository = MockRepository(save_error=UnitTestError("unit-test"))
        settings = {"host": "unit.test.app.com"}
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
            PlayerDto(id="R0fj1B", nickname="Goat"),
        ]
        uc = CreateGameUseCase(repository, settings)
        try:
            resp = await uc.execute(data)  # noqa: F841
            assert 0
        except UnitTestError as e:
            assert e.args[0] == "unit-test"
