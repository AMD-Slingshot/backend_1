from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import text, speech, tts, chat, poster

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-a69j.vercel.app/", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static directories exist
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), "static")
POSTERS_DIR = os.path.join(STATIC_DIR, "posters")

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(POSTERS_DIR, exist_ok=True)

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Include routers
app.include_router(text.router, prefix="/api/text")
app.include_router(speech.router, prefix="/api/speech")
app.include_router(tts.router, prefix="/api/tts")
app.include_router(chat.router)
app.include_router(poster.router, prefix="/api/poster")

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# 👇 IMPORTANT FOR RENDER
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)