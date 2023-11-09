from typing import Annotated

from fastapi import Depends, APIRouter

from .schemas import MoveCommandResponse, MoveCommandRequest
from cleanerrobot.app.dtos import MoveCommand, Point, Command
from cleanerrobot.app.ports.input import MoveCommandUseCase
from cleanerrobot.dependencies import get_move_service

router = APIRouter()


@router.post("/tibber-developer-test/enter-path", response_model=MoveCommandResponse, status_code=201)
async def clean_command(request_move_command: MoveCommandRequest,
                        cleaner_service: Annotated[MoveCommandUseCase, Depends(get_move_service)],
                        size: int = 100_000) -> MoveCommandResponse:
    move_commands = MoveCommand(
        room_size=size,
        origin=Point(request_move_command.start.x, request_move_command.start.y),
        commands=[Command(direction=cmd.direction, steps=cmd.steps) for cmd in request_move_command.commands]
    )
    execution_response = cleaner_service.clean(move_command=move_commands)

    return MoveCommandResponse(
        id=execution_response.id,
        commands=execution_response.commands,
        result=execution_response.result,
        duration=execution_response.duration,
        timestamp=execution_response.timestamp
    )
