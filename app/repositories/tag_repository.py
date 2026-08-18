from sqlalchemy import select

from app.models import Tag
from app.repositories import TaskRepository
from app.db import SessionDep



class TagRepository:
    def __init__(self, session: SessionDep, task_repo: TaskRepository = TaskRepository(SessionDep)):
        self.session = session
        self.task_repo = task_repo
        
    
    def get_all_tags(self):
        return self.session.execute(
            select(Tag)
        ).scalars().all()
    
    
    def get_all_tags_by_task_id(self, task_id: int):
        task = self.task_repo.get_task_by_id(task_id=task_id)
        tags = task.tags
        return tags
    
    
    def get_tag(self, tag_id: int):
        return self.session.execute(
            select(Tag)
            .where(Tag.id == tag_id)
        ).scalar_one_or_none()
        
    
    def create(self, tag_data: dict):
        tag = Tag(**tag_data)
        self.session.add(tag)
        self.session.commit()
        self.session.refresh(tag)
        return tag
    
    
    def update(self, tag: Tag, updated_tag: dict):
        for attr, value in updated_tag.items():
            setattr(tag, attr, value)
        
        self.session.commit()
        self.session.refresh(tag)
        return tag
    
    