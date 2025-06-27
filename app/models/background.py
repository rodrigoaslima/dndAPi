class Background:
    def __init__(self, index: str, name:str, url:str):
        self.index = index
        self.name = name
        self.url = url

    def to_dict(self):
        return{"index": self.index, "name": self.name, "url": self.url}

    @classmethod
    def from_dict(cls, data:dict)->"Background":
        return cls(
            index=data.get("index"),
            name=data.get("name"),
            url=data.get("url")
        )