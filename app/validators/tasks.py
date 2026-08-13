from pydantic import BaseModel, field_validator
from typing import Optional

from app.models import TaskStatus

class TaskRead(BaseModel):
    
    id: int
    name: str
    project_id: int
    assignee_id: int
    status: TaskStatus
    

class TaskCreate(BaseModel):
    
    name: str
    project_id: int
    assignee_id: int


class TaskUpdate(BaseModel):
    
    name: Optional[str] = None
    project_id: Optional[int] = None
    assignee_id: Optional[int] = None
    status: Optional[TaskStatus] = None    
    
    