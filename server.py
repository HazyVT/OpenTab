import threading

from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello World!"

def run_server():
    app.run("0.0.0.0", 60002)

    