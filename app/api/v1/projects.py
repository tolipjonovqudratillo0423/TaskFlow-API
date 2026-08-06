from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.db.session import SessionDep
from app.models import Project
from app.validators.projects import ProjectRead, ProjectCreate


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(project_in: ProjectCreate, session: SessionDep):
    
    project = Project(**project_in.model_dump())
    
    session.add(project)
    session.commit()
    session.refresh(project)
    return project