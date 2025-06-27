from fastapi import APIRouter
from app.services.alignments_service import AlignmentsService
from app.db.mongo import db

service = AlignmentsService(db)

router = APIRouter()


@router.get("/")
async def get_alignments():
    return await service.get_alignments()