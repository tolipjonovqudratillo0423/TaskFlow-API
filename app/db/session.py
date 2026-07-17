from typing import Annotated
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

from db.engine import engine


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=True,
)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        

SessionDep = Annotated[Session,Depends(get_db)]