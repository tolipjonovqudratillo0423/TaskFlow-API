from fastapi import APIRouter, HTTPException, Depends

from app.validators import (
    TaskRead, 
    TaskCreate,
    TaskUpdate
)
from app.services import TaskService
from app.db import SessionDep
from app.repositories import TaskRepository
from app.api import get_current_user, project_router
from app.models import User



task_router = APIRouter(prefix="/tasks", tags=["Tasks"])
# owner_task_router = 



@task_router.post("/", response_model=TaskRead, tags=["Tasks"])
def create(task_in: TaskCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo, session)
    
    task = service.create(task_data=task_in.model_dump(), owner_id=current_user.id)
    return task


@task_router.get("/{task_id}", response_model=TaskRead, tags=["Tasks"])
def get_task_by_id(task_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo, session)
    
    task = service.get_task_by_id(task_id=task_id, current_user_id=current_user.id)
    return task


@task_router.get("/owner", response_model=list[TaskRead], tags=["Tasks"])
def get_all_task_by_owner(session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo, session)
    
    tasks = service.get_all_tasks_by_owner(owner_id=current_user.id)
    return tasks


@project_router.get("/{project_id}/tasks/owner", response_model=list[TaskRead], tags=["Tasks"])
def get_all_task_by_owner_and_project(project_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo, session)
    
    tasks = service.get_all_tasks_by_owner_and_project(owner_id=current_user.id, project_id=project_id)
    return tasks


@task_router.get("/assignee", response_model=list[TaskRead], tags=["Tasks"])
def get_all_task_by_assignee(session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    
    tasks = service.get_all_tasks_by_assignee(assignee_id=current_user.id)
    return tasks


@project_router.get("/{project_id}/tasks/assignee", response_model=list[TaskRead], tags=["Tasks"])
def get_all_tasks_by_assignee_and_project(project_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    
    tasks = service.get_all_tasks_by_assignee_and_project(assignee_id=current_user.id, project_id=project_id)
    return tasks


@task_router.put("/{task_id}", response_model=TaskRead, tags=["Tasks"])
def update(task_id: int, updated_task: TaskUpdate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    
    task = service.update(task_id=task_id, updated_task=updated_task.model_dump(), current_user_id=current_user.id)
    return task


@task_router.delete("/{task_id}", response_model=TaskRead, tags=["Tasks"])
def delete(task_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TaskRepository(session)
    service = TaskService(repo)
    
    task = service.delete(task_id=task_id, current_user_id=current_user.id)
    return {
        "status": True,
        "message": f"'{task.name}' was deleted!"
    }









