from sqlalchemy import select

from app.models import (
    Project
)
from app.db import SessionDep


class ProjectRepository:
    
    def __init__(self, session: SessionDep):
        self.session = session
    
    
    def get_all_projects(self):
        return self.session.execute(
            select(Project)
        ).scalars().all()
    
    
    
    def get_all_projects_by_owner(self, owner_id: int) -> list[Project]:
        
        return self.session.execute(
            select(Project)
            .where(
                Project.owner_id == owner_id,
                Project.is_active == True
            )
        ).scalars().all()
    
    
    def get_project(self, project_id: int, owner_id: int) -> Project:
        
        return self.session.execute(
            select(Project)
            .where(
                Project.id == project_id,
                Project.owner_id == owner_id,
                Project.is_active == True
            )
        ).scalar_one_or_none()
    
    
    def create(self, project_data: dict, owner_id:int ) -> Project:
        project = Project(**project_data)
        project.owner_id = owner_id
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project


    def update(self, project: Project, project_data: dict)-> Project:
        
        for attr, value in project_data.items():
            setattr(project, attr, value)
        
        self.session.commit()
        self.session.refresh(project)
        return project

    
    def delete(self, project: Project)-> Project:
        project.is_active = False
        self.session.commit()
        self.session.refresh(project)
        return project
        
        
        
        
 
