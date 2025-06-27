from fastapi import APIRouter
from app.services.backgrounds_service import BackgroundService
from app.db.mongo import db

service = BackgroundService(db)

router = APIRouter()

@router.get("/")
async def get_alignments():
    return await service.get_backgrounds()