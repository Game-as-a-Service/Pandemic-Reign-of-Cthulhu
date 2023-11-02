import pytest
from app.domain import Player, Investigator


@pytest.fixture
def player():
    return Player("guQlii", "Player A")


def test_set_investigator(player):
    player.set_investigator(Investigator.DETECTIVE)
    assert player._investigator == Investigator.DETECTIVE


def test_get_investigator(player):
    player.set_investigator(Investigator.DOCTOR)
    assert player.get_investigator() == Investigator.DOCTOR


def test_not_set(player):
    assert player.get_investigator() is None
