from sqlalchemy.orm import (
    Mapped,mapped_column
)

from db.base import BaseModel



class User(BaseModel):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str]
    email: Mapped[str]
    password_hash: Mapped[str]
    