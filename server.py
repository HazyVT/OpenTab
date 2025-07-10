import json
import os
import traceback

from models.folder import Folder
from models.tab import Tab

from flask import Flask, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path="/static")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.get("/extension")
@cross_origin()
def get_extension():
    return "Hello from OpenTab"

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
    app.run("0.0.0.0", 60002)

    