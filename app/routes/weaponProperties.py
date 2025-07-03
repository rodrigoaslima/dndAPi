from fastapi import APIRouter
from app.services.weaponProperties_service import WeaponPropertiesService
from app.db.mongo import db

service = WeaponPropertiesService(db)

router = APIRouter()

@router.get("/")
async def get_traits():
    return await service.get_weapon_properties()