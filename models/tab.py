class Tab:
    def __init__(self, id: int, name: str, link: str, icon: str, parent: int, active: bool):
        self.id = id
        self.name = name
        self.link = link
        self.icon = icon
        self.parent = parent
        self.type = "tab"
        self.is_active = active
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "icon": self.icon,
            "link": self.link,
            "parent": self.parent,
            "active": self.is_active
        }
        
    