from gtts import gTTS
import uuid
import os
from fastapi import HTTPException

def text_to_speech(text: str):
    try:
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        filename = f"audio_{uuid.uuid4()}.mp3"
        filepath = f"static/{filename}"

        os.makedirs("static", exist_ok=True)

        tts = gTTS(text=text, lang="en")
        tts.save(filepath)

        return filepath
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text-to-speech error: {str(e)}"
        )