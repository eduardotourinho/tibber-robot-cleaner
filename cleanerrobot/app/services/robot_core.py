from .command_processor import process_clean_commands
from ..dtos import MoveCommandExecution
from ..ports.input import MoveCommandUseCase, MoveCommand
from ..ports.output import CommandExecutionStorageManager


class RobotCore(MoveCommandUseCase):
    history_saver: CommandExecutionStorageManager

    def __init__(self, history_saver: CommandExecutionStorageManager):
        self.history_saver = history_saver

    def clean(self, move_command: MoveCommand) -> MoveCommandExecution:
        commands_result = process_clean_commands(move_command.room_size, move_command.origin,
                                                 move_command.commands)

        return self.history_saver.save(commands_result)
