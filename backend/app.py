from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend import restapi
import backend.settings as settings
from contextlib import asynccontextmanager
import logging



@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize()
    yield
    shutdown()


def initialize() -> None:
    logging.basicConfig(
        level=logging.INFO,
        force=True,
    )


def shutdown() -> None:
    pass



app = FastAPI(lifespan=lifespan)

# CORS

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(restapi.router)
