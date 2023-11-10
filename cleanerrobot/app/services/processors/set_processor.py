import functools
from time import perf_counter

from cleanerrobot.app.dtos import Command, Point, Direction, MoveCommandResult
from cleanerrobot.app.services.processors import generate_command_queue, to_array_coord


def process_clean_commands(room_size: int, origin: Point, commands: list[Command]) -> MoveCommandResult:
    double_room_size = room_size * 2 + 1

    start_time = perf_counter()
    processed_commands = 0
    visited_set = set()

    for origin_point, command in generate_command_queue(origin, commands):
        origin_array_point = to_array_coord(double_room_size, origin_point)
        cleaned_set = _process_command(origin_array_point, command)

        visited_set.update(cleaned_set)
        processed_commands += 1

    visited_nodes = _count_cleaned_nodes(visited_set)
    end_time = perf_counter()

    return MoveCommandResult(command_count=processed_commands, process_time=end_time - start_time,
                             steps_count=visited_nodes)


def _count_cleaned_nodes(visited_set: set) -> int:
    return len(visited_set)


def _set_visited_nodes(origin: Point, final: Point) -> set:
    if origin.x == final.x:
        visited_nodes = {Point(origin.x, py + origin.y) for py in range(final.y - origin.y)}
    else:
        visited_nodes = {Point(px + origin.x, origin.y) for px in range(final.x - origin.x)}

    return visited_nodes


def _process_command(origin: Point, command: Command) -> set:
    match command.direction:
        case Direction.NORTH | Direction.SOUTH:
            if command.direction == Direction.NORTH:
                initial_y = origin.y - command.steps
                final_y = origin.y + 1
            else:
                initial_y = origin.y
                final_y = initial_y + command.steps + 1

            return _set_visited_nodes(Point(origin.x, initial_y), Point(origin.x, final_y))

        case Direction.EAST | Direction.WEST:
            if command.direction == Direction.EAST:
                initial_x = origin.x
                final_x = origin.x + command.steps + 1
            else:
                initial_x = origin.x - command.steps
                final_x = origin.x + 1

            return _set_visited_nodes(Point(initial_x, origin.y), Point(final_x, origin.y))
