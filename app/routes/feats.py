from fastapi import APIRouter
from app.services.feats_service import FeatsService
from app.db.mongo import db

service = FeatsService(db)

router = APIRouter()

@router.get("/")
async def get_feats():
    return await service.get_feats()