from fastapi import APIRouter
from app.services.ruleSections_service import RuleSectionsService
from app.db.mongo import db

service = RuleSectionsService(db)

router = APIRouter()

@router.get("/")
async def get_rule_sections():
    return await service.get_rule_sections()