from fastapi import APIRouter
from app.services.abilityPoints_service import AbilityPointsService
from app.db.mongo import db

service = AbilityPointsService(db)

router = APIRouter()

@router.get("/")
async def get_ability_points():
    return await service.get_ability_points()