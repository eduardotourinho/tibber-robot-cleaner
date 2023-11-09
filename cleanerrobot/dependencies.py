import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends

from .adapters.storage.db import initialize_db, get_db_config
from .adapters.storage.repositories import ExecutionRepository
from .app.ports.input import MoveCommandUseCase
from .app.ports.output import CommandExecutionStorageManager
from .app.services.robot_core import RobotCore

environment = os.environ.get("APP_ENV", "dev")

if environment == "dev":
    env_file_path = Path(f"{os.getcwd()}/.env")
else:
    env_file_path = Path(f"{os.getcwd()}/.env.{environment}")

load_dotenv(env_file_path)

engine = initialize_db(get_db_config())


def get_storage_manager() -> CommandExecutionStorageManager:
    yield ExecutionRepository(engine)


def get_move_service(
        storage_manager: CommandExecutionStorageManager = Depends(get_storage_manager)) -> MoveCommandUseCase:
    yield RobotCore(storage_manager)
