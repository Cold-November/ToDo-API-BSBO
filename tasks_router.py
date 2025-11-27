# tasks_router.py

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List, Dict, Any
from schemas import Task, TaskCreate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Временная база данных (список словарей)
tasks_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Сдать проект по FastAPI",
        "description": "Завершить разработку API и написать документацию",
        "is_important": True,
        "is_urgent": True,
        "quadrant": "Q1",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "title": "Изучить SQLAlchemy",
        "description": "Прочитать документацию и попробовать примеры",
        "is_important": True,
        "is_urgent": False,
        "quadrant": "Q2",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 3,
        "title": "Сходить на лекцию",
        "description": None,
        "is_important": False,
        "is_urgent": True,
        "quadrant": "Q3",
        "completed": False,
        "created_at": datetime.now()
    },
    {
        "id": 4,
        "title": "Посмотреть сериал",
        "description": "Новый сезон любимого сериала",
        "is_important": False,
        "is_urgent": False,
        "quadrant": "Q4",
        "completed": True,
        "created_at": datetime.now()
    },
]


# --------------------------
#        GET ALL TASKS
# --------------------------
@router.get("/", response_model=List[Task])
async def get_all_tasks():
    return tasks_db


# --------------------------
#      GET TASK BY ID
# --------------------------
@router.get("/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    task = next((t for t in tasks_db if t["id"] == task_id), None)

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task


# --------------------------
#      GET BY QUADRANT
# --------------------------
@router.get("/quadrant/{quadrant}", response_model=List[Task])
async def get_tasks_by_quadrant(quadrant: str):

    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4"
        )

    filtered_tasks = [t for t in tasks_db if t["quadrant"] == quadrant]
    return filtered_tasks


# --------------------------
#      TASKS STATISTICS
# --------------------------
@router.get("/stats")
async def get_tasks_stats() -> dict:
    total = len(tasks_db)

    by_quadrant = {
        "Q1": len([t for t in tasks_db if t["quadrant"] == "Q1"]),
        "Q2": len([t for t in tasks_db if t["quadrant"] == "Q2"]),
        "Q3": len([t for t in tasks_db if t["quadrant"] == "Q3"]),
        "Q4": len([t for t in tasks_db if t["quadrant"] == "Q4"]),
    }

    by_status = {
        "completed": len([t for t in tasks_db if t["completed"]]),
        "pending": len([t for t in tasks_db if not t["completed"]]),
    }

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }


# --------------------------
#     SEARCH TASKS
# --------------------------
@router.get("/search", response_model=List[Task])
async def search_tasks(q: str):

    if len(q) < 2:
        raise HTTPException(
            status_code=422,
            detail="Ключевое слово должно содержать минимум 2 символа"
        )

    q_lower = q.lower()

    filtered = [
        t for t in tasks_db
        if q_lower in t["title"].lower() or
        q_lower in (t["description"] or "").lower()
    ]

    return filtered


# --------------------------
#   FILTER BY STATUS
# --------------------------
@router.get("/status/{status}", response_model=List[Task])
async def get_tasks_by_status(status: str):

    if status not in ["completed", "pending"]:
        raise HTTPException(status_code=404, detail="Статус не найден")

    filtered = [
        t for t in tasks_db
        if t["completed"] is (status == "completed")
    ]

    return filtered
# --------------------------
#        CREATE TASK
# --------------------------
@router.post("/", response_model=Task, status_code=201)
async def create_task(task: TaskCreate):

    new_task = {
        "id": len(tasks_db) + 1,
        "created_at": datetime.now(),
        **task.dict()
    }

    tasks_db.append(new_task)
    return new_task