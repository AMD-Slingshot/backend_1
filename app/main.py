from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import text, speech, tts, chat, poster

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directories if they don't exist
static_dir = "static"
posters_dir = "static/posters"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
if not os.path.exists(posters_dir):
    os.makedirs(posters_dir)

# Mount static files to serve audio files and posters
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(text.router, prefix="/api/text")
app.include_router(speech.router, prefix="/api/speech")
app.include_router(tts.router, prefix="/api/tts")
app.include_router(chat.router)  # Add chat router at root level
app.include_router(poster.router, prefix="/api/poster")

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}