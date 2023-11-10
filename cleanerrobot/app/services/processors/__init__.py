from typing import Iterator

from cleanerrobot.app.dtos import Point, Command, Direction

direction_lookup_map = {
    Direction.NORTH: lambda i, origin: Point(origin.x, origin.y + i),
    Direction.SOUTH: lambda i, origin: Point(origin.x, origin.y - i),
    Direction.EAST: lambda i, origin: Point(origin.x + i, origin.y),
    Direction.WEST: lambda i, origin: Point(origin.x - i, origin.y),
}


def generate_command_queue(origin: Point, commands: list[Command]) -> Iterator[tuple[Point, Command]]:
    next_origin = origin
    for command in commands:
        yield next_origin, command
        next_origin = direction_lookup_map[command.direction](command.steps, next_origin)


def to_array_coord(room_size: int, point: Point) -> Point:
    size = int(room_size / 2)
    adjusted_x = point.x + size
    adjusted_y = size - point.y

    return Point(adjusted_x, adjusted_y)
