from sqlalchemy import Engine
from sqlalchemy.orm import Session

from .models import Execution
from cleanerrobot.app.dtos import MoveCommandResult, MoveCommandExecution
from cleanerrobot.app.ports.output import CommandExecutionStorageManager


class ExecutionRepository(CommandExecutionStorageManager):
    engine: Engine

    def __init__(self, engine: Engine):
        self.engine = engine

    def save(self, command_results: MoveCommandResult) -> MoveCommandExecution:
        with Session(self.engine) as session:
            execution = Execution(
                commands=command_results.command_count,
                result=command_results.steps_count,
                duration=command_results.process_time
            )

            session.add(execution)
            session.commit()

            return MoveCommandExecution(
                execution.id,
                execution.commands,
                execution.result,
                execution.duration,
                execution.timestamp)
