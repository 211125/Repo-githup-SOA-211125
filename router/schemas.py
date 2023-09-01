from pydantic import BaseModel
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    completed: bool  
    created_at: datetime
    class Config:
        from_attributes = True
