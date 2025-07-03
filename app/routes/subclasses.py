from fastapi import APIRouter
from app.services.subclasses_service import SubclassesService
from app.db.mongo import db

service = SubclassesService(db)

router = APIRouter()

@router.get("/")
async def get_subclasses():
    return await service.get_subclasses()