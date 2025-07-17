from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class CharacterCreateSchema(BaseModel):
    name: str
    level: int
    race: str
    char_class: str = Field(..., alias="class")
    ability_scores: Dict[str, int]
    skills: List[str]
    weapons: List[str]
    spells: List[str]
    feats: List[str] = []
    items: List[str] = []
    hp: int = 0
    acc: int = 10
    speed: int = 30
    custom_notes: Optional[str] = None
