# Главный файл приложения
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
from datetime import datetime

app = FastAPI(
    title="ToDo API",
    version="1.0",
    contact={
        "name": "Дмитрий",
    }
)


# Временное хранилище (позже будет заменено на PostgreSQL)
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

@app.get("/")
async def root() -> dict:
    return {
        "message": "Добро пожаловать в ToDo API!",
        "app": {
            "title": app.title,
            "version": app.version,
            "description": app.description,
            "contact": app.contact,
        }
    }

@app.get("/tasks")
async def get_all_tasks() -> dict:
    return {
        "count": len(tasks_db), # считает количество записей в хранилище
        "tasks": tasks_db # выводит всё, чта есть в хранилище
    }
@app.get("/tasks/quadrant/{quadrant}")
async def get_tasks_by_quadrant(quadrant: str) -> dict:
    if quadrant not in ["Q1", "Q2", "Q3", "Q4"]:
        raise HTTPException(
            status_code=400,
            detail="Неверный квадрант. Используйте: Q1, Q2, Q3, Q4"
        )
    filtered_tasks = [
        task # ЧТО добавляем в список
        for task in tasks_db # ОТКУДА берем элементы
if task["quadrant"] == quadrant # УСЛОВИЕ фильтрации
]
    return {
        "quadrant": quadrant,
        "count": len(filtered_tasks),
        "tasks": filtered_tasks
    }


@app.get("/tasks/stats")
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
        "pending": len([t for t in tasks_db if not t["completed"]])
    }

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }



@app.get("/tasks/search")
async def search_tasks(q: str) -> dict:
    if len(q) < 2:
        raise HTTPException(status_code=422, detail="Ключевое слово слишком короткое")

    q_lower = q.lower()

    filtered = [
        t for t in tasks_db
        if q_lower in t["title"].lower() or q_lower in (t["description"] or "").lower()
    ]

    return {
        "query": q,
        "count": len(filtered),
        "tasks": filtered
    }

@app.get("/tasks/status/{status}")
async def get_tasks_by_status(status: str) -> dict:
    if status not in ["completed", "pending"]:
        raise HTTPException(status_code=404, detail="Статус не найден")

    filtered = [
        t for t in tasks_db
        if t["completed"] is (status == "completed")
    ]

    return {
        "status": status,
        "count": len(filtered),
        "tasks": filtered
    }

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int) -> dict:
    task = next((t for t in tasks_db if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task
