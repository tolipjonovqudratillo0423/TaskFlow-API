from app.repositories import ProjectRepository
from app.models import Project
from app.services.exceptions import ProjectAccessDeniedError,ProjectNotFoundError


class ProjectService:
    
    def __init__(self, repo: ProjectRepository):
        self.repo = repo
        
    def get_all_projects_by_owner(self, owner_id: int) -> list[Project]:
        projects = self.repo.get_all_projects_by_owner(owner_id=owner_id)
        
        if projects is None:
            raise ProjectNotFoundError
        return projects
    

    def get_project(self, project_id: int, owner_id: int) -> Project:
        
        project = self.repo.get_project(project_id, owner_id)
        if not project:
            raise ProjectNotFoundError
        
        if project.owner_id != owner_id:
            raise ProjectAccessDeniedError
                
        return project
    
        
    def create(self, owner_id: int, project_data: dict) -> Project:
        
        project = self.repo.create(
            project_data=project_data,
            owner_id=owner_id)
        
        return project
        
    
    def update(self, owner_id: int, project_id: int, updated_project: dict) -> Project:
        instance = self.repo.get_project(project_id, owner_id)
        
        if not instance:
            raise ProjectNotFoundError
        
        if instance.owner_id != owner_id:
            raise ProjectAccessDeniedError
        
        project = self.repo.update(instance, updated_project)
        return project
    
    
    def delete(self, owner_id: int, project_id: int)-> dict:
        
        project = self.repo.get_project(project_id,owner_id)
        
        if not project:
            raise ProjectNotFoundError
        
        if project.owner_id != owner_id:
            raise ProjectAccessDeniedError
        project = self.repo.delete(project)
        return project