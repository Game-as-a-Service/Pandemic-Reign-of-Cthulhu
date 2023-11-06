import pytest
from app.domain import Game, GameError
from app.dto import PlayerDto, Investigator


@pytest.fixture
def game():
    return Game()


def test_assign_valid(game):
    err = game.assign_character(Investigator.DETECTIVE)
    assert err is None


def test_assign_invalid(game):
    game.assign_character(Investigator.DETECTIVE)
    err = game.assign_character(Investigator.DETECTIVE)
    assert isinstance(err, GameError)
    assert err.args[0] == "investigator-already-chosen"


def test_assign_invalid2(game):
    game.assign_character(Investigator.DETECTIVE)
    game.assign_character(Investigator.HUNTER)
    err = game.assign_character(Investigator.DETECTIVE)
    assert isinstance(err, GameError)
    assert err.args[0] == "investigator-already-chosen"

    err = game.assign_character(Investigator.HUNTER)
    assert isinstance(err, GameError)
    assert err.args[0] == "investigator-already-chosen"


def test_assign_not_exist(game):
    err = game.assign_character("unknown")
    assert isinstance(err, GameError)
    assert err.args[0] == "invalid-investigator"


def test_filter_unselected_all(game):
    data = [
        PlayerDto(id="x8eu3L", nickname="Sheep"),
        PlayerDto(id="8e1u3g", nickname="Lamb"),
    ]
    assert game.add_players(player_dtos=data) is None
    # --- sub case 1, the first player selected
    player = game.get_player("x8eu3L")
    assert player is not None
    expect_chosen_role = Investigator.DOCTOR
    assert game.assign_character(expect_chosen_role) is None
    player.set_investigator(expect_chosen_role)
    result = game.filter_unselected_investigators(6)
    assert len(result) == 6
    assert expect_chosen_role not in result
    # --- sub case 2, the 2nd player selected
    player = game.get_player("8e1u3g")
    assert player is not None
    expect_chosen_role = Investigator.DETECTIVE
    assert game.assign_character(expect_chosen_role) is None
    player.set_investigator(expect_chosen_role)
    result = game.filter_unselected_investigators(99)
    assert len(result) == 5
    assert Investigator.DOCTOR not in result
    assert Investigator.DETECTIVE not in result


def test_filter_unselected_limit(game):
    data = [
        PlayerDto(id="x8eu3L", nickname="Sheep"),
        PlayerDto(id="8e1u3g", nickname="Lamb"),
    ]
    assert game.add_players(player_dtos=data) is None
    result = game.filter_unselected_investigators(2)
    assert len(result) == 2
    result = game.filter_unselected_investigators(3)
    assert len(result) == 3
