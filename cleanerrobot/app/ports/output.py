from abc import ABC, abstractmethod

from ..dtos import MoveCommandResult, MoveCommandExecution


class CommandExecutionStorageManager(ABC):

    @abstractmethod
    def save(self, command_results: MoveCommandResult) -> MoveCommandExecution:
        pass
