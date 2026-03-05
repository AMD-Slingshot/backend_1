import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.poster_service import generate_poster
from app.services.announcement_service import generate_announcement_script
API_URL = os.getenv("API_URL")
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
    # New fields
    registration_link: str = ""
    organization_name: str = ""
    prizes: str = ""
    contact_info: str = ""

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
            call_to_action=request.call_to_action,
            organization_name=request.organization_name,
            registration_link=request.registration_link,
            prizes=request.prizes,
            contact_info=request.contact_info
        )
        
        # Generate announcement script and audio with marketing content
        announcement = generate_announcement_script(
            title=request.title,
            description=request.description,
            date=request.date,
            venue=request.venue,
            tagline=request.tagline,
            time=request.time,
            tone=request.tone,
            target_audience=request.target_audience,
            call_to_action=request.call_to_action,
            organization_name=request.organization_name,
            prizes=request.prizes
        )
        
        # Convert paths to URLs
        poster_url = f"{API_URL}/{poster_path}"
        
        return {
            "poster_url": poster_url,
            "announcement_script": announcement["script"],
            "announcement_audio": announcement["audio_url"],
            "marketing": announcement["marketing"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating poster: {str(e)}"
        )
