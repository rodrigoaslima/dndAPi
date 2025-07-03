from fastapi import APIRouter
from app.services.traits_service import TraitsService
from app.db.mongo import db

service = TraitsService(db)

router = APIRouter()

@router.get("/")
async def get_traits():
    return await service.get_traits()