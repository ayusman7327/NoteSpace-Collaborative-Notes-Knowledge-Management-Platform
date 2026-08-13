import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.database import Base, engine

from app.routers.activity_logs import router as activity_logs_router
from app.routers.ai import router as ai_router
from app.routers.attachments import router as attachments_router
from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.pages import router as pages_router
from app.routers.tags import router as tags_router
from app.routers.users import router as users_router
from app.routers.workspace_invitations import (
    router as workspace_invitations_router,
)
from app.routers.workspace_members import (
    router as workspace_members_router,
)
from app.routers.workspaces import router as workspaces_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="NoteSpace API",
    version="1.0.0",
    description="Collaborative Notes and Knowledge Management Platform",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs(
    "uploads",
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(pages_router)
app.include_router(tags_router)
app.include_router(activity_logs_router)
app.include_router(ai_router)
app.include_router(comments_router)
app.include_router(workspace_invitations_router)
app.include_router(workspace_members_router)
app.include_router(attachments_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to NoteSpace API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }


@app.get("/debug/database")
def debug_database():
    try:
        with engine.connect() as connection:
            connection.execute(
                text("SELECT 1")
            )

        return {
            "database": "connected",
        }

    except Exception as error:
        return {
            "database": "error",
            "detail": str(error),
        }


@app.get("/debug/config")
def debug_config():
    from app.core.config import settings

    return {
        "database_url_configured": bool(
            settings.database_url
        ),
        "secret_key_configured": bool(
            settings.secret_key
        ),
        "gemini_configured": bool(
            settings.gemini_api_key
        ),
    }