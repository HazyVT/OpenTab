import json
import sqlite3

from models.folder import Folder
from models.tab import Tab

class DataManager:
    def __init__(self):
        pass

    def get_full_data_to_json(request):
        elements = {}
    
        # Recursively find children of folder
        # Loop through all the folders
        def get_folder_data(folder: Folder):
            cursor.execute("SELECT * FROM Folders WHERE parent = {}".format(folder.id))
            inner_folders = cursor.fetchall()

            for folder in inner_folders:
                item = Folder(folder[0], folder[1], folder[2])
                elements[item.id] = item
                get_folder_data(item)
            
            cursor.execute("SELECT * FROM Tabs WHERE parent = {}".format(folder.id))
            inner_tabs = cursor.fetchall()

            for tab in inner_tabs:
                item = Tab(tab[0], tab[1], tab[2], tab[3], tab[4])
                folder.add_to_children(item)


        conn = sqlite3.connect("mydb.sqlite")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Folders WHERE parent = -1")
        root_folders = cursor.fetchall()

        cursor.execute("SELECT * FROM Tabs WHERE parent = -1")
        root_tabs = cursor.fetchall()

        for folder in root_folders:
            item = Folder(folder[0], folder[1], folder[2])
            elements[item.id] = item
            get_folder_data(item)
        
        for tab in root_tabs:
            item = Tab(tab[0], tab[1], tab[2], tab[3], tab[4])
            elements[item.id] = item

        
        page_data = [v.to_dict() for v in elements.values()]
        return page_data