from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_important: bool
    deadline_at: Optional[datetime] = None      # вместо is_urgent пользователь передаёт дату

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_important: Optional[bool] = None
    deadline_at: Optional[datetime] = None

class TaskResponse(TaskBase):
    id: int
    is_urgent: bool
    quadrant: str
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    days_until_deadline: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)