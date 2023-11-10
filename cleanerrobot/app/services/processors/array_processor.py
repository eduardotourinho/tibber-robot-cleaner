from time import perf_counter

import numpy as np

from cleanerrobot.app.dtos import Command, Point, Direction, MoveCommandResult
from cleanerrobot.app.services.processors import generate_command_queue, to_array_coord


def process_clean_commands(room_size: int, origin: Point, commands: list[Command]) -> MoveCommandResult:
    double_room_size = room_size * 2 + 1
    grid = _init_room(double_room_size)

    start_time = perf_counter()
    processed_commands = 0

    for origin_point, command in generate_command_queue(origin, commands):
        origin_array_point = to_array_coord(double_room_size, origin_point)
        match command.direction:
            case Direction.NORTH | Direction.SOUTH:
                if command.direction == Direction.NORTH:
                    initial_y = origin_array_point.y - command.steps
                    final_y = origin_array_point.y + 1
                else:
                    initial_y = origin_array_point.y
                    final_y = initial_y + command.steps + 1

                _set_visited_nodes(grid, Point(origin_array_point.x, initial_y), Point(origin_array_point.x, final_y))

            case Direction.EAST | Direction.WEST:
                if command.direction == Direction.EAST:
                    initial_x = origin_array_point.x
                    final_x = origin_array_point.x + command.steps + 1
                else:
                    initial_x = origin_array_point.x - command.steps
                    final_x = origin_array_point.x + 1

                _set_visited_nodes(grid, Point(initial_x, origin_array_point.y), Point(final_x, origin_array_point.y))

        processed_commands += 1

    visited_nodes = _count_cleaned_nodes(grid)
    end_time = perf_counter()

    return MoveCommandResult(command_count=processed_commands, process_time=end_time - start_time,
                             steps_count=visited_nodes)


def _init_room(room_size: int) -> np.ndarray:
    return np.zeros((room_size, room_size), dtype=np.byte)


def _create_mask_array(size: int) -> np.ndarray:
    return np.ones(size, dtype=np.byte)


def _count_cleaned_nodes(grid: np.ndarray) -> int:
    return int(np.count_nonzero(grid))


def _set_visited_nodes(grid: np.ndarray, origin: Point, final: Point) -> None:
    if origin.x == final.x:
        visited_nodes_mask = _create_mask_array(final.y - origin.y)
        grid[origin.y:final.y, origin.x] = visited_nodes_mask
    else:
        visited_nodes_mask = _create_mask_array(final.x - origin.x)
        grid[origin.y, origin.x:final.x] = visited_nodes_mask
