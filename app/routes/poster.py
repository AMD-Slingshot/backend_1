from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.poster_service import generate_poster
from app.services.announcement_service import generate_announcement_script

router = APIRouter()

class PosterRequest(BaseModel):
    title: str
    description: str
    date: str
    venue: str
    tagline: str = ""
    time: str
    theme_color: str = "#2980b9"  # Default blue
    tone: str = "formal"  # formal, fun, technical
    target_audience: str = "general public"
    call_to_action: str = "Register Now"

@router.post("/generate-poster")
async def create_poster(request: PosterRequest):
    """
    Generate an event poster and voice announcement based on provided details.
    
    Returns:
    - poster_url: URL to download the generated poster image
    - announcement_script: AI-generated announcement text
    - announcement_audio: URL to the audio announcement
    """
    try:
        # Generate poster image
        poster_path = generate_poster(
            title=request.title,
            description=request.description,
            date=request.date,
            venue=request.venue,
            tagline=request.tagline,
            time=request.time,
            theme_color=request.theme_color,
            tone=request.tone,
            target_audience=request.target_audience,
            call_to_action=request.call_to_action
        )
        
        # Generate announcement script and audio
        announcement = generate_announcement_script(
            title=request.title,
            description=request.description,
            date=request.date,
            venue=request.venue,
            tagline=request.tagline,
            time=request.time,
            tone=request.tone,
            target_audience=request.target_audience,
            call_to_action=request.call_to_action
        )
        
        # Convert paths to URLs
        poster_url = f"http://localhost:8000/{poster_path}"
        
        return {
            "poster_url": poster_url,
            "announcement_script": announcement["script"],
            "announcement_audio": announcement["audio_url"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating poster: {str(e)}"
        )
