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


# 用parametrize來設置不同的測試案例和期望結果
@pytest.mark.parametrize(
    "assignments, limit, expected_lengths, expected_not_in_results",
    [
        # 測試案例1: 當所有調查員都未選擇時
        ([], 6, [6], []),
        # 測試案例2: 當第一個玩家選擇了一個調查員時
        ([("x8eu3L", Investigator.DOCTOR)], 6, [6], [Investigator.DOCTOR]),
        # 測試案例3: 當兩個玩家都選擇了不同的調查員時
        (
            [("x8eu3L", Investigator.DOCTOR), ("8e1u3g", Investigator.DETECTIVE)],
            99,
            [5],
            [Investigator.DOCTOR, Investigator.DETECTIVE],
        ),
        # 測試案例4: 限制數量的案例
        ([], 2, [2], []),
        ([], 3, [3], []),
    ],
)
def test_filter_unselected(
    game, assignments, limit, expected_lengths, expected_not_in_results
):
    # 設置玩家
    data = [
        PlayerDto(id="x8eu3L", nickname="Sheep"),
        PlayerDto(id="8e1u3g", nickname="Lamb"),
    ]
    assert game.add_players(player_dtos=data) is None

    # 分配調查員給指定的玩家
    for player_id, role in assignments:
        player = game.get_player(player_id)
        assert player is not None
        assert game.assign_character(role) is None
        player.set_investigator(role)

    # 測試不同的限制條件
    for expected_length in expected_lengths:
        result = game.filter_unselected_investigators(limit)
        assert len(result) == expected_length
        for role in expected_not_in_results:
            assert role not in result
