from fastapi import FastAPI
from routers import tasks, stats
from scheduler import start_scheduler
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()            # <-- запускаем планировщик при старте
    print("Приложение запущено")
    yield                        # <-- сервер работает
    print("Приложение остановлено")


app = FastAPI(
    title="Task Manager API",
    version="2.0.0",
    lifespan=lifespan            # <-- современный способ вместо on_event
)

app.include_router(tasks.router, prefix="/api/v2")
app.include_router(stats.router, prefix="/api/v2")


@app.get("/")
async def root():
    return {"msg": "API работает!"}
