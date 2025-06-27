from fastapi import APIRouter

from app.services.damageTypes_service import DamageTypesService
from app.db.mongo import db

service = DamageTypesService(db)

router = APIRouter()

@router.get("/")
async def get_damage_types():
    return await service.get_damage_types()
