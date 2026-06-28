#!/usr/bin/env python3
"""Horizon.Team watermark v3 - validated method"""
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import math
import sys

def add_watermark(input_path, output_path, watermark_text="Horizon.Team"):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    angle = 45
    opacity = 80
    scale = 2
    
    new_w, new_h = width * scale, height * scale
    font_size = 56 * scale
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    # Get text dimensions
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), watermark_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    step_x = int(text_w * 4.0)
    step_y = int(text_h * 5.0)
    
    # Calculate rotation extra space
    extra = int(max(new_w, new_h) * (math.sqrt(2) - 1) / 2) + 100
    rotated_w = new_w + extra * 2
    rotated_h = new_h + extra * 2
    
    # Draw watermark on large layer
    large_layer = Image.new('RGBA', (rotated_w, rotated_h), (0, 0, 0, 0))
    large_draw = ImageDraw.Draw(large_layer)
    for y in range(-new_h, new_h * 2, step_y):
        for x in range(-new_w, new_w * 2, step_x):
            large_draw.text((x + extra, y + extra), watermark_text, font=font, fill=(255, 255, 255, opacity))
    
    large_layer = large_layer.filter(ImageFilter.GaussianBlur(radius=1.5 * scale))
    layer_rotated = large_layer.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
    layer_rotated = layer_rotated.resize((width, height), Image.LANCZOS)
    
    output = Image.alpha_composite(img, layer_rotated)
    output.convert('RGB').save(output_path, 'JPEG', quality=95)
    print(f"✅ Watermarked: {output_path}")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    add_watermark(input_path, output_path)
