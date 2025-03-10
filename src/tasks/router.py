from datetime import date
from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.core.dependencies import get_db

from .crud import create, delete, get_task, get_tasks, update
from .schemas import TaskCreate, TaskResponse, TaskStatus, TaskUpdate
from .suggestions import generate_smart_suggestions
from .suggestions_ai import generate_smart_suggestions_ai

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description=(
        "Create a new task by providing the necessary task details.\n\n"
        "The request should include:\n"
        "- **title**: Title of the task\n"
        "- **description**: Task details or description\n"
        "- **due_date**: Due date (YYYY-MM-DD)\n"
        "- **status**: (Optional) Task status (defaults to 'pending')\n\n"
        "The response returns the created"
        "task including its ID and creation date."
    ),
)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return create(db, task)


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="Retrieve all tasks with optional filters",
    description=(
        "Retrieve all tasks with optional filtering and sorting.\n\n"
        "- **status**: Filter by status (pending, in_progress, completed)\n"
        "- **due_date**: Filter by due date (expected format: YYYY-MM-DD)\n"
        "- **sort_by**: Field to sort by (creation_date, due_date)\n"
        "- **order**: Sort order (asc, desc)"
    ),
)
def read_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    due_date: Optional[date] = Query(
        None, description="Filter tasks by due date (YYYY-MM-DD)"
    ),
    sort_by: Optional[Literal["creation_date", "due_date"]] = Query(
        None, description='Sort tasks by "creation_date" or "due_date"'
    ),
    order: Optional[Literal["asc", "desc"]] = Query(
        None, description='Sorting order: "asc" or "desc"'
    ),
    db: Session = Depends(get_db),
):
    tasks = get_tasks(db, status, due_date, sort_by, order)
    return tasks


@router.get(
    "/suggestions",
    response_model=List[str],
    summary="Retrieve smart suggestions based on regex",
    description=(
        "Generate and retrieve task suggestions based on regex and patterns.\n\n"
    ),
)
def get_task_suggestions(db: Session = Depends(get_db)):
    suggestions = generate_smart_suggestions(db)
    return suggestions


@router.get(
    "/suggestions-ai",
    response_model=List[str],
    summary="Retrieve smart suggestions based on AI",
    description=("Generate and retrieve task suggestions based on an AI model.\n\n"),
)
def get_task_suggestions_ai(db: Session = Depends(get_db)):
    suggestions = generate_smart_suggestions_ai(db)
    return suggestions


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Retrieve details of a specific task",
    description=(
        "Retrieve a specific task by its ID.\n\n"
        "If a task with the given ID does not exist,"
        "the endpoint returns a 404 error."
    ),
)
def read_task(task_id: int, db: Session = Depends(get_db)):
    return get_task(db, task_id)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update an existing task",
    description=(
        "Update an existing task by providing"
        "any subset of task fields to be modified.\n\n"
        "The updated task is returned upon success."
    ),
)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    return update(db, task_id, task)


@router.delete(
    "/{task_id}",
    summary="Delete a task",
    description=(
        "Delete a task identified by its ID.\n\n"
        "If the deletion is successful, a confirmation message is returned.\n"
        "If the task does not exist, a 404 error is returned."
    ),
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return delete(db, task_id)
