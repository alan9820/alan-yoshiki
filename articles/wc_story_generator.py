#!/usr/bin/env python3
"""
World Cup 2026 IG Story Generator
用法: python3 wc_story_generator.py "Team1 vs Team2" "HH:MM HKT Date"

例如: python3 wc_story_generator.py "Saudi Arabia vs Uruguay" "03:00 HKT June 16"
"""
import sys
import subprocess
import os
import json
import requests
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import math

# === CONFIG ===
API_KEY = "6d207e02198a847aa98d0a2a901485a5"
FREEIMAGE_API = "https://freeimage.host/api/1/upload"
POLLINATIONS_API = "https://api.pollenations.com/image"
SEEDREAM_API = "https://api.pollenations.com/image"
IMG_WIDTH, IMG_HEIGHT = 720, 1280

def search_wc_result(team1, team2):
    """搜尋世界盃賽果"""
    # 讀取賽程資料
    schedule_file = "/home/alan9820/.openclaw/workspace/worldcup/schedule.md"
    if os.path.exists(schedule_file):
        with open(schedule_file, 'r') as f:
            content = f.read()
        # 簡單搜尋 - 實際應該用 web search
        return None  # 暫時返回 None，等 cron 自己搜
    return None

def generate_image(team1, team2, output_path):
    """用 Pollinations seedream 生成卡通圖片"""
    prompt = f"cartoon style illustration of {team1} vs {team2} football match, players in action on green grass field, stadium background with crowd, dramatic moment, colorful cartoon art style, no text, no letters, no words"
    
    # 使用 Pollinations API
    url = f"{SEEDREAM_API}?prompt={requests.utils.quote(prompt)}&model=seedream&width=720&height=1280&seed=42"
    
    response = requests.get(url, timeout=120)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            f.write(response.content)
        return True
    return False

def add_overlay_and_watermark(input_path, output_path, team1, team2, score):
    """加 black bar + 白字國家分數 + 金字 WC 2026 + Horizon.Team 浮水印"""
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
    overlay_font_size = int(height * 0.038)
    overlay_font = ImageFont.truetype(font_path, overlay_font_size)
    
    bbox = bar_draw.textbbox((0, 0), match_text, font=overlay_font)
    text_width = bbox[2] - bbox[0]
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

def upload_to_freeimage(image_path):
    """上傳圖片到 freeimage.host"""
    with open(image_path, 'rb') as f:
        response = requests.post(
            FREEIMAGE_API,
            data={'key': API_KEY, 'format': 'json'},
            files={'source': f}
        )
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            return result['image']['url']
    return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python3 wc_story_generator.py 'Team1' 'Team2' 'Score'")
        sys.exit(1)
    
    team1 = sys.argv[1]
    team2 = sys.argv[2]
    score = sys.argv[3]
    
    print(f"Generating World Cup Story: {team1} {score} {team2}")
    
    # 步驟 1: 生成圖片
    raw_img = f"/tmp/wc_raw_{team1}_{team2}.png"
    final_img = f"/tmp/wc_{team1}_{team2}_story.jpg"
    
    if generate_image(team1, team2, raw_img):
        # 步驟 2: 加 overlay + 浮水印
        add_overlay_and_watermark(raw_img, final_img, team1, team2, score)
        
        # 步驟 3: 上傳
        url = upload_to_freeimage(final_img)
        if url:
            print(f"Uploaded: {url}")
            print(f"📱 請確認圖片: {url}")
        else:
            print("上傳失敗")
    else:
        print("圖片生成失敗")
