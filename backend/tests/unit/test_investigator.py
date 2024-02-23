import pytest
from app.domain import Game, GameError, GameErrorCodes, GameFuncCodes
from app.dto import PlayerDto, Investigator


@pytest.fixture
def game():
    return Game()


def test_assign_valid(game):
    err = game.assign_character(Investigator.DETECTIVE)
    assert err is None


def test_assign_invalid(game):
    game.assign_character(Investigator.DETECTIVE)
    with pytest.raises(GameError) as e:
        game.assign_character(Investigator.DETECTIVE)
        assert e.func_code == GameFuncCodes.ASSIGN_CHARACTER
        assert e.error_code == GameErrorCodes.INVESTIGATOR_CHOSEN


def test_assign_invalid2(game):
    game.assign_character(Investigator.DETECTIVE)
    game.assign_character(Investigator.HUNTER)
    with pytest.raises(GameError) as e:
        game.assign_character(Investigator.DETECTIVE)
        assert e.error_code == GameErrorCodes.INVESTIGATOR_CHOSEN

    with pytest.raises(GameError) as e:
        game.assign_character(Investigator.HUNTER)
        assert e.error_code == GameErrorCodes.INVESTIGATOR_CHOSEN


def test_assign_not_exist(game):
    with pytest.raises(GameError) as e:
        game.assign_character("unknown")
        assert e.error_code == GameErrorCodes.INVALID_INVESTIGATOR


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


@pytest.mark.parametrize(
    "ut_data",
    [
        (
            [
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.HUNTER,
                    "actual": Investigator.HUNTER,
                    "error": None,
                },
                {
                    "player_id": "8e1u3g",
                    "expect": Investigator.DRIVER,
                    "actual": Investigator.DRIVER,
                    "error": None,
                },
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.DETECTIVE,
                    "actual": Investigator.DETECTIVE,
                    "error": None,
                },
                {
                    "player_id": "8e1u3g",
                    "expect": Investigator.HUNTER,
                    "actual": Investigator.HUNTER,
                    "error": None,
                },
                {
                    "player_id": "e1u30B",
                    "expect": Investigator.REPORTER,
                    "actual": Investigator.REPORTER,
                    "error": None,
                },
                {
                    "player_id": "e1u30B",
                    "expect": Investigator.DRIVER,
                    "actual": Investigator.DRIVER,
                    "error": None,
                },
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.REPORTER,
                    "actual": Investigator.REPORTER,
                    "error": None,
                },
            ]
        ),
        (
            [
                {
                    "player_id": "e1u30B",
                    "expect": Investigator.MAGICIAN,
                    "actual": Investigator.MAGICIAN,
                    "error": None,
                },
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.DRIVER,
                    "actual": Investigator.DRIVER,
                    "error": None,
                },
                {
                    "player_id": "8e1u3g",
                    "expect": Investigator.DRIVER,
                    "actual": None,
                    "error": GameErrorCodes.INVESTIGATOR_CHOSEN,
                },
                {
                    "player_id": "e1u30B",
                    "expect": Investigator.DRIVER,
                    "actual": Investigator.MAGICIAN,
                    "error": GameErrorCodes.INVESTIGATOR_CHOSEN,
                },
                {
                    "player_id": "e1u30B",
                    "expect": Investigator.OCCULTIST,
                    "actual": Investigator.OCCULTIST,
                    "error": None,
                },
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.OCCULTIST,
                    "actual": Investigator.DRIVER,
                    "error": GameErrorCodes.INVESTIGATOR_CHOSEN,
                },
            ]
        ),
        (
            [
                {
                    "player_id": "x8eu3L",
                    "expect": Investigator.DRIVER,
                    "actual": Investigator.DRIVER,
                    "error": None,
                },
                {
                    "player_id": "x8eu3L",
                    "expect": 12345,
                    "actual": Investigator.DRIVER,
                    "error": GameErrorCodes.INVALID_INVESTIGATOR,
                },
                {
                    "player_id": "e1u30B",
                    "expect": 9999,
                    "actual": None,
                    "error": GameErrorCodes.INVALID_INVESTIGATOR,
                },
            ]
        ),
    ],
)  # end of pytest parameter set
def test_switch_to_unselected(game, ut_data):
    setup_data = [
        PlayerDto(id="x8eu3L", nickname="Sheep"),
        PlayerDto(id="8e1u3g", nickname="Lamb"),
        PlayerDto(id="e1u30B", nickname="Llama"),
    ]
    assert game.add_players(player_dtos=setup_data) is None
    for p in game.players:
        assert p.get_investigator() is None

    for d in ut_data:
        if d["error"]:
            with pytest.raises(GameError) as e:
                game.switch_character(d["player_id"], d["expect"])
                assert e.value == d["error"]
        else:
            game.switch_character(d["player_id"], d["expect"])
        player = game.get_player(d["player_id"])
        assert player.get_investigator() == d["actual"]


def test_switch_and_game_start(game):
    setup_data = [
        PlayerDto(id="8e1u3g", nickname="Hawk"),
        PlayerDto(id="e1u30B", nickname="Pelican"),
    ]
    assert game.add_players(player_dtos=setup_data) is None
    for p in game.players:
        assert p.get_investigator() is None

    with pytest.raises(GameError) as e:
        game.start("8e1u3g")
        assert e.value == GameErrorCodes.INVALID_INVESTIGATOR

    game.switch_character("8e1u3g", Investigator.OCCULTIST)
    game.start("8e1u3g")

    with pytest.raises(GameError) as e:
        game.switch_character("8e1u3g", Investigator.DRIVER)
        assert e.value == GameErrorCodes.PLAYER_ALREADY_STARTED
