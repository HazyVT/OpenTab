
class Folder:
    def __init__(self, id: int, name: str, parent: int):
        self.id = id
        self.name = name
        self.type = "folder"
        self.children = {}
        self.parent = parent
    
    def add_to_children(self, item):
        self.children[item.id] = item
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "parent": self.parent,
            "children": [x.to_dict() for x in self.children.values()]
        }