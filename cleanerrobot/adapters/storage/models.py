from datetime import datetime

from sqlalchemy import DateTime, func, Double
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class Execution(BaseModel):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True, server_default=func.now())
    commands: Mapped[int]
    result: Mapped[int]
    duration: Mapped[float] = mapped_column(Double(precision=10))

    def __repr__(self) -> str:
        return (f"Execution("
                f"id: {self.id!r}, "
                f"commands: {self.commands!r}, "
                f"result: {self.result!r}, "
                f"timestamp:{self.timestamp!r})")
