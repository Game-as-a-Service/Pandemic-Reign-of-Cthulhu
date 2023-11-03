import pytest
from app.dto import PlayerDto, Investigator
from app.domain import Game, GameError
from app.adapter.repository import AbstractRepository
from app.usecase import CreateGameUseCase, ReadInvestigatorUseCase


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
        try:
            resp = await uc.execute(data)  # noqa: F841
            assert 0
        except GameError as e:
            assert e.args[0] == "incorrect-number-of-players"

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
        try:
            resp = await uc.execute(data)  # noqa: F841
            assert 0
        except GameError as e:
            assert e.args[0] == "incorrect-number-of-players"


class TestReadInvestigatorFromGame:
    @pytest.mark.asyncio
    async def test_selected_ok(self):
        mockgame = Game()
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
            PlayerDto(id="8e1u3g", nickname="Lamb"),
        ]
        assert mockgame.add_players(player_dtos=data) is None
        repository = MockRepository(mock_fetched=mockgame)
        uc = ReadInvestigatorUseCase(repository)

        # --- sub case 1, the first player selected
        player = mockgame.get_player("x8eu3L")
        assert player is not None
        expect_chosen_role = Investigator.DOCTOR
        assert mockgame.assign_character(expect_chosen_role) is None
        player.set_investigator(expect_chosen_role)
        result = await uc.execute(mockgame.id, 99)  # noqa: F841
        assert len(result) == 6
        assert expect_chosen_role not in result

        # --- sub case 2, the 2nd player selected
        player = mockgame.get_player("8e1u3g")
        assert player is not None
        expect_chosen_role = Investigator.DETECTIVE
        assert mockgame.assign_character(expect_chosen_role) is None
        player.set_investigator(expect_chosen_role)
        result = await uc.execute(mockgame.id, 99)  # noqa: F841
        assert len(result) == 5
        assert Investigator.DOCTOR not in result
        assert Investigator.DETECTIVE not in result

    @pytest.mark.asyncio
    async def test_limit_return_sequence(self):
        mockgame = Game()
        data = [
            PlayerDto(id="x8eu3L", nickname="Sheep"),
            PlayerDto(id="8e1u3g", nickname="Lamb"),
        ]
        assert mockgame.add_players(player_dtos=data) is None
        repository = MockRepository(mock_fetched=mockgame)
        uc = ReadInvestigatorUseCase(repository)
        result = await uc.execute(mockgame.id, 2)  # noqa: F841
        assert len(result) == 2
        result = await uc.execute(mockgame.id, 3)  # noqa: F841
        assert len(result) == 3
