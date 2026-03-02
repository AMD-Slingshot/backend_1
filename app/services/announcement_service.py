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
    call_to_action: str,
    organization_name: str = "",
    prizes: str = ""
):
    """
    Generate a professional announcement script and marketing content using AI.
    Returns the script text, audio URL, and marketing materials.
    """
    try:
        # Create prompt for announcement script
        announcement_prompt = f"""
Create a {tone} voice announcement script for an event with the following details:

Event: {title}
Organization: {organization_name if organization_name else "N/A"}
Tagline: {tagline}
Description: {description}
Date: {date}
Time: {time}
Venue: {venue}
Prizes/Incentives: {prizes if prizes else "N/A"}
Target Audience: {target_audience}
Call to Action: {call_to_action}

Generate a compelling 30-45 second announcement script that:
- Has an engaging opening
- Clearly communicates the event details
- Matches the {tone} tone
- Appeals to {target_audience}
- Ends with the call to action: "{call_to_action}"

Keep it concise, clear, and enthusiastic. Make it suitable for a voice announcement.
DO NOT use markdown formatting like **bold** or *italic* as this will be converted to speech.
"""
        
        # Generate announcement script
        script = generate_text(announcement_prompt)
        
        # Generate marketing content
        marketing_prompt = f"""
Generate comprehensive marketing content for the following event:

Event: {title}
Tagline: {tagline}
Description: {description}
Date: {date}
Time: {time}
Venue: {venue}
Prizes: {prizes if prizes else "N/A"}
Target Audience: {target_audience}

Please provide:
1. **Taglines**: 3 catchy taglines (10-15 words each) suitable for social media and promotional materials
2. **Captions**: 2 engaging social media captions (50-100 words each) - one short and one detailed
3. **Instagram Hashtags**: 10-15 relevant hashtags for maximum reach

Format your response exactly as:
TAGLINES:
1. [tagline 1]
2. [tagline 2]
3. [tagline 3]

SHORT CAPTION:
[50-word engaging caption]

DETAILED CAPTION:
[100-word detailed caption]

INSTAGRAM HASHTAGS:
#hashtag1 #hashtag2 #hashtag3 [etc.]

Make sure all content is engaging, professional, and tailored to {target_audience}.
"""
        
        # Generate marketing content
        marketing_content = generate_text(marketing_prompt)
        
        # Parse marketing content
        marketing_data = parse_marketing_content(marketing_content)
        
        # Generate audio from script (markdown will be cleaned in TTS)
        audio_path = text_to_speech(script)
        audio_url = f"http://localhost:8000/{audio_path}"
        
        return {
            "script": script,
            "audio_url": audio_url,
            "marketing": marketing_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Announcement generation error: {str(e)}"
        )

def parse_marketing_content(content: str) -> dict:
    """
    Parse the AI-generated marketing content into structured format.
    """
    try:
        marketing = {
            "taglines": [],
            "short_caption": "",
            "detailed_caption": "",
            "hashtags": []
        }
        
        # Split content into sections
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Detect sections
            if 'TAGLINES:' in line.upper():
                current_section = 'taglines'
                continue
            elif 'SHORT CAPTION:' in line.upper():
                current_section = 'short_caption'
                continue
            elif 'DETAILED CAPTION:' in line.upper():
                current_section = 'detailed_caption'
                continue
            elif 'INSTAGRAM HASHTAGS:' in line.upper() or 'HASHTAGS:' in line.upper():
                current_section = 'hashtags'
                continue
            
            # Add content to appropriate section
            if current_section == 'taglines':
                # Remove numbering
                tagline = line.lstrip('0123456789.-) ')
                if tagline:
                    marketing['taglines'].append(tagline)
            
            elif current_section == 'short_caption':
                marketing['short_caption'] += line + ' '
            
            elif current_section == 'detailed_caption':
                marketing['detailed_caption'] += line + ' '
            
            elif current_section == 'hashtags':
                # Extract hashtags
                hashtags = [tag.strip() for tag in line.split() if tag.strip().startswith('#')]
                marketing['hashtags'].extend(hashtags)
        
        # Clean up captions
        marketing['short_caption'] = marketing['short_caption'].strip()
        marketing['detailed_caption'] = marketing['detailed_caption'].strip()
        
        # Ensure we have at least some default content
        if not marketing['taglines']:
            marketing['taglines'] = ["Join us for an amazing event!", "Don't miss out!", "Be there!"]
        
        if not marketing['hashtags']:
            marketing['hashtags'] = ["#event", "#community", "#dontmissout"]
        
        return marketing
    
    except Exception as e:
        # Return default marketing content if parsing fails
        return {
            "taglines": ["Join us for an amazing event!", "Don't miss out!", "Be there!"],
            "short_caption": "Exciting event coming up! Join us for an unforgettable experience.",
            "detailed_caption": "We're thrilled to invite you to our upcoming event. This is a unique opportunity to connect, learn, and grow. Don't miss out on this amazing experience!",
            "hashtags": ["#event", "#community", "#dontmissout", "#joinustoday"]
        }
