from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import authentication
from backend.restapi import items


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
