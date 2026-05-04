"""WebSocket manager for real-time updates."""
from fastapi import WebSocket
from typing import Dict, Set
from loguru import logger


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
        self.round_subscribers: Set[int] = set()

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected")

    def disconnect(self, user_id: int):
        self.active_connections.pop(user_id, None)

    async def disconnect_all(self):
        for ws in self.active_connections.values():
            await ws.close()
        self.active_connections.clear()

    async def send_personal(self, user_id: int, message: dict):
        ws = self.active_connections.get(user_id)
        if ws:
            await ws.send_json(message)

    async def broadcast(self, message: dict):
        for ws in self.active_connections.values():
            try:
                await ws.send_json(message)
            except Exception:
                pass


ws_manager = ConnectionManager()
