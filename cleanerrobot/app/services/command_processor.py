from time import perf_counter
from typing import List, Set

from ..dtos import Command, Point, Direction, MoveCommandResult


class CommandProcessor:

    def process_commands(self, origin: Point, commands: List[Command]) -> MoveCommandResult:
        start_time = perf_counter()

        visited_set = set()
        initial_position = origin

        for command in commands:
            processed_positions = self.process_move_command(initial_position, command)
            initial_position = processed_positions[len(processed_positions) - 1]

            visited_set |= set(processed_positions)

        end_time = perf_counter()

        return MoveCommandResult(steps=visited_set, command_count=len(commands), process_time=end_time - start_time)

    @staticmethod
    def process_move_command(origin: Point, command: Command) -> List[Point]:
        steps = []

        for i in range(0, command.steps + 1):
            new_position = None

            match command.direction:
                case Direction.NORTH:
                    new_position = Point(origin.x, origin.y + i)
                case Direction.SOUTH:
                    new_position = Point(origin.x, origin.y - i)
                case Direction.EAST:
                    new_position = Point(origin.x + i, origin.y)
                case Direction.WEST:
                    new_position = Point(origin.x - i, origin.y)

            steps.append(new_position)

        return steps
