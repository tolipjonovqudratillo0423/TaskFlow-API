from fastapi import APIRouter, HTTPException, Depends

from app.validators import (
    TaskRead, 
    TaskCreate,
    TaskUpdate
)
from app.services import TaskService
from app.db import SessionDep
from app.repositories import TaskRepository
from app.api import get_current_user
from app.models import User


task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("/", response_model=TaskRead, tags=["Tasks"])
def create(task_in: TaskCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo, session)
    
    task = service.create(task_data=task_in.model_dump(), owner_id=current_user.id)
    return task
