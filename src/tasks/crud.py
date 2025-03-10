from datetime import date
from typing import List, Literal, Optional

from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from .models import Task
from .schemas import TaskCreate, TaskUpdate

from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def handle_db_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = args[0]
        try:
            result = func(*args, **kwargs)
            db.commit()
            return result
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Integrity error: {str(e)}",
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}",
            )

    return wrapper


def get_tasks(
    db: Session,
    status: Optional[str] = None,
    due_date: Optional[date] = None,
    sort_by: Optional[Literal["creation_date", "due_date"]] = None,
    order: Literal["asc", "desc"] = "asc",
) -> List[Task]:
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if due_date:
        query = query.filter(Task.due_date == due_date)

    if sort_by:
        column = getattr(Task, sort_by)
        sort_func = asc if order == "asc" else desc
        query = query.order_by(sort_func(column))

    return query.all()


def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found.",
        )
    return task


@handle_db_exceptions
def create(db: Session, task: TaskCreate) -> Task:
    task_data = task.model_dump()
    db_task = Task(**task_data)
    db.add(db_task)
    db.flush()
    db.refresh(db_task)
    return db_task


@handle_db_exceptions
def update(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found.",
        )
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
    return task


@handle_db_exceptions
def delete(db: Session, task_id: int) -> str:
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found.",
        )
    db.delete(task)
    return f"Task with id {task_id} deleted successfully"
