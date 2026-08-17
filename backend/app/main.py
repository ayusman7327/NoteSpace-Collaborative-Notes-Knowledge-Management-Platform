from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.activity_logs import router as activity_logs_router
from app.routers.ai import router as ai_router
from app.routers.attachments import router as attachments_router
from app.routers.auth import router as auth_router
from app.routers.comments import router as comments_router
from app.routers.pages import router as pages_router
from app.routers.realtime import router as realtime_router
from app.routers.tags import router as tags_router
from app.routers.users import router as users_router
from app.routers.workspace_invitations import router as workspace_invitations_router
from app.routers.workspace_members import router as workspace_members_router
from app.routers.workspaces import router as workspaces_router


app = FastAPI(
    title="NoteSpace API",
    description="Backend API for the NoteSpace collaborative knowledge management platform.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Welcome to NoteSpace API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NoteSpace API",
    }


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(workspace_members_router)
app.include_router(workspace_invitations_router)
app.include_router(pages_router)
app.include_router(tags_router)
app.include_router(comments_router)
app.include_router(attachments_router)
app.include_router(activity_logs_router)
app.include_router(ai_router)
app.include_router(realtime_router)