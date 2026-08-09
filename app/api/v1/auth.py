import jwt

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
from fastapi.security import OAuth2PasswordBearer


from app.models import User
from app.validators import UserCreate, UserRead, Login
from app.db import SessionDep
from app.core import (
    set_password, check_password, 
    create_access_token,create_refresh_token
)

from app.core import settings



auth_router = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_router.post("/register", response_model=UserRead, tags=["AUTH"])
def register(new_user: UserCreate, session: SessionDep):
    
    user_data = new_user.model_dump()
    
    plain_password = user_data.pop("password")
    user = User(**user_data)
    user.password_hash = set_password(plain_password=plain_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


@auth_router.post("/login", tags=["AUTH"])
def login(credentials: Login, session: SessionDep):
    
    user = session.execute(select(User).where(User.email == credentials.email)).scalar_one_or_none()
    if user is None or not check_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials!"
        )
    
    access = create_access_token(user_id=user.id)
    refresh = create_refresh_token(user_id=user.id)
    return {
        "access": access,
        "refresh": refresh,
    }
    
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_schema), session: SessionDep = None) -> User:
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        user_id = payload.get("sub")
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=401,
            detail="Couldn't validate credentials"
        )
    
    user = session.execute(select(User).where(User.id == int(user_id))).scalar_one_or_none()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return user
