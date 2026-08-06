from sqlalchemy import create_engine

from app.core.config import settings

engine = create_engine(url=settings.database_url, echo=True)

