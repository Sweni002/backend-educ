from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import asyncio

router = APIRouter()

class LiveManager:
    def __init__(self):
        # Clé = session_id, valeur = liste de WebSockets connectés
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, session_id: int, websocket: WebSocket):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)
        print(f"Client connecté à la session {session_id}, total: {len(self.active_connections[session_id])}")

    def disconnect(self, session_id: int, websocket: WebSocket):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            print(f"Client déconnecté de la session {session_id}, restant: {len(self.active_connections[session_id])}")
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: int, message: dict):
        if session_id in self.active_connections:
            living_connections = []
            for connection in self.active_connections[session_id]:
                try:
                    await connection.send_json(message)
                    living_connections.append(connection)
                except Exception as e:
                    print(f"Erreur en envoyant WS: {e}")
            self.active_connections[session_id] = living_connections

live_manager = LiveManager()

@router.websocket("/ws/live/{session_id}")
async def websocket_live_status(websocket: WebSocket, session_id: int):
    await live_manager.connect(session_id, websocket)
    try:
        while True:
            # Attend un message (par exemple un ping ou rien)
            data = await websocket.receive_text()
            # Tu peux gérer ici si besoin un message de la part client
            # Sinon ignore ou répond à un ping
    except WebSocketDisconnect:
        live_manager.disconnect(session_id, websocket)
