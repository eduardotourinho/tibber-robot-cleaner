from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, auto
from typing import Set, List


class Direction(StrEnum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class Command:
    direction: Direction
    steps: int


@dataclass(frozen=True)
class MoveCommand:
    origin: Point
    commands: List[Command]


@dataclass(frozen=True)
class MoveCommandResult:
    steps: Set[Point]
    command_count: int
    process_time: float


@dataclass(frozen=True)
class MoveCommandExecution:
    id: int
    commands: int
    result: int
    duration: float
    timestamp: datetime
