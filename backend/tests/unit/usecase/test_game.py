import pytest
from app.dto import PlayerDto, SingleInvestigatorDto, ListInvestigatorsDto, UpdateDifficultyDto
from app.domain import Game, GameError, GameErrorCodes, GameFuncCodes
from app.adapter.repository import AbstractRepository
from app.usecase import CreateGameUseCase, GetAvailableInvestigatorsUseCase, UpdateGameDifficultyUseCase


class MockRepository(AbstractRepository):
    def __init__(self, save_error=None, mock_fetched: Game = None):
        self._save_error = save_error
        self._mock_fetched = mock_fetched

    async def save(self, game: Game):
        if self._save_error:
            raise self._save_error

    async def get_game(self, game_id: str) -> Game:
        if self._mock_fetched:
            return self._mock_fetched
        else:
            raise UnitTestError("MockRepository.get_game")


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

    @pytest.mark.asyncio
    async def test_only_one_player(self):
        repository = MockRepository()
        settings = {"host": "unit.test.app.com"}
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
        ]
        uc = CreateGameUseCase(repository, settings)
        with pytest.raises(GameError) as e:
            resp = await uc.execute(data)  # noqa: F841
            assert e.func_code == GameFuncCodes.ADD_PLAYERS
            assert e.error_code == GameErrorCodes.INCORECT_NUM_PLAYERS

    @pytest.mark.asyncio
    async def test_over_four_player(self):
        repository = MockRepository()
        settings = {"host": "unit.test.app.com"}
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
            PlayerDto(id="8e1u3g", nickname="Lamb"),
            PlayerDto(id="h4oOp0", nickname="Llama"),
            PlayerDto(id="R0fj1B", nickname="Goat"),
            PlayerDto(id="oC9TNH", nickname="Alpaca"),
        ]
        uc = CreateGameUseCase(repository, settings)
        with pytest.raises(GameError) as e:
            resp = await uc.execute(data)  # noqa: F841
            assert e.func_code == GameFuncCodes.ADD_PLAYERS
            assert e.error_code == GameErrorCodes.INCORECT_NUM_PLAYERS


class TestGetAvailInvestigatorFromGame:
    @pytest.mark.asyncio
    async def test_unselected_ok(self):
        mockgame = Game()
        repository = MockRepository(mock_fetched=mockgame)
        uc = GetAvailableInvestigatorsUseCase(repository)

        def mock_presenter(items) -> ListInvestigatorsDto:
            def fn1(v):
                return SingleInvestigatorDto(investigator=v)

            return list(map(fn1, items))

        result = await uc.execute(mockgame.id, mock_presenter)  # noqa: F841
        assert len(result) == 2

class TestUpdateGameDifficulty:
    @pytest.mark.asyncio
    async def test_ok(self):
        mockgame = Game()
        repository = MockRepository(mock_fetched=mockgame)
        settings = {"host": "unit.test.app.com"}
        data = UpdateDifficultyDto(level="standard")
        uc = UpdateGameDifficultyUseCase(repository, settings)
        resp = await uc.execute(mockgame.id, data.level)
        assert resp.message is not None

    