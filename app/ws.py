from typing import Dict
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self) -> None:
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active[client_id] = websocket

    def disconnect(self, client_id: str) -> None:
        self.active.pop(client_id, None)

    async def send_to(self, client_id: str, message: str) -> None:
        ws = self.active.get(client_id)
        if ws:
            await ws.send_text(message)

    async def broadcast(self, message: str) -> None:
        for ws in list(self.active.values()):
            await ws.send_text(message)

manager = ConnectionManager()
