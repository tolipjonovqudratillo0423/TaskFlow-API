from app.repositories import TagRepository
from app.models import Tag

class TagService:
    def __init__(self, repo: TagRepository):
        self.repo = repo

    def get_all_tags(self)-> list[Tag]:
        return self.repo.get_all_tags()
    
    
    def get_all_tags_by_task_id(self, task_id: int)-> Tag:
        return self.repo.get_all_tags_by_task_id(task_id=task_id)
    
    
    def get_tag(self, tag_id: int)-> Tag:
        return self.repo.get_tag(tag_id=tag_id)
    
    
    def create(self, tag_data: dict)-> Tag:
        return self.repo.create(tag_data=tag_data)
    
    
    def update(self, tag_id: int, updated_tag: dict)-> Tag:
        tag = self.get_tag(tag_id=tag_id)
        return self.repo.update(tag=tag, updated_tag=updated_tag)