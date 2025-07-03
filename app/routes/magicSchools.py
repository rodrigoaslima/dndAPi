from fastapi import APIRouter
from app.services.magicSchools_service import MagicSchoolsService
from app.db.mongo import db

service = MagicSchoolsService(db)

router = APIRouter()

@router.get("/")
async def get_magic_schools():
    return await service.get_magic_schools()