from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import authentication
from backend.restapi import user
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

app.include_router(authentication.router, prefix='/api/v1')
app.include_router(user.router, prefix='/api/v1/me')
app.include_router(events.router, prefix='/api/v1/events')
