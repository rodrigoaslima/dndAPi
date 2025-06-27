from fastapi import APIRouter
from app.services.spells_service import SpellsService
from app.db.mongo import db

service = SpellsService(db)

router = APIRouter()

@router.get("/")
async def get_spells():
    return await service.get_spells()