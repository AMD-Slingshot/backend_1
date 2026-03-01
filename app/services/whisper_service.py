import requests
from app.config import HUGGINGFACE_API_KEY
from fastapi import HTTPException

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-small"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

def transcribe_audio(audio_bytes):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            data=audio_bytes,
            timeout=30
        )

        result = response.json()

        # Handle model loading case
        if "error" in result:
            error_msg = result["error"]
            if "loading" in error_msg.lower():
                raise HTTPException(
                    status_code=503,
                    detail="Model is loading, please try again in a few seconds"
                )
            elif "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                raise HTTPException(
                    status_code=429,
                    detail="HuggingFace API rate limit exceeded"
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"Transcription error: {error_msg}"
                )

        return {"text": result.get("text", "")}
    
    except HTTPException:
        raise
    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Failed to connect to HuggingFace API: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Transcription error: {str(e)}"
        )