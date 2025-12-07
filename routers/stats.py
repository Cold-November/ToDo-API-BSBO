from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Task
from database import get_async_session

router = APIRouter(prefix="/stats", tags=["Statistics"])

@router.get("/")
async def stats(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()

    total = len(tasks)
    quadrant = {"Q1":0,"Q2":0,"Q3":0,"Q4":0}
    status = {"completed":0,"pending":0}

    for t in tasks:
        quadrant[t.quadrant] += 1
        status["completed" if t.completed else "pending"] += 1

    return {"total": total, "quadrant": quadrant, "status": status}

@router.get("/timing")
async def deadline_stats(db: AsyncSession = Depends(get_async_session)):
    from datetime import datetime, timezone
    result = await db.execute(select(Task))
    tasks = result.scalars().all()

    now = datetime.now(timezone.utc)
    return [{
        "title": t.title,
        "description": t.description,
        "created_at": t.created_at,
        "days_left": (t.deadline_at - now).days if t.deadline_at else None
    } for t in tasks if not t.completed]
