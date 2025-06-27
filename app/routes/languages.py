from fastapi import APIRouter
from app.services.languages_service import LanguagesService
from app.db.mongo import db

service = LanguagesService(db)

router = APIRouter()

@router.get("/")
async def get_languages():
    return await service.get_languages()