from app.models.character import Character
#from database import character_collection
from fastapi import HTTPException

def create_character_service(data: dict):
    print(data)
    try:
        character = Character(
            name=data["name"],
            level=data["level"],
            race=data["race"],
            char_class=data["char_class"],
            ability_scores=data["ability_scores"],
            skills=data["skills"],
            weapons=data["weapons"],
            spells=data["spells"],
            feats=data.get("feats", []),
            items=data.get("items", []),
            hp=data.get("hp", 0),
            ac=data.get("ac", 10),
            speed=data.get("speed", 30)
        )
    except HTTPException as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {str(e)}")

    #result = character_collection.insert_one(character.to_dict())
    #if not result.inserted_id:
        #raise HTTPException(status_code=500, detail="Erro ao criar personagem.")

    #return {"id": str(result.inserted_id), "message": "Personagem criado com sucesso"}
