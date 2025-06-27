from fastapi import APIRouter
from app.services.classes_service import ClassesService
from app.db.mongo import db

service = ClassesService(db)

router = APIRouter()

@router.get("/")
async def get_class():
    return await service.get_classes()
