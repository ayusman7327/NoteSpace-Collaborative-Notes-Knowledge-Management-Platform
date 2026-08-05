from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database import Base, engine
from app.models import (
    Page,
    PageVersion,
    User,
    Workspace,
    WorkspaceMember
)
from app.routers.auth import router as auth_router
from app.routers.pages import router as pages_router
from app.routers.users import router as users_router
from app.routers.workspaces import router as workspace_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Collaborative Notes and Knowledge Management Platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workspace_router)
app.include_router(pages_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to NoteSpace API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }