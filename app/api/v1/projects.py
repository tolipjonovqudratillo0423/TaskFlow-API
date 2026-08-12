from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select

from app.db.session import SessionDep
from app.models import Project, User
from app.validators import (
    ProjectRead,
    ProjectCreate,
    ProjectUpdate
)
from app.api import get_current_user
from app.repositories import ProjectRepository
from app.services import ProjectService, ProjectNotFoundError, ProjectAccessDeniedError


project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("/", response_model=ProjectRead, status_code=201)
def create_project(project_in: ProjectCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    service = ProjectService(repo)
    
    try:
        project = service.create(project_data=project_in.model_dump(), owner_id=current_user.id)
        return project
    except ProjectNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except ProjectAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")


@project_router.get("/", response_model=list[ProjectRead], tags=["Projects"])
def get_all_projects(session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    service = ProjectService(repo)
    
    try:
        projects = service.get_all_projects_by_owner(owner_id=current_user.id)
        return projects
    except ProjectNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except ProjectAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")
    

@project_router.get("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def get_project(project_id:int, session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    service = ProjectService(repo)
    
    try:
        project = service.get_project(project_id=project_id, owner_id=current_user.id)
        return project
    except ProjectNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except ProjectAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")


@project_router.put("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def update_project(project_id:int, updated_project: ProjectUpdate, session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    service = ProjectService(repo)
    try:
        project = service.update(project_id=project_id,
                                 owner_id=current_user.id,
                                 updated_project=updated_project.model_dump()
                                 )
        return project
    except ProjectNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except ProjectAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")


@project_router.delete("/{project_id}", tags=["Projects"])
def delete_project(project_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    service = ProjectService(repo)
    
    try:
        project = service.delete(project_id=project_id, owner_id=current_user.id)
        return {
            "status": True,
            "message": f"'{project.name}' deleted!"
        }
    except ProjectNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except ProjectAccessDeniedError:
        raise HTTPException(status_code=403, detail="Access denied")
    
    
    