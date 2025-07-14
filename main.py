import threading
import sqlite3

from webview.webview import Webview, Size, SizeHint
from server import run_server

db = sqlite3.connect("mydb.sqlite")
cursor = db.cursor()
tabs_create_query = """
CREATE TABLE IF NOT EXISTS Tabs (
    id INTEGER PRIMARY KEY,
    title TEXT,
    url TEXT,
    icon TEXT,
    parent INTEGER
);
"""
folders_create_query = """
CREATE TABLE IF NOT EXISTS Folders (
    id INTEGER PRIMARY KEY,
    name TEXT,
    parent INTEGER
);
"""
cursor.execute(tabs_create_query)
cursor.execute(folders_create_query)
db.commit()

server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
    
window_size = Size(400, 800, SizeHint.NONE)
webview = Webview(size=window_size)
webview.title = "OpenTab"
webview.navigate("http://localhost:60002")
webview.run()
     