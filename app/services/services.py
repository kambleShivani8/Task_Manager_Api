from sqlalchemy.orm import Session
from app.models.models import Task
from app.schemas.task import TaskCreate, TaskUpdate


# CREATE
def create_task(db: Session, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# READ
def get_tasks(db: Session):
    return db.query(Task).all()


# READ (filter + sort + pagination)
def get_tasks_filtered_sorted_paginated(
    db: Session,
    completed: bool | None,
    sort_by: str,
    order: str,
    page: int,
    size: int
):
    query = db.query(Task)

    if completed is not None:
        query = query.filter(Task.completed == completed)

    if sort_by == "title":
        column = Task.title
    else:
        column = Task.id

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    offset = (page - 1) * size
    return query.offset(offset).limit(size).all()


# UPDATE
def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.completed is not None:
        task.completed = task_data.completed

    if task_data.priority is not None:
        task.priority = task_data.priority

    db.commit()
    db.refresh(task)
    return task


# DELETE
def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return None

    db.delete(task)
    db.commit()
    return task
