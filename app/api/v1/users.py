from fastapi import APIRouter, HTTPException, Depends

from app.db import SessionDep
from app.validators import UserRead
from app.models import User
from app.api import get_current_user


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/about-me", response_model=UserRead, tags=["Users"])
def about_me(current_user: User = Depends(get_current_user)):
    
    return current_user