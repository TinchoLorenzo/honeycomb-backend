import pytest
from src.model.src.honeycomb.bee import Bee


def test_bee_creation():
    with pytest.raises(Exception) as excepinfo:
        Bee(0, 0, 'a', '')
    assert 'The values provided are not correct' in str(excepinfo.value)
    with pytest.raises(Exception) as excepinfo:
        Bee(0, 0, 'N', 'LR M')
    with pytest.raises(Exception) as excepinfo:
        Bee(0, 0, 'N', 'LRLRLRMMRMALM')
    assert 'The values provided are not correct' in str(excepinfo.value)
    with pytest.raises(Exception) as excepinfo:
        Bee(0, 0, 'NN', 'LRLRLRMMRMALM')
    assert 'The values provided are not correct' in str(excepinfo.value)


@pytest.fixture
def default_bee():
    return Bee(0, 0, 'N', '')


@pytest.fixture
def rotation_bee():
    return Bee(0, 0, 'N', 'LRLLRRRR')


@pytest.fixture
def expected_rotation_bee_steps():
    return [
        ([0, 0], "W"),
        ([0, 0], "N"),
        ([0, 0], "W"),
        ([0, 0], "S"),
        ([0, 0], "W"),
        ([0, 0], "N"),
        ([0, 0], "E"),
        ([0, 0], "S"),
    ]


@pytest.fixture
def bee_two():
    return Bee(3, 2, 'W', 'MRMMMRMLM')


@pytest.fixture
def expected_bee_two_steps():
    return [
        ([2, 2], "W"),
        ([2, 2], "N"),
        ([2, 3], "N"),
        ([2, 4], "N"),
        ([2, 5], "N"),
        ([2, 5], "E"),
        ([3, 5], "E"),
        ([3, 5], "N"),
        ([3, 6], "N"),
    ]


def test_step_by_step(bee_two, rotation_bee, expected_bee_two_steps, expected_rotation_bee_steps):
    for expected_step, actualL_step in zip(expected_rotation_bee_steps, rotation_bee.make_next_move()):
        bee_uuid, step = actualL_step
        assert step == expected_step
    for expected_step, actualL_step in zip(expected_bee_two_steps, bee_two.make_next_move()):
        bee_uuid, step = actualL_step
        assert step == expected_step


def test_all_at_once(bee_two, rotation_bee, expected_bee_two_steps, expected_rotation_bee_steps):
    for expected_step, actualL_step in zip(expected_rotation_bee_steps, rotation_bee.make_all_moves()):
        bee_uuid, step = actualL_step
        assert step == expected_step
    for expected_step, actualL_step in zip(expected_bee_two_steps, bee_two.make_all_moves()):
        bee_uuid, step = actualL_step
        assert step == expected_step


def test_mixed_moves(bee_two, rotation_bee, expected_bee_two_steps, expected_rotation_bee_steps):
    i = 0
    for expected_step, actualL_step in zip(expected_rotation_bee_steps, rotation_bee.make_next_move()):
        bee_uuid, step = actualL_step
        assert step == expected_step
        i += 1
        if i > 2:
            break

    for expected_step, actualL_step in zip(expected_rotation_bee_steps[i:], rotation_bee.make_all_moves()):
        bee_uuid, step = actualL_step
        assert step == expected_step
    i = 0

    for expected_step, actualL_step in zip(expected_bee_two_steps, bee_two.make_next_move()):
        bee_uuid, step = actualL_step
        assert step == expected_step
        i += 1
        if i > 4:
            break
    for expected_step, actualL_step in zip(expected_bee_two_steps[i:], bee_two.make_all_moves()):
        bee_uuid, step = actualL_step
        assert step == expected_step


def test_set_moves(default_bee: Bee):
    with pytest.raises(Exception) as excepinfo:
        default_bee.set_moves('LR M')
    assert default_bee.get_moves() == ''


def test_set_location(bee_two: Bee):
    bee_two.set_location(1, 1)
    assert bee_two.get_position()[0] == [1, 1]


def test_set_orientation(bee_two: Bee):
    bee_two.set_orientation('E')
    assert bee_two.get_position()[1] == 'E'


def test_reset(bee_two: Bee, expected_bee_two_steps):
    bee_two.make_all_moves()
    assert bee_two.get_position() == expected_bee_two_steps[-1], \
        'The position after making all moves is not matching'
    bee_two.reset()
    assert bee_two.get_position() == ([3,2], 'W'), 'Position after reset is not matching'
    assert bee_two.get_moves() == 'MRMMMRMLM', 'The moves after reset is not matching'
    bee_two.make_all_moves()
    assert bee_two.get_position() == expected_bee_two_steps[-1], \
        'The position after reset and then making all moves is not matching'
