import pytest

from datetime import datetime
from typing import List, Set
from unittest.mock import Mock

import pytest

from cleanerrobot.app.services.command_processor import process_clean_commands
from cleanerrobot.app.dtos import MoveCommandExecution, MoveCommandResult
from cleanerrobot.app.ports.output import CommandExecutionStorageManager
from cleanerrobot.app.ports.input import MoveCommand
from cleanerrobot.app.dtos import Point, Command, Direction
from cleanerrobot.app.services.robot_core import RobotCore

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
    )
]


@pytest.fixture()
def storage(mocker):
    mock = Mock(spec=CommandExecutionStorageManager)
    mocker.patch('cleanerrobot.app.ports.output.CommandExecutionStorageManager.save', return_value=mock)
    yield mock


@pytest.fixture()
def subject(storage: CommandExecutionStorageManager):
    yield RobotCore(storage)


@pytest.mark.parametrize("origin, commands, expected_set", move_commands_data_provider)
def test_process_commands(subject, storage, mocker,
                          origin: Point, commands: List[Command], expected_set: Set[Point]):
    mocked_return = MoveCommandResult(len(commands), 0.000123, len(expected_set))
    mocker.patch("cleanerrobot.app.services.command_processor.process_clean_commands", return_value=mocked_return)

    storage.save.return_value = MoveCommandExecution(1, len(commands), len(expected_set), 0.000123,
                                                     datetime.now())

    actual_result = subject.clean(MoveCommand(origin, commands, room_size=10))

    assert actual_result.commands == len(commands)
    assert actual_result.result == len(expected_set)

    # command_processor_mock.process_clean_commands.assert_called_once_with(origin, commands)
    storage.save.assert_called_once()
