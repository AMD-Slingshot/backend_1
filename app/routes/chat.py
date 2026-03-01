from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gemini_service import generate_text
from app.services.tts_service import text_to_speech

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    return_audio: bool = True  # Option to return audio

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint that accepts text messages and returns AI responses.
    Also generates audio using gTTS.
    Compatible with frontend Audio.jsx component.
    """
    try:
        # Generate AI response using Gemini
        reply = generate_text(request.message)
        
        # Generate audio if requested
        audio_url = None
        if request.return_audio:
            audio_path = text_to_speech(reply)
            # Convert to URL path
            audio_url = f"http://localhost:8000/{audio_path}"
        
        return {
            "reply": reply,
            "audio_url": audio_url
        }
    except HTTPException:
        # Re-raise HTTPExceptions from gemini_service
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
