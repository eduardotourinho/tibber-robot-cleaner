import os
from dataclasses import dataclass

from sqlalchemy import create_engine, Engine

from .models import BaseModel


@dataclass
class DbConfig:
    db_host: str
    db_port: int
    database: str
    db_schema: str
    user: str
    password: str


def get_db_config() -> DbConfig:
    return DbConfig(
        db_host=os.environ.get("DB_HOST", "localhost"),
        db_port=int(os.environ.get("DB_PORT", "5432")),
        database=os.environ.get("DB_NAME"),
        db_schema=os.environ.get("DB_SCHEMA"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )


def get_connection_string(config: DbConfig) -> str:
    return (f"postgresql+psycopg://{config.user}:{config.password}@{config.db_host}:{config.db_port}"
            f"/{config.database}?options=-csearch_path={config.db_schema}")


def get_db_engine(conn_str: str | None = None) -> Engine:
    return create_engine(conn_str, echo=True)


def drop_all_tables(engine: Engine) -> None:
    BaseModel.metadata.drop_all(engine)


def initialize_db(config: DbConfig) -> Engine:
    conn_str = get_connection_string(config)
    engine = get_db_engine(conn_str)
    BaseModel.metadata.create_all(engine)

    return engine
