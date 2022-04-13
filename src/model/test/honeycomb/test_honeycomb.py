import pytest
from src.model.src.honeycomb.honeycomb import Bee, HoneyComb


def test_honeycomb_creation():
    with pytest.raises(Exception) as excepinfo:
        HoneyComb([], -1)
    assert 'The attributes of the Honeycomb are not correct' == str(excepinfo.value)
    with pytest.raises(Exception) as excepinfo:
        HoneyComb([2], 0)


@pytest.fixture
def default_honeycomb(rotation_bee, default_bee, bee_two):
    return HoneyComb([rotation_bee, default_bee, bee_two], 10)


@pytest.fixture
def small_honeycomb(rotation_bee, bee_two):
    return HoneyComb([rotation_bee, bee_two], 4)


@pytest.fixture
def expected_bee_two_on_small_honeycomb(expected_bee_two_steps, small_honeycomb):
    i = 0
    for position, orientation in expected_bee_two_steps:
        if not small_honeycomb.__validate_position__(position):
            break
        else:
            i += 1
    for j in range(i, len(expected_bee_two_steps)):
        expected_bee_two_steps[j] = None
    return expected_bee_two_steps


def extend_expected_steps(steps_list):
    longest = max([len(steps) for steps in steps_list])
    i = 0
    for steps in steps_list:
        steps_list[i] = steps + [steps[-1]] * (longest - len(steps))
        i += 1
    return steps_list


def test_honeycomb_step_by_step(default_honeycomb, expected_bee_two_steps, expected_rotation_bee_steps,
                                rotation_bee, bee_two):
    expected_list = [expected_rotation_bee_steps, expected_bee_two_steps]
    extend_expected_steps(expected_list)
    j = 0
    for moves in default_honeycomb.simulate_next():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1


def test_honeycomb_all_steps(default_honeycomb, expected_bee_two_steps, expected_rotation_bee_steps,
                             rotation_bee, bee_two):
    expected_list = [expected_rotation_bee_steps, expected_bee_two_steps]
    extend_expected_steps(expected_list)
    j = 0
    for moves in default_honeycomb.simulate_all():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1


def test_honeycomb_mixed(default_honeycomb, expected_bee_two_steps, expected_rotation_bee_steps,
                         rotation_bee, bee_two):
    expected_list = [expected_rotation_bee_steps, expected_bee_two_steps]
    extend_expected_steps(expected_list)
    j = 0
    for moves in default_honeycomb.simulate_next():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1
        if j > 4:
            break
    for moves in default_honeycomb.simulate_all():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1


@pytest.fixture
def expected_small_bee_two_steps():
    return [
        ([2, 2], "W"),
        ([2, 2], "N"),
        ([2, 3], "N"),
        ([2, 4], "N"),
        None,
        None,
        None,
        None,
        None,
    ]


def test_small_honeycomb_step_by_step(small_honeycomb, expected_bee_two_on_small_honeycomb, expected_rotation_bee_steps,
                                      rotation_bee, bee_two):
    expected_list = [expected_rotation_bee_steps, expected_bee_two_on_small_honeycomb]
    extend_expected_steps(expected_list)
    j = 0
    for moves in small_honeycomb.simulate_next():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1


def test_add_bees(expected_bee_two_steps, expected_rotation_bee_steps, rotation_bee, bee_two):
    honeycomb = HoneyComb([], 10)
    honeycomb.add_bee(bee_two)
    honeycomb.add_bee(rotation_bee)
    expected_list = [expected_rotation_bee_steps, expected_bee_two_steps]
    extend_expected_steps(expected_list)
    j = 0
    for moves in honeycomb.simulate_all():
        for bee_uuid, move in moves.items():
            if bee_uuid == rotation_bee.get_id():
                assert move == expected_list[0][j]
            elif bee_uuid == bee_two.get_id():
                assert move == expected_list[1][j]
            else:
                assert False
        j += 1


def test_delete_bee(default_honeycomb, expected_bee_two_steps, rotation_bee, bee_two):
    default_honeycomb.delete_bee(rotation_bee.get_id())
    for i, moves in enumerate(default_honeycomb.simulate_next()):
        for bee_uuid, move in moves.items():
            assert move == expected_bee_two_steps[i]


def test_reset_bees(small_honeycomb, expected_bee_two_on_small_honeycomb, expected_rotation_bee_steps,
                    rotation_bee, bee_two):
    expected_list = [expected_rotation_bee_steps, expected_bee_two_on_small_honeycomb]
    extend_expected_steps(expected_list)
    # Simulate the entire honeycomb and verify the position is the latest of the expected list
    small_honeycomb.simulate_all()
    for bee_uuid, bee in small_honeycomb.get_bees().items():
        if bee_uuid == rotation_bee.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == expected_list[0][-1]
        elif bee_uuid == bee_two.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == expected_list[1][-1]
        else:
            assert False

    small_honeycomb.reset()

    # Reset the honeycomb and verify the position and moves are the initial ones of each bee
    for bee_uuid, bee in small_honeycomb.get_bees().items():
        if bee_uuid == rotation_bee.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == (
            [0, 0], 'N'), 'Rotation Bee: Position after reset is not matching'
            assert rotation_bee.get_moves() == 'LRLLRRRR', 'Rotation Bee: The moves after reset is not matching'
        elif bee_uuid == bee_two.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == (
            [3, 2], 'W'), 'Bee two: Position after reset is not matching'
            assert bee_two.get_moves() == 'MRMMMRMLM', 'Bee two: The moves after reset is not matching'
        else:
            assert False

    # Simulate the entire honeycomb again and verify the position is the latest of the expected list
    small_honeycomb.simulate_all()
    for bee_uuid, bee in small_honeycomb.get_bees().items():
        if bee_uuid == rotation_bee.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == expected_list[0][-1]
        elif bee_uuid == bee_two.get_id():
            assert small_honeycomb.get_bee_position(bee_uuid) == expected_list[1][-1]
        else:
            assert False
