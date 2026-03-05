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
    call_to_action: str,
    organization_name: str = "",
    registration_link: str = "",
    prizes: str = "",
    contact_info: str = ""
):
    """
    Generate a professional event poster based on input parameters.
    Returns the filepath of the generated poster.
    """
    try:
        # Poster dimensions - larger for better quality
        width, height = 1080, 1920
        
        # Parse theme color (default to blue if invalid)
        try:
            color_hex = theme_color.lstrip('#')
            if len(color_hex) == 6:
                theme_rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
            else:
                theme_rgb = (41, 128, 185)
        except:
            theme_rgb = (41, 128, 185)
        
        # Create image with gradient background
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Create modern gradient background
        for i in range(height):
            ratio = i / height
            r = int(theme_rgb[0] * (1 - ratio * 0.4))
            g = int(theme_rgb[1] * (1 - ratio * 0.4))
            b = int(theme_rgb[2] * (1 - ratio * 0.4))
            draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
        
        # Add decorative elements - top accent bar
        accent_color = tuple(min(255, int(c * 0.7)) for c in theme_rgb)
        draw.rectangle([(0, 0), (width, 20)], fill=accent_color)
        
        # Load fonts - try Windows fonts first, then Linux fonts
        def load_font(size, bold=False):
            # Windows fonts
            windows_fonts = ["arialbd.ttf" if bold else "arial.ttf"]
            # Linux/Unix fonts (DejaVu installed via apt-packages.txt)
            linux_fonts = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
            ]
            
            for font_path in windows_fonts + linux_fonts:
                try:
                    return ImageFont.truetype(font_path, size)
                except:
                    continue
            
            # Fallback - create a proper sized default
            return ImageFont.load_default()
        
        org_font = load_font(40, bold=True)
        title_font = load_font(90, bold=True)
        tagline_font = load_font(45, bold=False)
        heading_font = load_font(50, bold=True)
        body_font = load_font(42, bold=False)
        small_font = load_font(36, bold=False)
        cta_font = load_font(60, bold=True)
        prize_font = load_font(48, bold=True)
        
        y_position = 60
        padding = 60
        
        # Draw organization name at top if provided
        if organization_name:
            org_text = f"Presented by {organization_name}".upper()
            org_bbox = draw.textbbox((0, 0), org_text, font=org_font)
            org_width = org_bbox[2] - org_bbox[0]
            org_x = (width - org_width) // 2
            draw.text((org_x, y_position), org_text, fill='white', font=org_font)
            y_position += 100
        
        # Draw decorative line
        line_margin = width // 4
        draw.rectangle([(line_margin, y_position), (width - line_margin, y_position + 8)], 
                      fill='white')
        y_position += 60
        
        # Draw title (wrapped if needed)
        title_wrapped = textwrap.fill(title.upper(), width=15)
        title_lines = title_wrapped.split('\n')
        for line in title_lines:
            line_bbox = draw.textbbox((0, 0), line, font=title_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (width - line_width) // 2
            draw.text((line_x, y_position), line, fill='white', font=title_font)
            y_position += 110
        
        # Draw tagline
        if tagline:
            tagline_bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
            tagline_width = tagline_bbox[2] - tagline_bbox[0]
            tagline_x = (width - tagline_width) // 2
            draw.text((tagline_x, y_position), tagline, fill='white', font=tagline_font)
            y_position += 100
        
        # Draw decorative line
        draw.rectangle([(line_margin, y_position), (width - line_margin, y_position + 8)], 
                      fill='white')
        y_position += 80
        
        # Description box with rounded corners
        desc_y = y_position
        desc_height = 280
        box_padding = 80
        draw.rounded_rectangle(
            [(box_padding, desc_y), (width-box_padding, desc_y+desc_height)],
            radius=30,
            fill='white'
        )
        desc_wrapped = textwrap.fill(description, width=35)
        draw.multiline_text((box_padding+40, desc_y+40), desc_wrapped, 
                           fill='black', font=body_font, spacing=12, align='center')
        y_position = desc_y + desc_height + 80
        
        # Event details section
        details_y = y_position
        icon_size = 60
        col1_x = padding + 40
        col2_x = width // 2 + 40
        
        # Date
        draw.ellipse([(col1_x, details_y), (col1_x+icon_size, details_y+icon_size)], 
                    fill='white')
        draw.text((col1_x+10, details_y+10), "📅", font=body_font)
        draw.text((col1_x+icon_size+20, details_y), "DATE", fill='white', font=heading_font)
        draw.text((col1_x+icon_size+20, details_y+55), date, fill='white', font=body_font)
        
        # Time
        draw.ellipse([(col2_x, details_y), (col2_x+icon_size, details_y+icon_size)], 
                    fill='white')
        draw.text((col2_x+10, details_y+10), "🕐", font=body_font)
        draw.text((col2_x+icon_size+20, details_y), "TIME", fill='white', font=heading_font)
        draw.text((col2_x+icon_size+20, details_y+55), time, fill='white', font=body_font)
        
        details_y += 150
        
        # Venue
        draw.ellipse([(col1_x, details_y), (col1_x+icon_size, details_y+icon_size)], 
                    fill='white')
        draw.text((col1_x+10, details_y+10), "📍", font=body_font)
        draw.text((col1_x+icon_size+20, details_y), "VENUE", fill='white', font=heading_font)
        venue_wrapped = textwrap.fill(venue, width=30)
        draw.multiline_text((col1_x+icon_size+20, details_y+55), venue_wrapped, 
                           fill='white', font=body_font, spacing=8)
        details_y += 150
        
        # Prizes section if provided
        if prizes:
            prizes_y = details_y + 20
            prize_box_padding = 100
            prize_height = 120
            draw.rounded_rectangle(
                [(prize_box_padding, prizes_y), (width-prize_box_padding, prizes_y+prize_height)],
                radius=20,
                fill='#FFD700',
                outline='white',
                width=4
            )
            draw.text((width//2 - 100, prizes_y+20), "🏆 PRIZES", fill='#000', font=heading_font)
            prize_wrapped = textwrap.fill(prizes, width=30)
            draw.multiline_text((prize_box_padding+40, prizes_y+75), prize_wrapped, 
                              fill='#000', font=body_font, align='center', spacing=8)
            details_y = prizes_y + prize_height + 60
        
        # Contact info if provided
        if contact_info:
            contact_bbox = draw.textbbox((0, 0), f"📞 {contact_info}", font=small_font)
            contact_width = contact_bbox[2] - contact_bbox[0]
            contact_x = (width - contact_width) // 2
            draw.text((contact_x, details_y+20), f"📞 {contact_info}", fill='white', font=small_font)
            details_y += 80
        
        # Call to action button
        cta_y = height - 280
        cta_box_height = 120
        cta_margin = 150
        
        # Shadow effect
        shadow_offset = 8
        draw.rounded_rectangle(
            [(cta_margin+shadow_offset, cta_y+shadow_offset), 
             (width-cta_margin+shadow_offset, cta_y+cta_box_height+shadow_offset)],
            radius=25,
            fill='#00000040'
        )
        draw.rounded_rectangle(
            [(cta_margin, cta_y), (width-cta_margin, cta_y+cta_box_height)],
            radius=25,
            fill='white',
            outline='#FFD700',
            width=6
        )
        
        # CTA text
        cta_text = call_to_action.upper()
        cta_bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        cta_width = cta_bbox[2] - cta_bbox[0]
        cta_x = (width - cta_width) // 2
        draw.text((cta_x, cta_y+30), cta_text, fill=theme_rgb, font=cta_font)
        
        # QR code placeholder
        if registration_link:
            qr_text = "Scan QR to Register →"
            qr_bbox = draw.textbbox((0, 0), qr_text, font=small_font)
            qr_width = qr_bbox[2] - qr_bbox[0]
            qr_x = (width - qr_width) // 2
            draw.text((qr_x, height-130), qr_text, fill='white', font=small_font)
        
        # Target audience badge
        badge_text = f"Open to: {target_audience.title()}"
        badge_bbox = draw.textbbox((0, 0), badge_text, font=small_font)
        badge_width = badge_bbox[2] - badge_bbox[0]
        badge_x = (width - badge_width) // 2
        draw.text((badge_x, height-70), badge_text, fill='white', font=small_font)
        
        # Save poster
        os.makedirs("static/posters", exist_ok=True)
        filename = f"poster_{uuid.uuid4()}.png"
        filepath = f"static/posters/{filename}"
        img.save(filepath, 'PNG', quality=95, dpi=(300, 300))
        
        return filepath
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Poster generation error: {str(e)}"
        )
