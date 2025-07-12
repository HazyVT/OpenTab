"""
import json
import os
import traceback
import sqlite3

from models.folder import Folder
from models.tab import Tab

from werkzeug.routing import Rule
from geventwebsocket.websocket import WebSocket

app = Flask(__name__, static_url_path="/static")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
sockets = Sockets()

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.get("/extension")
@cross_origin()
def get_extension():
    return "Hello from OpenTab"

@app.route("/new-tab", methods=["POST"])
@cross_origin()
def new_tab():
    if "id" in request.json:
        # Make connection to sqlite database
        conn = sqlite3.connect("mydb.sqlite")
        cursor = conn.cursor()
        
        new_tab_id = request.json["id"]
        new_tab_title = request.json["title"]
        new_tab_obj = Tab(new_tab_id, new_tab_title, "")

        #INSERT INTO Tabs (id, title, url, icon, parent) VALUES ({}, "{}", "{}", "{}", {})

        #format(new_tab_obj.id, new_tab_obj.name, new_tab_obj.link, new_tab_obj.icon, -1)
    else:
        print("Error: No id in body of new tab request.")

    return ""

@sockets.route("/ws/data", websocket=True)
def handle_connect(ws: WebSocket):
    print("Client Connected")

sockets.url_map.add(Rule('/ws', endpoint=handle_connect, websocket=True))

@app.get('/get-data')
def get_data():
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
                    
    return render_template("data.html", children=page_data)

def run_server():
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('0.0.0.0', 60002), app, handler_class=WebSocketHandler)
    server.start()
"""

from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models.websocket_manager import WebSocketManager
import uvicorn

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

websocket_manager = WebSocketManager()

@app.route("/")
def homepage(request: Request):

    return templates.TemplateResponse("homepage.html", {"request": request})

@app.websocket("/ws")
async def handle_websocket(websocket: WebSocket):
    print("Client Connected")
    await websocket_manager.connect(websocket)
    

def run_server():

    
    uvicorn.run(app, host="0.0.0.0", port=60002)