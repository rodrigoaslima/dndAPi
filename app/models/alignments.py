class Alignment:
    def __init__(self, index, name, url):
        self.index = index
        self.name = name
        self.url = url

    def to_dict(self):
        return {"index": self.index, "name": self.name, "url": self.url}

    @classmethod
    def from_dict(cls, data: dict) -> "Alignment":
        return cls(
            index = data.get("index"),
            name = data.get("name"),
            url = data.get("url"),
        )
