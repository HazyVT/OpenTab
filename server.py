import json
import os
import traceback

from jinja2 import Environment, FileSystemLoader
from flask import Flask
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
    with open("data.json", "r") as file:
        data = json.load(file)
        template = env.get_template("tab_data.html")
        return template.render(data)
    

def run_server():
    app.run("0.0.0.0", 60002)

    