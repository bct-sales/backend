from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import authentication
from backend.restapi import items
from backend.restapi import users
from backend.settings import load_settings
import logging
import sys
import os


settings = load_settings()

if settings.database_path is None:
    logging.error("Use BCT_DATABASE_PATH to specify which database to use")
    sys.exit(-1)


if not os.path.isfile(settings.database_path):
    logging.error("Database does not exist")
    sys.exit(-2)


app = FastAPI()

# CORS

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(items.router)
app.include_router(users.router)
