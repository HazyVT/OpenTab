from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.htmx_connection = None

    async def connect_htmx(self, websocket: WebSocket):
        await websocket.accept()
        self.htmx_connection = websocket

    async def disconnect_htmx(self):
        self.htmx_connection = None
        
    