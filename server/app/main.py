from fastapi import FastAPI

from app.core.config import settings
from app.exceptions.handler import register_exception_handlers
from app.api.v1 import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)
register_exception_handlers(app=app)


@app.get("/", status_code=200, summary="Welcome from Projex!")
def index():
    return {"message": "Welcome from projex!"}


app.include_router(api_router, prefix=settings.API_V1_STR)
