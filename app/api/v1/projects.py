from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import SessionDep
from app.models import Project
from app.validators import (
    ProjectRead,
    ProjectCreate,
    ProjectUpdate
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(project_in: ProjectCreate, session: SessionDep):
    
    project = Project(**project_in.model_dump())
    
    session.add(project)
    session.commit()
    session.refresh(project)
    return project


@router.get("/", response_model=list[ProjectRead], tags=["Projects"])
def get_all_projects(session:SessionDep):
    
    projects = session.execute(select(Project).where(Project.is_active == True)).scalars().all()
    return projects
    

@router.get("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def get_project(project_id:int, session:SessionDep):
    
    project = session.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
    return project


@router.put("/{project_id}", response_model=ProjectRead, tags=["Projects"])
def update_project(project_id:int, updated_project: ProjectUpdate, session:SessionDep):
    
    project = session.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
        
    for attrs, value in updated_project.model_dump(exclude_unset=True).items():
        setattr(project, attrs, value)
    session.commit()
    session.refresh(project)
    
    return project


@router.delete("/{project_id}", tags=["Projects"])
def delete_project(project_id: int, session: SessionDep):
    
    project = session.execute(select(Project).where(Project.id == project_id)).scalar_one_or_none()
    if project is None or project.is_active:
        raise HTTPException(
            status_code=404,
            detail="Project not found!"
        )
        
    project.is_active = False
    session.commit()
    session.refresh(project)

    return {
        "status": True,
        "message": f"'{project.name}' deleted!"

    }
    
    
    