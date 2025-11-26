# main.py
from fastapi import FastAPI
from tasks_router import router as tasks_router

app = FastAPI(
    title="ToDo API",
    version="1.0",
    contact={"name": "Дмитрий"}
)


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


# Подключаем router
app.include_router(tasks_router)
