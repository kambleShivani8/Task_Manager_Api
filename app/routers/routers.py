from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.services import (
    create_task,
    get_tasks_filtered_sorted_paginated,
    update_task,
    delete_task,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# CREATE TASK
# -------------------------
@router.post("/", response_model=TaskResponse)
def create_task_api(
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task)


# -------------------------
# READ TASKS (Filter + Pagination)
# -------------------------
@router.get("/", response_model=list[TaskResponse])
def list_tasks_api(
    completed: bool | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return get_tasks_filtered_sorted_paginated(
        db=db,
        completed=completed,
        sort_by="id",
        order="asc",
        page=page,
        size=size,
    )


# -------------------------
# UPDATE TASK
# -------------------------
@router.put("/{task_id}", response_model=TaskResponse)
def update_task_api(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    updated_task = update_task(db, task_id, task)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


# -------------------------
# DELETE TASK
# -------------------------
@router.delete("/{task_id}")
def delete_task_api(
    task_id: int,
    db: Session = Depends(get_db),
):
    deleted_task = delete_task(db, task_id)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
