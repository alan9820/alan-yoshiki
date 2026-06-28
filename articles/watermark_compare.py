#!/usr/bin/env python3
"""Compare two watermark versions: white+higher opacity vs black"""
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import math

def add_watermark(input_path, output_path, fill_color, opacity, step_x_mul=4.0, step_y_mul=5.0):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size
    
    angle = 45
    scale = 2
    
    new_w, new_h = width * scale, height * scale
    font_size = 56 * scale
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    
    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), "Horizon.Team", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    
    step_x = int(text_w * step_x_mul)
    step_y = int(text_h * step_y_mul)
    
    extra = int(max(new_w, new_h) * (math.sqrt(2) - 1) / 2) + 100
    rotated_w = new_w + extra * 2
    rotated_h = new_h + extra * 2
    
    large_layer = Image.new('RGBA', (rotated_w, rotated_h), (0, 0, 0, 0))
    large_draw = ImageDraw.Draw(large_layer)
    for y in range(-new_h, new_h * 2, step_y):
        for x in range(-new_w, new_w * 2, step_x):
            large_draw.text((x + extra, y + extra), "Horizon.Team", font=font, fill=(*fill_color, opacity))
    
    large_layer = large_layer.filter(ImageFilter.GaussianBlur(radius=1.5 * scale))
    layer_rotated = large_layer.rotate(angle, expand=True, fillcolor=(0, 0, 0, 0))
    layer_rotated = layer_rotated.resize((width, height), Image.LANCZOS)
    
    output = Image.alpha_composite(img, layer_rotated)
    output.convert('RGB').save(output_path, 'JPEG', quality=95)
    print(f"✅ Watermarked: {output_path}")

if __name__ == "__main__":
    import sys
    input_path = sys.argv[1]
    out_white = sys.argv[2]   # white + opacity 150
    out_black = sys.argv[3]   # black + opacity 100
    
    add_watermark(input_path, out_white, (255, 255, 255), 150)
    add_watermark(input_path, out_black, (30, 30, 30), 100)
