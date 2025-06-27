from fastapi import APIRouter

from app.services.conditions_service import ConditionsService
from app.db.mongo import db

service = ConditionsService(db)

router = APIRouter()

@router.get("/")
async def get_conditions():
    return await service.get_conditions()

