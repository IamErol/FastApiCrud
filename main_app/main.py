from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import database
from main_app.routers.user import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan, swagger_ui_parameters={"operationsSorter": "method"})


app.include_router(user_router)
