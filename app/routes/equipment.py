from fastapi import APIRouter

from app.services.equipament_service import EquipmentService
from app.db.mongo import db

service = EquipmentService(db)

router = APIRouter()

@router.get("/")
async def get_equipments():
    return await service.get_equipment()
