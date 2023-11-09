import pytest

from datetime import datetime

import pytest

from cleanerrobot.adapters.storage.repositories import ExecutionRepository
from cleanerrobot.app.dtos import MoveCommandResult, Point, MoveCommandExecution


@pytest.fixture()
def subject(db_engine):
    return ExecutionRepository(db_engine)


def test_save(subject):
    command_result = MoveCommandResult(
        steps_count=5,
        command_count=2,
        process_time=0.000123
    )
    expected_execution = MoveCommandExecution(
        id=1,
        commands=2,
        result=5,
        duration=0.000123,
        timestamp=datetime.now()
    )
    actual_execution = subject.save(command_result)

    assert actual_execution.id == expected_execution.id
    assert actual_execution.result == expected_execution.result
    assert actual_execution.commands == expected_execution.commands
