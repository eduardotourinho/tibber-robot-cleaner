from .command_processor import CommandProcessor
from ..dtos import MoveCommandExecution
from ..ports.input import MoveCommandUseCase, MoveCommand
from ..ports.output import CommandExecutionStorageManager


class RobotCore(MoveCommandUseCase):
    command_processor: CommandProcessor
    history_saver: CommandExecutionStorageManager

    def __init__(self, command_processor: CommandProcessor, history_saver: CommandExecutionStorageManager):
        self.command_processor = command_processor
        self.history_saver = history_saver

    def clean(self, move_command: MoveCommand) -> MoveCommandExecution:
        commands_result = self.command_processor.process_commands(move_command.origin, move_command.commands)

        return self.history_saver.save(commands_result)
