import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.core.config import settings
from src.core.database import Base, engine
from src.tasks.router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("task_manager.db"):
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(task_router)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Task Manager API!", "status": "online"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("src/static/favicon.png")
