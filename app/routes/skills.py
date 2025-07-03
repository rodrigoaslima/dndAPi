from fastapi import APIRouter
from app.services.skills_service import SkillsService
from app.db.mongo import db

service = SkillsService(db)

router = APIRouter()

@router.get("/")
async def get_skills():
    return await service.get_skills()