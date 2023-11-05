from dataclasses import dataclass
from datetime import datetime
from typing import List

from pydantic import Field

from cleanerrobot.app.dtos import Direction


@dataclass(frozen=True)
class StartPoint:
    x: int = Field(ge=-100_000, le=100_000)
    y: int = Field(ge=-100_000, le=100_000)


@dataclass(frozen=True)
class MoveCommand:
    direction: Direction
    steps: int = Field(gt=0, lt=100_000)


@dataclass(frozen=True)
class MoveCommandRequest:
    start: StartPoint
    commands: List[MoveCommand] = Field(max_length=10_000)


@dataclass
class MoveCommandResponse:
    id: int
    commands: int
    result: int
    duration: float
    timestamp: datetime
