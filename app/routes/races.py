from fastapi import APIRouter
from app.services.races_service import RacesService
from app.db.mongo import db

service = RacesService(db)

router = APIRouter()

@router.get("/")
async def get_races():
    return await service.get_races()