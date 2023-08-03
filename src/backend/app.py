from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import items
from backend.restapi import users


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

app.include_router(items.router)
app.include_router(users.router)
