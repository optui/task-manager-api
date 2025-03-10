from sqlalchemy import Column, Date, Enum, Integer, String, func
from src.core.database import Base
from .schemas import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    creation_date = Column(Date, nullable=False, server_default=func.date("now"))
    due_date = Column(Date)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
