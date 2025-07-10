class Folder:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.children = {}
    
    def add_to_children(self, item):
        self.children[item.id] = item
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "children": [x.to_dict() for x in self.children.values()]
        }