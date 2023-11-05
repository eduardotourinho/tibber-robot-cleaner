import pytest

from cleanerrobot.app.dtos import Point, Command, Direction
from cleanerrobot.app.services.command_processor import CommandProcessor

move_commands_data_provider = [
    (
        Point(0, 0),
        [Command(Direction.EAST, 1)],
        {Point(0, 0), Point(1, 0)},
    ),
    (
        Point(10, 10),
        [Command(Direction.WEST, 10)],
        {Point(10 - i, 10) for i in range(11)},
    ),
    (
        Point(0, 0),
        [Command(Direction.NORTH, 2), Command(Direction.SOUTH, 5)],
        {Point(0, 0), Point(0, 1), Point(0, 2), Point(0, -1), Point(0, -2),
         Point(0, -3)},
    ),
    (
        Point(-10, 20),
        [Command(Direction.NORTH, 2), Command(Direction.EAST, 5), Command(Direction.SOUTH, 1)],
        {Point(-10, 20), Point(-10, 21), Point(-10, 22), Point(-9, 22), Point(-8, 22),
         Point(-7, 22), Point(-6, 22), Point(-5, 22), Point(-5, 21)},
    ),
    (
        Point(0, 0),
        [Command(Direction.NORTH, 2), Command(Direction.EAST, 5), Command(Direction.SOUTH, 2),
         Command(Direction.NORTH, 3)],
        {Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 2), Point(2, 2),
         Point(3, 2), Point(4, 2), Point(5, 2), Point(5, 1), Point(5, 0), Point(5, 3)},
    ),
]

single_command_data_provider = [
    (
        Point(0, 0),
        Command(Direction.NORTH, 10),
        [Point(0, i) for i in range(11)]
    ),
    (
        Point(0, 0),
        Command(Direction.EAST, 10),
        [Point(i, 0) for i in range(0, 11)]
    ),
    (
        Point(0, 0),
        Command(Direction.SOUTH, 10),
        [Point(0, i - 10) for i in range(10, -1, -1)]
    ),
    (
        Point(0, 0),
        Command(Direction.WEST, 10),
        [Point(i - 10, 0) for i in range(10, -1, -1)]
    ),
]


@pytest.fixture()
def subject():
    yield CommandProcessor()


@pytest.mark.parametrize("origin, commands, expected_set", move_commands_data_provider)
def test_process_commands(subject, origin, commands, expected_set):
    actual_result = subject.process_commands(origin, commands)

    assert actual_result.steps == expected_set
    assert actual_result.command_count == len(commands)
    assert actual_result.process_time > 0.0


@pytest.mark.parametrize("origin, command, expected_positions", single_command_data_provider)
def test_process_move_command(subject, origin, command, expected_positions):
    actual_positions = subject.process_move_command(origin, command)

    assert expected_positions == actual_positions
