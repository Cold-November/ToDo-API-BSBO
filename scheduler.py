from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_async_session
from models import Task
from utils import calculate_urgency, determine_quadrant
import asyncio


async def update_task_urgency():
    async for db in get_async_session():
        result = await db.execute(select(Task))
        tasks = result.scalars().all()

        updated = 0
        for task in tasks:
            old_urgent = task.is_urgent
            new_urgent = calculate_urgency(task.deadline_at)
            new_quadrant = determine_quadrant(task.is_important, new_urgent)

            if old_urgent != new_urgent or task.quadrant != new_quadrant:
                task.is_urgent = new_urgent
                task.quadrant = new_quadrant
                updated += 1

        if updated > 0:
            await db.commit()
            print(f"Обновлено задач: {updated}")
        else:
            print("Обновление не требуется")


def start_scheduler():
    scheduler = AsyncIOScheduler()

    #ежедневный запуск в 09:00
    scheduler.add_job(update_task_urgency, trigger='cron', hour=9, minute=0)

    # для теста каждые 5 минут (включи → протестируй → потом закомментируй)
    scheduler.add_job(update_task_urgency, trigger='interval', minutes=5)

    scheduler.start()
    print("Scheduler запущен")
