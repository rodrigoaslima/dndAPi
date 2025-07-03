from fastapi import APIRouter
from app.services.rules_service import RulesService
from app.db.mongo import db

service = RulesService(db)

router = APIRouter()

@router.get("/")
async def get_rules():
    return await service.get_rules()