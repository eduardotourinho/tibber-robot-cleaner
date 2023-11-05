from abc import ABC, abstractmethod

from ..dtos import MoveCommand, MoveCommandExecution


class MoveCommandUseCase(ABC):

    @abstractmethod
    def clean(self, move_command: MoveCommand) -> MoveCommandExecution:
        pass
