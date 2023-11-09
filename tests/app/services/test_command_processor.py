import pytest

from cleanerrobot.app.dtos import Point, Command, Direction
from cleanerrobot.app.services.command_processor import process_clean_commands, to_array_coord

move_commands_data_provider = [
    (
        5,
        Point(0, 0),
        [Command(Direction.EAST, 1)],
        {Point(0, 0), Point(1, 0)},
    ),
    (
        5,
        Point(0, 0),
        [Command(Direction.EAST, 1), Command(Direction.WEST, 6)],
        {Point(0, 0), Point(1, 0),
         Point(0, 0), Point(0, -1), Point(0, -2), Point(0, -3), Point(0, -4), Point(0, -5)},
    ),
    (
        20,
        Point(10, 10),
        [Command(Direction.WEST, 10)],
        {Point(10, 10), Point(9, 10), Point(8, 10), Point(7, 10), Point(6, 10), Point(5, 10), Point(4, 10),
         Point(3, 10), Point(2, 10), Point(1, 10), Point(0, 10)},
    ),
    (
        10,
        Point(0, 0),
        [Command(Direction.NORTH, 2), Command(Direction.SOUTH, 5)],
        {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, -1), Point(0, -2),
         Point(0, -3)},
    ),
    (
        30,
        Point(-10, 20),
        [Command(Direction.NORTH, 2), Command(Direction.EAST, 5), Command(Direction.SOUTH, 1)],
        {Point(-10, 20), Point(-10, 21), Point(-10, 22), Point(-9, 22), Point(-8, 22),
         Point(-7, 22), Point(-6, 22), Point(-5, 22), Point(-5, 21)},
    ),
    (
        10,
        Point(0, 0),
        [Command(Direction.NORTH, 2), Command(Direction.EAST, 5), Command(Direction.SOUTH, 2),
         Command(Direction.NORTH, 3)],
        {Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 2), Point(2, 2),
         Point(3, 2), Point(4, 2), Point(5, 2), Point(5, 1), Point(5, 0), Point(5, 3)},
    ),
    (
        10,
        Point(-10, -10),
        [Command(Direction.EAST, 9), Command(Direction.NORTH, 10), Command(Direction.SOUTH, 5),
         Command(Direction.WEST, 4), Command(Direction.EAST, 10)],
        {Point(-10, -10), Point(-9, -10), Point(-8, -10), Point(-7, -10), Point(-6, -10), Point(-5, -10),
         Point(-4, -10), Point(-3, -10), Point(-2, -10), Point(-1, -10),
         Point(-1, -9), Point(-1, -8), Point(-1, -7), Point(-1, -6), Point(-1, -5), Point(-1, -4), Point(-1, -3),
         Point(-1, -2), Point(-1, -1), Point(-1, 0),
         Point(-1, -1), Point(-1, -2), Point(-1, -3), Point(-1, -4), Point(-1, -5),
         Point(-2, -5), Point(-3, -5), Point(-4, -5), Point(-5, -5),
         Point(-4, -5), Point(-3, -5), Point(-2, -5), Point(-1, -5), Point(0, -5), Point(1, -5), Point(2, -5),
         Point(3, -5), Point(4, -5), Point(5, -5)}
    )
]

# [room_size, cart_point, array_point]
point_transform_data_provider = [
    (3, Point(-1, 1), Point(0, 0)),
    (3, Point(0, 1), Point(1, 0)),
    (3, Point(1, 1), Point(2, 0)),
    (3, Point(0, -1), Point(1, 2)),
    (3, Point(0, 0), Point(1, 1)),
    (3, Point(0, 1), Point(1, 0)),
    (3, Point(-1, -1), Point(0, 2)),
    (3, Point(0, -1), Point(1, 2)),
    (3, Point(1, -1), Point(2, 2)),
    (20, Point(0, 0), Point(10, 10)),
    (20, Point(0, -10), Point(10, 20)),
    (20, Point(-10, 10), Point(0, 0)),
    (20, Point(-10, 0), Point(0, 10)),
    (20, Point(-10, -10), Point(0, 20)),
    (20, Point(10, -10), Point(20, 20)),
    (20, Point(10, 0), Point(20, 10)),
    (20, Point(10, 10), Point(20, 0)),
    (20, Point(0, 10), Point(10, 0)),
    (6, Point(-1, 2), Point(2, 1)),
    (6, Point(0, 0), Point(3, 3))
]


@pytest.mark.parametrize("room_size, origin, array_point", point_transform_data_provider)
def test_shift_point(room_size, origin, array_point):
    actual = to_array_coord(room_size, origin)

    assert actual == array_point, f"Cartesian point {origin} should be translated to array coordinate {array_point}"


@pytest.mark.parametrize("room_size, origin, commands, expected_set", move_commands_data_provider)
def test_process_room(room_size, origin, commands, expected_set):
    actual = process_clean_commands(room_size, origin, commands)

    assert actual.steps_count == len(expected_set), \
        f"Number of cleaned steps should be {len(expected_set)}. Actual: {actual.steps_count}"
    assert actual.command_count == len(commands), \
        f"Number of processed commands should be {len(commands)}. Actual: {actual.command_count}"
    assert actual.process_time > 0
