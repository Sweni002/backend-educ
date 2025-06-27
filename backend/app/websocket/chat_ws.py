from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.comment import Comment
import json
from datetime import datetime
from app.models.user import User  # importe ton modèle User

router = APIRouter()

# Gestionnaire de connexions par session
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: int):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: int):
        if session_id in self.active_connections:
            self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def broadcast(self, session_id: int, message: str):
        connections = self.active_connections.get(session_id, [])
        for connection in connections:
            await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat/{session_id}/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    db: Session = Depends(get_db),
):
    await manager.connect(websocket, session_id)

    try:
        while True:
            data = await websocket.receive_text()

            if data == "__fichier_ajoute__":
                await manager.broadcast(session_id, data)
                continue

            comment = Comment(
                session_id=session_id,
                user_id=user_id,
                message=data
            )
            db.add(comment)
            db.commit()
            db.refresh(comment)

            user = db.query(User).filter(User.id == user_id).first()

            message_data = {
                "comment_id": comment.id,
                "session_id": session_id,
                "user_id": user_id,
                "user_name": user.name if user else "Anonyme",
                "message": comment.message,
                "created_at": comment.created_at.isoformat()
            }

            await manager.broadcast(session_id, json.dumps(message_data))

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)