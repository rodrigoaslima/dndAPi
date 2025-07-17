import datetime
from typing import Dict, List

class Character:
    def __init__(
            self,
            name: str,
            level: int,
            race:str,
            char_class:str,
            ability_scores: Dict[str, int],
            skills: List[str],
            weapons: List[str],
            spells: List[str],
            feats: List[str] = [],
            items: List[str] = [],
            hp: int = 0,
            ac: int = 10,
            speed: int = 30
   ):
        self.name = name
        self.level = level
        self.race = race
        self.char_class = char_class
        self.ability_scores = ability_scores
        self.skills = skills
        self.weapons = weapons
        self.spells = spells
        self.feats = feats
        self.items = items
        self.hp = hp
        self.ac = ac
        self.speed = speed
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        def to_dict(self):
            return {
                'name': self.name,
                'level': self.level,
                'race': self.race,
                'char_class': self.char_class,
                'ability_scores': self.ability_scores,
                'skills': self.skills,
                'weapons': self.weapons,
                'spells': self.spells,
                'feats': self.feats,
                'items': self.items,
                'hp': self.hp,
                'ac': self.ac,
                'speed': self.speed,
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat(),

            }