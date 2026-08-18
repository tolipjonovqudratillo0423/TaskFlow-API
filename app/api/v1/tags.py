from fastapi import APIRouter, HTTPException, Depends

from app.api import get_current_user
from app.repositories import TagRepository
from app.db import SessionDep
from app.models import User
from app.validators import TagRead, TagCreate
from app.services import TagService


tag_router = APIRouter(prefix="/tags", tags=["Tags"])


@tag_router.get("/", response_model=list[TagRead], tags=["Tags"])
def get_all_tags(session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TagRepository(session)
    service = TagService(repo)

    tags = service.get_all_tags()
    return tags


@tag_router.post("/", response_model=TagRead, tags=["Tags"], status_code=201)
def create_tag(tag: TagCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    repo = TagRepository(session)
    service = TagService(repo)

    try:
        tag = service.create(tag_data=tag.model_dump())
        return tag
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))