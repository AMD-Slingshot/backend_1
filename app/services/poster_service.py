from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from fastapi import HTTPException
import uuid

def generate_poster(
    title: str,
    description: str,
    date: str,
    venue: str,
    tagline: str,
    time: str,
    theme_color: str,
    tone: str,
    target_audience: str,
    call_to_action: str
):
    """
    Generate an event poster based on input parameters.
    Returns the filepath of the generated poster.
    """
    try:
        # Poster dimensions
        width, height = 800, 1200
        
        # Parse theme color (default to blue if invalid)
        try:
            # Remove # if present and convert to RGB
            color_hex = theme_color.lstrip('#')
            if len(color_hex) == 6:
                theme_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            else:
                theme_rgb = (41, 128, 185)  # Default blue
        except:
            theme_rgb = (41, 128, 185)  # Default blue
        
        # Create a gradient background
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create gradient background
        for i in range(height):
            # Gradient from theme color to lighter version
            ratio = i / height
            r = int(theme_rgb[0] + (255 - theme_rgb[0]) * ratio * 0.3)
            g = int(theme_rgb[1] + (255 - theme_rgb[1]) * ratio * 0.3)
            b = int(theme_rgb[2] + (255 - theme_rgb[2]) * ratio * 0.3)
            draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
        
        # Add decorative header bar
        header_height = 150
        draw.rectangle([(0, 0), (width, header_height)], fill=theme_rgb)
        
        # Try to load fonts (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("arial.ttf", 60)
            tagline_font = ImageFont.truetype("arial.ttf", 30)
            heading_font = ImageFont.truetype("arialbd.ttf", 36)
            body_font = ImageFont.truetype("arial.ttf", 28)
            small_font = ImageFont.truetype("arial.ttf", 24)
            cta_font = ImageFont.truetype("arialbd.ttf", 40)
        except:
            title_font = ImageFont.load_default()
            tagline_font = ImageFont.load_default()
            heading_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            cta_font = ImageFont.load_default()
        
        y_position = 30
        
        # Draw title (wrapped if needed)
        title_wrapped = textwrap.fill(title.upper(), width=20)
        title_bbox = draw.multiline_textbbox((0, 0), title_wrapped, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (width - title_width) // 2
        draw.multiline_text((title_x, y_position), title_wrapped, fill='white', font=title_font, align='center')
        y_position += title_bbox[3] - title_bbox[1] + 40
        
        # Draw tagline
        if tagline:
            tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
            tagline_width = tagline_bbox[2] - tagline_bbox[0]
            tagline_x = (width - tagline_width) // 2
            draw.text((tagline_x, y_position), tagline, fill='white', font=tagline_font)
            y_position += 80
        else:
            y_position += 40
        
        # Draw description box
        padding = 50
        desc_wrapped = textwrap.fill(description, width=40)
        draw.rectangle([(padding, y_position), (width-padding, y_position+200)], 
                      fill='white', outline=theme_rgb, width=3)
        draw.multiline_text((padding+20, y_position+20), desc_wrapped, 
                           fill='black', font=small_font, spacing=8)
        y_position += 230
        
        # Event details section
        details_y = y_position
        
        # Date & Time
        draw.text((padding, details_y), "📅 DATE:", fill='white', font=heading_font)
        draw.text((padding+20, details_y+45), date, fill='white', font=body_font)
        details_y += 100
        
        draw.text((padding, details_y), "🕐 TIME:", fill='white', font=heading_font)
        draw.text((padding+20, details_y+45), time, fill='white', font=body_font)
        details_y += 100
        
        # Venue
        draw.text((padding, details_y), "📍 VENUE:", fill='white', font=heading_font)
        venue_wrapped = textwrap.fill(venue, width=35)
        draw.multiline_text((padding+20, details_y+45), venue_wrapped, fill='white', font=body_font)
        details_y += 120
        
        # Call to action button
        cta_y = height - 180
        cta_box_height = 80
        cta_margin = 100
        
        # Draw CTA box
        draw.rounded_rectangle(
            [(cta_margin, cta_y), (width-cta_margin, cta_y+cta_box_height)],
            radius=15,
            fill='white',
            outline=theme_rgb,
            width=4
        )
        
        # Draw CTA text
        cta_bbox = draw.textbbox((0, 0), call_to_action.upper(), font=cta_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        cta_x = (width - cta_width) // 2
        draw.text((cta_x, cta_y+15), call_to_action.upper(), fill=theme_rgb, font=cta_font)
        
        # Target audience badge
        badge_text = f"For: {target_audience.title()}"
        badge_bbox = draw.textbbox((0, 0), badge_text, font=small_font)
        badge_width = badge_bbox[2] - badge_bbox[0]
        badge_x = (width - badge_width) // 2
        draw.text((badge_x, height-60), badge_text, fill='white', font=small_font)
        
        # Save poster
        os.makedirs("static/posters", exist_ok=True)
        filename = f"poster_{uuid.uuid4()}.png"
        filepath = f"static/posters/{filename}"
        img.save(filepath, 'PNG', quality=95)
        
        return filepath
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Poster generation error: {str(e)}"
        )
