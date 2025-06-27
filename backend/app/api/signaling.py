from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import json

router = APIRouter()

rooms = {}  # { session_id: { user_id: websocket } }
lock = asyncio.Lock()

async def ping_loop(websocket: WebSocket):
    while True:
        try:
            await websocket.send_text(json.dumps({"type": "ping"}))
            await asyncio.sleep(20)
        except Exception:
            break

@router.websocket("/ws/signaling/{session_id}/{user_id}")
async def signaling(websocket: WebSocket, session_id: str, user_id: str):
    await websocket.accept()
    print(f"User {user_id} connected to session {session_id}")

    async with lock:
        if session_id not in rooms:
            rooms[session_id] = {}
        rooms[session_id][user_id] = websocket

    ping_task = asyncio.create_task(ping_loop(websocket))

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received from {user_id}: {message}")

            try:
                data = json.loads(message)
                if data.get("type") == "pong":
                    # ignorer les pongs
                    continue
            except json.JSONDecodeError:
                print("⚠️ Message non JSON ignoré")

            async with lock:
                recipients = [ws for uid, ws in rooms.get(session_id, {}).items() if uid != user_id]
            for ws in recipients:
                try:
                    await ws.send_text(message)
                except Exception as e:
                    print(f"Error sending to recipient: {e}")

    except WebSocketDisconnect:
        print(f"User {user_id} disconnected from session {session_id}")
    except Exception as e:
        print(f"Error for user {user_id}: {e}")
    finally:
        ping_task.cancel()
        async with lock:
            if session_id in rooms and user_id in rooms[session_id]:
                del rooms[session_id][user_id]
                if not rooms[session_id]:
                    del rooms[session_id]
        print(f"Cleaned up user {user_id} from session {session_id}")
