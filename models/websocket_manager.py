from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.connection = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connection = websocket

    async def disconnect(self):
        await self.connection.close()
    