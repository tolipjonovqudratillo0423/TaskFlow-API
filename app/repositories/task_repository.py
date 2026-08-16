from sqlalchemy import select

from app.models import Task, Project
from app.db import SessionDep


class TaskRepository:
    
    def __init__(self, session: SessionDep):
        self.session = session
        
    
    def get_task_by_id(self, task_id: int)-> Task:
        
        task = self.session.execute(
            select(Task)
            .where(
                Task.id == task_id
            )
        ).scalar_one_or_none() 
        return task   
    
    def get_all_task(self)-> list[Task]:
        
        tasks = self.session.execute(
            select(Task)
        ).scalars().all()
        
        return tasks
    
    
    def get_all_tasks_by_owner(self, owner_id: int)-> list[Task]:
        
        tasks = self.session.execute(
            select(Task)
            .join(Task.project)
            .where(Project.owner_id == owner_id)
        ).scalars().all()
        return tasks
        
        
    def get_all_tasks_by_owner_and_project(self, owner_id: int, project_id: int)-> list[Task]:
        
        tasks = self.session.execute(
            select(Task)
            .join(Task.project)
            .where(Task.project_id == project_id)
            .where(Project.owner_id == owner_id)
        ).scalars().all()
        return tasks


    def get_all_tasks_by_assignee(self, assignee_id: int)-> list[Task]:
        
        tasks = self.session.execute(
            select(Task)
            .where(Task.assignee_id == assignee_id)
        ).scalars().all()
        return tasks
    
    
    def get_all_tasks_by_assignee_and_project(self, assignee_id: int, project_id: int)-> list[Task]:
        
        tasks = self.session.execute(
            select(Task)
            .where(
                Task.project_id == project_id,
                Task.assignee_id == assignee_id
            )
        ).scalars().all()
        return tasks
        
    def create(self, task_data: dict)-> Task:
         
        task = Task(**task_data)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    
    def update(self, task: Task, updated_task: dict)-> Task:
              
        for attr, value in updated_task.items():
            setattr(task, attr, value)
    
        self.session.commit()
        self.session.refresh(task)
        return task


    def delete(self, task: Task)-> Task:
        
        task.is_active = False
        self.session.commit()
        self.session.refresh(task)
        return task