import json

from models.folder import Folder
from models.tab import Tab

class DataManager:
    def __init__(self):
        pass

    def get_full_data_to_json(request):
        elements = {}
    
        # Recursively find children of folder
        def get_folder_data(element, parent):
            item = Folder(element["id"], element["name"])
            internal_data = [v for v in data["tree"] if v["parent"] == item.id]
            for internal in internal_data:
                if internal["type"] == "Folder":
                    get_folder_data(internal, item.children)
                else:
                    tab = Tab(internal["id"], internal["name"], "")
                    item.add_to_children(tab)
                
            parent[item.id] = item
        
        with open("data.json", "r") as file:
            data = json.load(file)
            root_data = [v for v in data["tree"] if v["parent"] == "."]
            for item in root_data:
                get_folder_data(item, elements)
        
        page_data = [v.to_dict() for v in elements.values()]
        return page_data