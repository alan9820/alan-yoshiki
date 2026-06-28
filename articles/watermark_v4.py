#!/usr/bin/env python3
"""Horizon.Team watermark v4 - 3 vertical columns, layout tilted 30° left"""
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import math
import sys

def add_watermark(input_path, output_path, watermark_text="Horizon.Team"):
    img = Image.open(input_path).convert('RGBA')
    width, height = img.size

    opacity = 100
    scale = 2
    layout_tilt = -30  # rotate entire layout 30° counter-clockwise (left)

    new_w, new_h = width * scale, height * scale
    font_size = 14 * scale
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    font = ImageFont.truetype(font_path, font_size)

    temp_img = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), watermark_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Build a layer large enough so rotation doesn't crop columns
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
            side_draw.text((col_x, y), watermark_text, font=font, fill=(255, 255, 255, opacity))

    side_layer = side_layer.filter(ImageFilter.GaussianBlur(radius=0.5 * scale))

    # Rotate the entire layout
    rotated_layer = side_layer.rotate(layout_tilt, resample=Image.BICUBIC, expand=False)

    # Crop back to image size, centered
    cx = big_w // 2
    cy = big_h // 2
    crop_box = (cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2)
    rotated_layer = rotated_layer.crop(crop_box)

    output = Image.alpha_composite(img, rotated_layer)
    output.convert('RGB').save(output_path, 'JPEG', quality=95)
    print(f"✅ Watermarked: {output_path}")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    add_watermark(input_path, output_path)
