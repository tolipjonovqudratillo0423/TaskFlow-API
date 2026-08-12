import enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    ForeignKey,
    Table,
    Column,
    String,
    Enum
)

from app.db.base import BaseModel
if TYPE_CHECKING:
    from models.users import User


class ProjectStatus(str, enum.Enum):

    ACTIVE = "active"
    ARCHIVED = "archived"

class TaskStatus(str, enum.Enum):

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Project(BaseModel):

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(
        String(100)
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    description: Mapped[str] = mapped_column(
        String(500)
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, values_callable=lambda x:[e.value for e in x]),
        index=True
    )

    owner: Mapped["User"] = relationship(
        back_populates="projects"
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project"
    )


task_tags = Table(
    "task_tags",
    BaseModel.metadata,
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Task(BaseModel):

    __tablename__ = "tasks"

    name: Mapped[str] = mapped_column(
        String(100)
    )
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        index=True
    )
    assignee_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, values_callable=lambda x:[e.value for e in x]),
        index=True
    )

    project: Mapped["Project"] = relationship(
        back_populates="tasks"
    )
    
    tags: Mapped[list["Tag"]] = relationship(
        secondary=task_tags,
        back_populates="tasks"
    )
    assignee: Mapped["User"] = relationship(
        back_populates="tasks"
    )
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="task"
    )


class Tag(BaseModel):

    __tablename__ = "tags"

    name: Mapped[str] = mapped_column(
        String(100)
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="tags",
        secondary=task_tags
    )



class Comment(BaseModel):

    __tablename__ = "comments"

    comment: Mapped[str] = mapped_column(
        String(500)
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        index=True
    )

    task: Mapped["Task"] = relationship(
        back_populates="comments"
    )
    author: Mapped["User"] = relationship(
        back_populates="comments"
    )