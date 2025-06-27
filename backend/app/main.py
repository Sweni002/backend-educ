from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.websocket.chat_ws import router as chat_ws_router
# Importer tous les modèles explicitement
from app.models.user import User
from app.models.session import Session
from app.models.participant import Participant
from app.models.comment import Comment
from app.models.file import File
from app.models.speak_request import SpeakRequest
from app.models.transcription import Transcription
from app.models.video import Video
# Importer les routers
from app.api import auth
from app.api import session as session_api
from app.api import comment as comment_api
from app.api import file as file_api
from app.api import speak as speak_api
from app.api import video  , signaling
from fastapi.staticfiles import StaticFiles
from app.websocket.live_socket import router as live_socket_router

# Créer les tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cours en ligne API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(session_api.router, prefix="/sessions", tags=["Sessions"])
app.include_router(comment_api.router, prefix="/comments", tags=["Comments"])
app.include_router(file_api.router, prefix="/files", tags=["Files"])
app.include_router(speak_api.router, prefix="/speak", tags=["Speak Requests"])
app.include_router(video.router)

app.include_router(signaling.router)
app.include_router(chat_ws_router)

app.include_router(live_socket_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    Base.metadata.create_all(bind=engine)
    return {"message": "API Cours en ligne"}