from fastapi import APIRouter

from app.services.equipmentTypes_service import EquipmentTypesService
from app.db.mongo import db

service = EquipmentTypesService(db)

router = APIRouter()

@router.get("/")
async def get_equipments_types():
    return await service.get_equipment_types()
