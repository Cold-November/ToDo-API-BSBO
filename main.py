# main.py
from fastapi import FastAPI
from tasks_router import router as tasks_router

app = FastAPI(
    title="ToDo API",
    version="3.0",
    description="Практика 3: Pydantic-схемы и валидация данных",
    contact={"name": "Малякин Дмитрий"}
)

@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в ToDo API (Практика 3)!",
        "version": app.version,
        "info": "Используются Pydantic-схемы и валидация данных"
    }

# подключение маршрутов
app.include_router(tasks_router)