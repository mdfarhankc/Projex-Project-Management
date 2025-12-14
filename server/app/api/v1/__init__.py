from fastapi import APIRouter
from app.api.v1 import auth, tag, workspace

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(workspace.router, prefix="/workspaces")
api_router.include_router(tag.router, prefix="/tags")
