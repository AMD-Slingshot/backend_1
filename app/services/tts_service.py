from gtts import gTTS
import uuid
import os
import re
from fastapi import HTTPException

def clean_markdown_for_audio(text: str) -> str:
    """
    Remove markdown formatting to ensure clean text-to-speech output.
    Converts markdown to plain text for natural audio speech.
    """
    # Remove bold/italic markers (**text**, *text*, __text__, _text_)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove headers (# Header)
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove inline code (`code`)
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    # Remove links [text](url) -> text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove list markers (- item, * item, 1. item)
    text = re.sub(r'^[\-\*]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def text_to_speech(text: str):
    try:
        if not text or not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Text cannot be empty"
            )
        
        # Clean markdown formatting before TTS
        clean_text = clean_markdown_for_audio(text)
        
        filename = f"audio_{uuid.uuid4()}.mp3"
        filepath = f"static/{filename}"

        os.makedirs("static", exist_ok=True)

        tts = gTTS(text=clean_text, lang="en")
        tts.save(filepath)

        return filepath
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text-to-speech error: {str(e)}"
        )