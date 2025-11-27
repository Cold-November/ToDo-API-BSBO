from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Базовая схема данных (то, что приходит от пользователя)
class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        title="Название задачи",
        example="Сходить на тренировку"
    )

    description: Optional[str] = Field(
        None,
        max_length=300,
        title="Описание задачи",
        example="Фулбади тренировка по плану"
    )

    is_important: bool = Field(
        ...,
        title="Важность задачи",
        example=True
    )

    is_urgent: bool = Field(
        ...,
        title="Срочность задачи",
        example=False
    )

    quadrant: str = Field(
        ...,
        pattern="^(Q1|Q2|Q3|Q4)$",
        title="Квадрант из матрицы Эйзенхауэра",
        example="Q2"
    )

    completed: bool = Field(
        False,
        title="Статус выполнения",
        example=False
    )


# Схема создания задачи (POST)
class TaskCreate(TaskBase):
    pass


# Схема ответа (то, что возвращает сервер)
class Task(TaskBase):
    id: int = Field(..., example=1)
    created_at: datetime = Field(..., example="2025-01-20T14:43:00")

    class Config:
        from_attributes = True