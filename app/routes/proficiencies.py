from fastapi import APIRouter
from app.services.proficiencies_service import ProficienciesService
from app.db.mongo import db

service = ProficienciesService(db)

router = APIRouter()

@router.get("/")
async def get_proficiencies():
    return await service.get_proficiencies()