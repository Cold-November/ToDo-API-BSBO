# Описание проекта и инструкция по запуску

# ToDo API (FastAPI)

Учебное API для работы со списком задач по матрице Эйзенхауэра. Реализовано на FastAPI с поддержкой фильтрации, поиска, статистики и получения задач по ID.

## Функциональность

- `/` — информация о приложении  
- `/tasks` — список всех задач  
- `/tasks/quadrant/{quadrant}` — задачи по квадранту (Q1–Q4)  
- `/tasks/search?q=...` — поиск по ключевому слову  
- `/tasks/status/{status}` — фильтрация по статусу  
- `/tasks/stats` — статистика по задачам  
- `/tasks/{task_id}` — задача по ID  

## Структура проекта
ToDo-API-BSBO/
├── main.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
├── README.md
└── venv/

## Установка и запуск

```bash
git clone https://github.com/Cold-November/ToDo-API-BSBO.git
cd ToDo-API-BSBO
python -m venv venv
.\venv\Scripts\Activate.ps1  # PowerShell
pip install -r requirements.txt
uvicorn main:app --reload
