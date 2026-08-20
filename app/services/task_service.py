from app.services import TaskAccessDeniedError, TaskNotFoundError, TaskIsEmpty
from app.repositories import TaskRepository, ProjectRepository
from app.models import Task, TaskStatus
from app.db import SessionDep



class TaskService:
    
    def __init__(self, repo: TaskRepository, session: SessionDep = None):
        self.repo = repo
        self.project_repo = ProjectRepository(session=session)
        
        
    def get_task_by_id(self, task_id: int, current_user_id)-> Task:
        
        task = self.repo.get_task_by_id(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError("Task not found!")
        
        if task.project.owner_id == current_user_id or task.assignee_id == current_user_id:
            return task
        raise TaskAccessDeniedError("Access denied")
  
    
    def get_all_tasks_by_owner(self, owner_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_owner(owner_id=owner_id)
        
        if not tasks: 
            raise TaskIsEmpty("User have no tasks!")
        return tasks


    def get_all_tasks_by_owner_and_project(self, owner_id: int, project_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_owner_and_project(owner_id=owner_id, project_id=project_id)
        project = self.project_repo.get_project(project_id, owner_id)
        
        if not project:
            raise TaskAccessDeniedError("You don't have permission to this project!")
        if not tasks:
            raise TaskNotFoundError("Task not found")
        
        return tasks
    

    def get_all_tasks_by_assignee(self, assignee_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_assignee(assignee_id=assignee_id)
        if not tasks:
            raise TaskNotFoundError("Task not found")
        
        return tasks
    
    
    def get_all_tasks_by_assignee_and_project(self, assignee_id: int, project_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_assignee_and_project(assignee_id=assignee_id, project_id=project_id)
        if not tasks:
            raise TaskIsEmpty("Task not found")        
       
        return tasks
    
    
    def create(self, task_data: dict, owner_id: int, tag_ids: list)-> Task:
        project = self.project_repo.get_project(project_id=task_data["project_id"], owner_id=owner_id)
        if not project: 
            raise TaskAccessDeniedError(
                "You are not owner of given project!"
            )
        task_data["status"] = TaskStatus.TODO  
        task = self.repo.create(task_data=task_data, tag_ids=tag_ids)
        return task
    
    
    def update(self, task_id: int, updated_task: dict, current_user_id: int)-> Task:
        instance = self.repo.get_task_by_id(task_id=task_id)
        
        if not instance:
            raise TaskNotFoundError("Task not found")
        
        if instance.project.owner_id == current_user_id or instance.assignee_id == current_user_id:
            task = self.repo.update(task=instance, updated_task=updated_task)
            return task
        
        raise TaskAccessDeniedError("Access denied")
        
        
    def delete(self, task_id: int, current_user_id: int)-> Task:
        
        task = self.repo.get_task_by_id(task_id=task_id)
        if not task:
            raise TaskNotFoundError("Task not found")
        
        
        if task.project.owner_id == current_user_id or task.assignee_id == current_user_id:
            task = self.repo.delete(task=task)
            return task
        
        raise TaskAccessDeniedError("Access denied")    
    
    

