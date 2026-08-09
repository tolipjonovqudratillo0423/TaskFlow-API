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


project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.post("/", response_model=ProjectRead, status_code=201)
def create_project(project_in: ProjectCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    project = repo.create(project_data=project_in.model_dump(), owner_id=current_user.id)
    return project


@project_router.get("/", response_model=list[ProjectRead], tags=["Projects"])
def get_all_projects(session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    projects = repo.get_all_projects_by_owner(owner_id=current_user.id)
    return projects
    

@project_router.get("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def get_project(project_id:int, session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    project = repo.get_project(project_id=project_id, owner_id=current_user.id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
    return project


@project_router.put("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def update_project(project_id:int, updated_project: ProjectUpdate, session:SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    project = repo.get_project(project_id=project_id, owner_id=current_user.id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project!"
        )
        
    for attrs, value in updated_project.model_dump(exclude_unset=True).items():
        setattr(project, attrs, value)
    session.commit()
    session.refresh(project)
    
    return project


@project_router.delete("/{project_id}", tags=["Projects"])
def delete_project(project_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = ProjectRepository(session)
    project = repo.get_project(project_id=project_id, owner_id=current_user.id)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
    if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have access to this project!"
            )
        
    project.is_active = False
    session.commit()
    session.refresh(project)

    return {
        "status": True,
        "message": f"'{project.name}' deleted!"
    }
    
    
    