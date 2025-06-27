from fastapi import APIRouter
from app.services.features_service import FeaturesService
from app.db.mongo import db

service = FeaturesService(db)

router = APIRouter()

@router.get("/")
async def get_features():
    return await service.get_features()