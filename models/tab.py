class Tab:
    def __init__(self, id: int, name: str, link: str):
        self.id = id
        self.name = name
        self.link = link
        self.icon = ""
        self.type = "tab"
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "icon": self.icon,
            "link": self.link
        }
        
    