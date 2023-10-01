from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from backend import restapi
import backend.settings as settings
from contextlib import asynccontextmanager
import logging
from fastapi import status


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


@app.get('/')
async def index():
    html_path = settings.load_settings().html_path
    if html_path is not None:
        return FileResponse(html_path)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="This page does not exist.")
