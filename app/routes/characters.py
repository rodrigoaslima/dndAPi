from fastapi import APIRouter, Request
from app.schemas.character import  CharacterCreateSchema
from app.services.character_service import (
    create_character_service,
    #get_all_characters_service,
    #get_character_by_id_service,
    #update_character_service,
    #delete_character_service
)

router = APIRouter()

@router.post("/characters")
async def create_character(character: CharacterCreateSchema):
    data = character.model_dump(by_alias=True)
    print(data)
    return create_character_service(data)

#@router.get("/characters")
#def get_all_characters():
#    return get_all_characters_service()

#@router.get("/characters/{character_id}")
#def get_character_by_id(character_id: str):
#    return get_character_by_id_service(character_id)

#@router.put("/characters/{character_id}")
#async def update_character(character_id: str, request: Request):
#    data = await request.json()
#    return update_character_service(character_id, data)

#@router.delete("/characters/{character_id}")
#def delete_character(character_id: str):
#    return delete_character_service(character_id)
