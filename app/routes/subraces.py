from fastapi import APIRouter
from app.services.subraces_service import SubracesService
from app.db.mongo import db

service = SubracesService(db)

router = APIRouter()

@router.get("/")
async def get_subraces():
    return await service.get_subraces()