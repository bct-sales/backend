from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from backend.restapi import authentication
from backend.restapi import events


router = APIRouter(prefix="/api/v1")

router.include_router(authentication.router)
router.include_router(events.router)
