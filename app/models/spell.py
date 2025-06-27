class Spell:
    def __init__(self, index: str, name:str, level:int, url:str):
        self.index = index
        self.name = name
        self.level = level
        self.url = url

    def is_high_level(self) -> bool:
        return self.level >= 5

    def to_dict(self) -> dict:
        return {"index": self.index, "name": self.name, "level": self.level, "url": self.url}

    @classmethod
    def from_dict(cls, data: dict) -> "Spell":
        return cls(
            index=data.get("index"),
            name=data.get("name"),
            level=data.get("level",0),
            url=data.get("url"),
        )