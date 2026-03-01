from app.services.gemini_service import generate_text
from app.services.tts_service import text_to_speech
from fastapi import HTTPException

def generate_announcement_script(
    title: str,
    description: str,
    date: str,
    venue: str,
    tagline: str,
    time: str,
    tone: str,
    target_audience: str,
    call_to_action: str
):
    """
    Generate a professional announcement script using AI based on event details.
    Returns the script text and audio URL.
    """
    try:
        # Create prompt for AI to generate announcement
        prompt = f"""
Create a {tone} voice announcement script for an event with the following details:

Event: {title}
Tagline: {tagline}
Description: {description}
Date: {date}
Time: {time}
Venue: {venue}
Target Audience: {target_audience}
Call to Action: {call_to_action}

Generate a compelling 30-45 second announcement script that:
- Has an engaging opening
- Clearly communicates the event details
- Matches the {tone} tone
- Appeals to {target_audience}
- Ends with the call to action: "{call_to_action}"

Keep it concise, clear, and enthusiastic. Make it suitable for a voice announcement.
"""
        
        # Generate script using AI
        script = generate_text(prompt)
        
        # Generate audio from script
        audio_path = text_to_speech(script)
        audio_url = f"http://localhost:8000/{audio_path}"
        
        return {
            "script": script,
            "audio_url": audio_url
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Announcement generation error: {str(e)}"
        )
