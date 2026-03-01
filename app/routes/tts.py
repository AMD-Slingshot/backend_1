from fastapi import APIRouter
from pydantic import BaseModel
from app.services.tts_service import text_to_speech

router = APIRouter()  

class TTSRequest(BaseModel):
    text: str

@router.post("/generate")
def generate_tts(request: TTSRequest):
    filepath = text_to_speech(request.text)
    return {"audio_url": filepath}