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

@app.get('/get-root-data')
def get_data():
    with open("data.json", "r") as file:
        data = json.load(file)
        root_data = [v for v in data["tree"] if v["parent"] == "."]
        template = env.get_template("data.html")
        file.close()
        return template.render({"tree": root_data})
    
@app.get('/get-elements')
def get_elements():
    id_param = request.args.get("id")
    with open("data.json", "r") as file:
        data = json.load(file)
        element_data = [v for v in data["tree"] if v["parent"] == int(id_param)]
        template = env.get_template("data.html")
        file.close()
        return template.render({"tree": element_data})

def run_server():
    app.run("0.0.0.0", 60002)

    