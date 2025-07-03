from fastapi import APIRouter
from app.services.monsters_service import MonstersService
from app.db.mongo import db

service = MonstersService(db)

router = APIRouter()

@router.get("/")
async def get_monsters():
    return await service.get_monsters()