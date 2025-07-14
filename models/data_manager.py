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

            for nested_folder in inner_folders:
                item = Folder(nested_folder[0], nested_folder[1], nested_folder[2])
                folder.add_to_children(item)
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
    
    async def handle_move_data(request, move_id: int, to_id: int):
        print(move_id, to_id)
        conn = sqlite3.connect("mydb.sqlite")
        cursor = conn.cursor()
        
        if move_id is not None:
            # Check if its a folder
            cursor.execute("SELECT * FROM Folders WHERE id = {}".format(move_id))
            item = cursor.fetchone()
            if item is not None:
                cursor.execute("UPDATE Folders SET parent = {} WHERE id = {}".format(to_id, move_id))
                conn.commit()
            else:            
                # Item is tab
                cursor.execute("UPDATE Tabs SET parent = {} WHERE id = {}".format(to_id, move_id))
                conn.commit()
            
