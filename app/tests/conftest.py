import pytest

from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import BaseModel
from app.db import get_db
from app.models import User
from app.api import get_current_user

SQLALCHEMY_DATABASE_URL = "postgresql://tqm:Alabas23@localhost/tqm_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    BaseModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    
    test_user = User(
        id=1,
        username='test_user',
        email="example@example.com",
        password_hash="fake_hash",
        phone_number="+998000000000",
        first_name="Test",
        last_name="User"
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)
    
    
    def over_ride_get_db():
        yield db_session
        
    def over_ride_get_current_user():
        return test_user
    
    app.dependency_overrides[get_db] = over_ride_get_db
    app.dependency_overrides[get_current_user] = over_ride_get_current_user
    yield TestClient(app)
    app.dependency_overrides.clear()

