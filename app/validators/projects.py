from pydantic import BaseModel, field_validator

from app.models import ProjectStatus



class ProjectCreate(BaseModel):
    
    name: str 
    status: ProjectStatus
    description: str
    owner_id: int
    
    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name of project must not be empty!")
        return value.strip()
    
    @field_validator("status")
    @classmethod
    def must_be_active_on_creation(cls, value: ProjectStatus) -> ProjectStatus:
        if value != ProjectStatus.ACTIVE:
            raise ValueError("New projects must start as active")
        return value

class ProjectRead(BaseModel):
    
    id: int
    name: str
    description: str
    status: str
    owner_id: int
    
    

    class Config:
        from_attributes =True
    
    