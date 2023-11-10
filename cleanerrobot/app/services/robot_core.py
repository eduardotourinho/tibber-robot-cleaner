import cleanerrobot.app.services.processors.array_processor as ap
import cleanerrobot.app.services.processors.set_processor as sp
from ..dtos import MoveCommandExecution
from ..ports.input import MoveCommandUseCase, MoveCommand
from ..ports.output import CommandExecutionStorageManager

COMMANDS_LEN_THRESHOLD = 1000


class RobotCore(MoveCommandUseCase):
    history_saver: CommandExecutionStorageManager

    def __init__(self, history_saver: CommandExecutionStorageManager, command_threshold=COMMANDS_LEN_THRESHOLD):
        self.history_saver = history_saver
        self.commands_threshold = command_threshold

    def clean(self, move_command: MoveCommand) -> MoveCommandExecution:
        print(len(move_command.commands))
        if len(move_command.commands) >= self.commands_threshold:
            process_command = ap.process_clean_commands
        else:
            process_command = sp.process_clean_commands

        commands_result = process_command(move_command.room_size, move_command.origin,
                                          move_command.commands)

        return self.history_saver.save(commands_result)
