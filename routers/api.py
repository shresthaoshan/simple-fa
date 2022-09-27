from fastapi import APIRouter
from . import auth, videos

router = APIRouter(prefix="/api")

router.include_router(videos.router)
router.include_router(auth.router)

@router.get("/")
def home():
    return {"check": True}
