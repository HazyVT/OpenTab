import json
import sqlite3
import uvicorn

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from models.server_models import NewTab, UpdatedTab

from models.websocket_manager import WebSocketManager
from models.data_manager import DataManager

templates = Jinja2Templates(directory="templates")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


websocket_manager = WebSocketManager()
data_manager = DataManager()


@app.route("/")
def homepage(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

@app.get("/extension")
def connect_to_extension():
    return "Hello from OpenTab"

@app.post("/new-tab")
async def new_tab(tab: NewTab):
    # Add new tab to sqlite database
    conn = sqlite3.connect("mydb.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Tabs VALUES ({}, '{}', '{}', '{}', {})"
        .format(tab.id, tab.title, "", "/static/blank.ico", -1)
    )
    conn.commit()
    # Rerun page data function to get updated page data from database as json
    # Send that to the websocket
    rendered_template = templates.TemplateResponse(request={"request": websocket_manager.htmx_connection}, name="list.html", context={"children": data_manager.get_full_data_to_json()}).body.decode()
    await websocket_manager.htmx_connection.send_text(rendered_template)

@app.post("/update-tab")
async def update_tab(tab: UpdatedTab):
    conn = sqlite3.connect("mydb.sqlite")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Tabs SET title = '{}', url = '{}', icon = '{}' WHERE id = {}".format(tab.title, tab.url, tab.icon, tab.id)
    )
    conn.commit()
    rendered_template = templates.TemplateResponse(request={"request": websocket_manager.htmx_connection}, name="list.html", context={"children": data_manager.get_full_data_to_json()}).body.decode()
    await websocket_manager.htmx_connection.send_text(rendered_template)


@app.get('/get-data', response_class=HTMLResponse)
def get_data(request: Request):
    page_data = data_manager.get_full_data_to_json()
    return templates.TemplateResponse(request=request, name="data.html", context={"children": page_data})

@app.websocket("/ws-ext")
async def handle_extension_websocket(websocket: WebSocket):
    await websocket_manager.extension_connection(websocket)
    print("Extension Connected")
    
    try:
        while True:
            data = await websocket_manager.extension_connection.receive_json()
            print(data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect_extension()
        print("Extension Disconnected")

@app.websocket("/ws")
async def handle_websocket(websocket: WebSocket):
    await websocket_manager.connect_htmx(websocket)
    print("Client Connected")
    rendered_template = templates.TemplateResponse(request={"request": websocket_manager.htmx_connection}, name="list.html", context={"children": data_manager.get_full_data_to_json()}).body.decode()
    await websocket_manager.htmx_connection.send_text(rendered_template)

    try:
        while True:
            data = await websocket_manager.htmx_connection.receive_text()
            print(data)
    except WebSocketDisconnect:
        await websocket_manager.disconnect_htmx()
        print("Client Disconnected")

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=60002)