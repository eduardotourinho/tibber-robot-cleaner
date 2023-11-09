from time import perf_counter
from typing import Iterator

import numpy as np

from ..dtos import Command, Point, Direction, MoveCommandResult

direction_lookup_map = {
    Direction.NORTH: lambda i, origin: Point(origin.x, origin.y + i),
    Direction.SOUTH: lambda i, origin: Point(origin.x, origin.y - i),
    Direction.EAST: lambda i, origin: Point(origin.x + i, origin.y),
    Direction.WEST: lambda i, origin: Point(origin.x - i, origin.y),
}


def generate_command_queue(origin: Point, commands: list[Command]) -> Iterator[tuple[Point, Command]]:
    initial_position = origin
    for command in commands:
        yield initial_position, command
        initial_position = direction_lookup_map[command.direction](command.steps, initial_position)


def to_array_coord(room_size: int, point: Point) -> Point:
    size = int(room_size / 2)
    adjusted_x = point.x + size
    adjusted_y = size - point.y

    return Point(adjusted_x, adjusted_y)


def process_clean_commands(room_size: int, origin: Point, commands: list[Command]) -> MoveCommandResult:
    start_time = perf_counter()
    double_room_size = room_size * 2 + 1

    grid = np.full((double_room_size, double_room_size), False, dtype=bool)
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

                visited_grid_nodes = grid[initial_y:final_y, origin_array_point.x]
                visited_nodes_mask = np.full((1, len(visited_grid_nodes)), True, dtype=bool)
                grid[initial_y:final_y, origin_array_point.x] = visited_nodes_mask

            case Direction.EAST | Direction.WEST:
                if command.direction == Direction.EAST:
                    initial_x = origin_array_point.x
                    final_x = origin_array_point.x + command.steps + 1
                else:
                    initial_x = origin_array_point.x - command.steps
                    final_x = origin_array_point.x + 1

                visited_grid_nodes = grid[origin_array_point.y, initial_x:final_x]
                visited_nodes_mask = np.full((1, len(visited_grid_nodes)), True, dtype=bool)
                grid[origin_array_point.y, initial_x:final_x] = visited_nodes_mask

        processed_commands += 1

    visited_nodes = int(np.count_nonzero(grid))
    end_time = perf_counter()

    return MoveCommandResult(command_count=processed_commands, process_time=end_time - start_time,
                             steps_count=visited_nodes)
