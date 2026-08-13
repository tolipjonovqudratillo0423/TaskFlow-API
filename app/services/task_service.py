from app.services import TaskAccessDeniedError, TaskNotFoundError
from app.repositories import TaskRepository, ProjectRepository
from app.models import Task



class TaskService:
    
    def __init__(self, repo: TaskRepository, project_repo: ProjectRepository = None):
        self.repo = repo
        self.project_repo = project_repo
        
    def get_task_by_id(self, task_id: int)-> Task:
        
        task = self.repo.get_task_by_id(task_id=task_id)
        
        if not task:
            raise TaskNotFoundError("Task not found!")
        
        return task
        
    
    def get_all_tasks_by_owner(self, owner_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_owner(owner_id=owner_id)
        
        if not tasks:
            raise TaskNotFoundError("Task not found")
        
        if tasks[0].project.owner_id != owner_id:
            raise TaskAccessDeniedError("Access denied")
                
        return tasks


    def get_all_tasks_by_owner_and_project(self, owner_id: int, project_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_owner_and_project(owner_id=owner_id, project_id=project_id)
        
        if not tasks:
            raise TaskNotFoundError("Task not found")
        
        if tasks[0].project.owner_id != owner_id:
            raise TaskAccessDeniedError("Access denied")
        
        return tasks
    

    def get_all_tasks_by_assignee(self, assignee_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_assignee(assignee_id=assignee_id)
        if not tasks:
            raise TaskNotFoundError("Task not found")
        
        if tasks[0].assignee_id != assignee_id:
            raise TaskAccessDeniedError("Access denied")
        
        return tasks
    
    def get_all_tasks_by_assignee_and_project(self, assignee_id: int, project_id: int)-> list[Task]:
        
        tasks = self.repo.get_all_tasks_by_assignee_and_project(assignee_id=assignee_id, project_id=project_id)
        
        if not tasks:
             raise TaskNotFoundError("Task not found")
         
        if tasks[0].assignee_id != assignee_id:
             raise TaskAccessDeniedError("Access denied")
               
        return tasks
    
    
    def create(self, task_data: dict, owner_id: int)-> Task:
        project = self.project_repo.get_project(project_id=task_data["project_id"], owner_id=owner_id)
        if not project: 
            raise TaskAccessDeniedError(
                "You are not owner of given project!"
            )
            
        task = self.repo.create(task_data=task_data)
        return task
    
    
    def update(self, task_id: int, task_data: dict)-> Task:
        instance = self.repo.get_task_by_id(task_id=task_id)
        
        if not instance:
            raise TaskNotFoundError("Task not found")
        
        if instance.project.owner_id != task_data["owner_id"]:
            raise TaskAccessDeniedError("Access denied")
        
        task = self.repo.update(task=task, task_data=task_data)
        return task
    
    
    def delete(self, task_id: int, owner_id: int)-> Task:
        
        task = self.repo.get_task_by_id(task_id=task_id)
        if not task:
            raise TaskNotFoundError("Task not found")
        
        if task.project.owner_id != owner_id:
            raise TaskAccessDeniedError("Access denied")
        
        task = self.repo.delete(task=task)
        return task
    

