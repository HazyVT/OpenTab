import threading

from jinja2 import Template, Environment, FileSystemLoader
from flask import Flask

app = Flask(__name__)
env = Environment(loader=FileSystemLoader("./templates"))

@app.route("/")
def homepage():
    template = env.get_template("homepage.html")
    data = {"names": ["John", "Eli", "Michael"]}
    return template.render(data)

def run_server():
    app.run("0.0.0.0", 60002)

    