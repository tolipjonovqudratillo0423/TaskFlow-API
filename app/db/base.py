from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)
from sqlalchemy import (
    func,
    DateTime,
)

class Base(DeclarativeBase):
    pass

class BaseModel(Base):
    
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    
    is_active: Mapped[bool] = mapped_column(
        default=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

