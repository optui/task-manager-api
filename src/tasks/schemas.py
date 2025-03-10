from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, field_validator


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskBase(BaseModel):
    title: str
    description: str
    due_date: date
    status: TaskStatus = TaskStatus.pending


class TaskCreate(TaskBase):
    @field_validator("due_date")
    def check_due_date(cls, due_date):
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past.")
        return due_date


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None

    @field_validator("due_date")
    def check_due_date(cls, due_date):
        if due_date is None:
            return due_date
        if due_date < date.today():
            raise ValueError("Due date cannot be in the past.")
        return due_date


class TaskResponse(TaskBase):
    id: int
    creation_date: date

    class Config:
        from_attributes = True
