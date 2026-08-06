from typing import TYPE_CHECKING
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    String
)

from app.db.base import BaseModel
if TYPE_CHECKING:
    from models.projects import Project, Task, Comment


class User(BaseModel):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    ) 
    username: Mapped[str] = mapped_column(
        String(100),
        index=True,
        unique=True
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )
    password_hash: Mapped[str]
    phone_number: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )
    first_name: Mapped[str] = mapped_column(
        String(50)
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
        
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner"
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="author"
    )
    




