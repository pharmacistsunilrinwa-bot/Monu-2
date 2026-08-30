from fastapi import WebSocket
from typing import Dict
import asyncio
import json

class TrackingService:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, request_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[request_id] = websocket

    def disconnect(self, request_id: str):
        if request_id in self.active_connections:
            del self.active_connections[request_id]

    async def update_status(self, request_id: str, status: str, error: str = None):
        if request_id in self.active_connections:
            message = {"request_id": request_id, "status": status}
            if error:
                message["error"] = error
            await self.active_connections[request_id].send_json(message)

tracking_service = TrackingService()
