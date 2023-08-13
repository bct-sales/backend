from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import authentication
from backend.restapi import events


app = FastAPI()

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

root_router = APIRouter(prefix="/api/v1")

root_router.include_router(authentication.router)
root_router.include_router(events.router)

app.include_router(root_router)
