from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_session
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskResponse
from utils import calculate_urgency, determine_quadrant, calculate_days_until_deadline
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# CREATE
@router.post("/", response_model=TaskResponse)
async def create_task(data: TaskCreate, db: AsyncSession = Depends(get_async_session)):
    is_urgent = calculate_urgency(data.deadline_at)
    quadrant = determine_quadrant(data.is_important, is_urgent)

    task = Task(
        title=data.title,
        description=data.description,
        is_important=data.is_important,
        is_urgent=is_urgent,
        deadline_at=data.deadline_at,
        quadrant=quadrant,
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    task.days_until_deadline = calculate_days_until_deadline(task.deadline_at)
    return task


# READ ALL
@router.get("/", response_model=list[TaskResponse])
async def get_tasks(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()

    for t in tasks:
        t.days_until_deadline = calculate_days_until_deadline(t.deadline_at)

    return tasks


# READ ONE
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(404, "Задача не найдена")

    task.days_until_deadline = calculate_days_until_deadline(task.deadline_at)
    return task


# UPDATE
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int, data: TaskUpdate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(404, "Задача не найдена")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    task.is_urgent = calculate_urgency(task.deadline_at)
    task.quadrant = determine_quadrant(task.is_important, task.is_urgent)

    await db.commit()
    await db.refresh(task)

    task.days_until_deadline = calculate_days_until_deadline(task.deadline_at)
    return task


# DELETE
@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(404, "Задача не найдена")

    await db.delete(task)
    await db.commit()
    return {"message": "Удалено", "id": task_id}


# MARK COMPLETE
@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(404, "Задача не найдена")

    task.completed = True
    task.completed_at = datetime.now()

    await db.commit()
    await db.refresh(task)

    task.days_until_deadline = calculate_days_until_deadline(task.deadline_at)
    return task
