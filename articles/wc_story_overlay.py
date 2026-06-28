#!/usr/bin/env python3
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import math

def add_watermark_and_overlay(input_path, output_path, team1, team2, score, event_name=""):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    # === PART 1: Horizon.Team watermark v4 tilt -30° ===
    opacity = 100
    scale = 2
    layout_tilt = -30
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font_size = 14 * scale
    font = ImageFont.truetype(font_path, font_size)
    
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), "Horizon.Team", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    extra = int(max(width, height) * (math.sqrt(2) - 1) / 2) + 200
    big_w = width + extra * 2
    big_h = height + extra * 2
    
    side_layer = Image.new('RGBA', (big_w, big_h), (0, 0, 0, 0))
    side_draw = ImageDraw.Draw(side_layer)
    
    v_step_y = int(text_h * 8.0)
    
    col_positions = [
        int(width * 0.05) + extra,
        int(width * 0.50) + extra,
        int(width * 0.95) + extra,
    ]
    
    for col_x in col_positions:
        for y in range(-text_h + extra, height + text_h + extra, v_step_y):
            side_draw.text((col_x, y), "Horizon.Team", font=font, fill=(255, 255, 255, opacity))
    
    side_layer = side_layer.filter(ImageFilter.GaussianBlur(radius=0.5 * scale))
    rotated_layer = side_layer.rotate(layout_tilt, resample=Image.BICUBIC, expand=False)
    
    cx = big_w // 2
    cy = big_h // 2
    crop_box = (cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2)
    rotated_layer = rotated_layer.crop(crop_box)
    
    img = Image.alpha_composite(img, rotated_layer)
    
    # === PART 2: Text overlay bar at bottom ===
    bar_height = int(height * 0.14)
    bar = Image.new('RGBA', (width, bar_height), (0, 0, 0, 230))
    bar_draw = ImageDraw.Draw(bar)
    
    # Draw score text
    match_text = f"{team1} {score} {team2}"
    # Reduced from 0.038 -> 0.030 to prevent overflow for long country names
    overlay_font_size = int(height * 0.030)
    overlay_font = ImageFont.truetype(font_path, overlay_font_size)
    
    # Use getlength() for accurate text width (textbbox underestimates due to char bearings)
    text_width = overlay_font.getlength(match_text)
    bbox = overlay_font.getbbox(match_text)
    text_height = bbox[3] - bbox[1]
    
    text_x = (width - text_width) // 2
    text_y = int(bar_height * 0.18)
    
    bar_draw.text((text_x, text_y), match_text, font=overlay_font, fill=(255, 255, 255, 255))
    
    # WC 2026 on next line
    badge_text = "WC 2026"
    badge_font_size = int(height * 0.028)
    badge_font = ImageFont.truetype(font_path, badge_font_size)
    badge_bbox = bar_draw.textbbox((0, 0), badge_text, font=badge_font)
    badge_width = badge_bbox[2] - badge_bbox[0]
    badge_x = (width - badge_width) // 2
    badge_y = text_y + text_height + int(height * 0.015)
    bar_draw.text((badge_x, badge_y), badge_text, font=badge_font, fill=(255, 215, 0, 255))
    
    # Composite bar at bottom
    img.paste(bar, (0, height - bar_height), bar)
    
    # Convert and save
    final = img.convert('RGB')
    final.save(output_path, 'JPEG', quality=95)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    # Netherlands vs Japan
    add_watermark_and_overlay(
        "/home/alan9820/.openclaw/media/inbound/a1f3c99d-ee24-445f-bbf2-c576b805d314.jpg",
        "/home/alan9820/.openclaw/workspace/articles/netherlands_japan_story.jpg",
        "Netherlands", "Japan", "2-2"
    )
    
    # Ivory Coast vs Ecuador
    add_watermark_and_overlay(
        "/home/alan9820/.openclaw/media/inbound/2f510c85-7907-4cee-8386-66d10c55bca0.jpg",
        "/home/alan9820/.openclaw/workspace/articles/ivorycoast_ecuador_story.jpg",
        "Ivory Coast", "Ecuador", "1-0"
    )