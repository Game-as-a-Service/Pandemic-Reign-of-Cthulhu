import pytest
from app.domain import Game, Investigator, GameError


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
