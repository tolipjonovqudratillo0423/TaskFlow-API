import uvicorn

from fastapi import FastAPI

from app.api import project_router, auth_router, user_router


app = FastAPI()

app.include_router(project_router)
app.include_router(auth_router)
app.include_router(user_router)

if __name__=="__main__":
    uvicorn.run("app.main:app", reload=True)

