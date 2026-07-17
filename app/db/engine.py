from sqlalchemy import create_engine

from core.config import settings

engine = create_engine(url=settings.database_url, echo=True)

