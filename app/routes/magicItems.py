from fastapi import APIRouter
from app.services.magicItems_service import MagicItemsService
from app.db.mongo import db

service = MagicItemsService(db)

router = APIRouter()

@router.get("/")
async def get_magic_items():
    return await service.get_magic_items()