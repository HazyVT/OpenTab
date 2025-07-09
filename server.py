import json
import os
import traceback

from jinja2 import Environment, FileSystemLoader
from flask import Flask, request
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path="/static")
env = Environment(loader=FileSystemLoader("./templates"))
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

@app.route("/")
def homepage():
    template = env.get_template("homepage.html")
    data = {"names": ["John", "Eli", "Michael"]}
    return template.render(data)

@app.get("/extension")
@cross_origin()
def get_extension():
    return "Hello from OpenTab"

@app.get("/tab-data")
def get_tab_data():
    id_param = request.args.get("id")

    with open("data.json", "r") as file:
        data = json.load(file)
        if id_param is None:
            root_items = [v for v in data["tree"] if v["parent"] == "."]
            template = env.get_template("tab_data.html")
            return template.render({"tree": root_items})
        else:
            nested_items = [v for v in data["tree"] if v["parent"] == int(id_param)]
            template = env.get_template("tab_data.html")
            return template.render({"tree": nested_items})   
            
def run_server():
    app.run("0.0.0.0", 60002)

    