class Tab:
    def __init__(self, id: int, name: str, link: str):
        self.id = id
        self.name = name
        self.link = link
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link
        }
        
    