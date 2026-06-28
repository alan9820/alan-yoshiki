#!/usr/bin/env python3
"""Post Venezuela earthquake news to Buffer Instagram feed."""
import sys
sys.path.insert(0, "/home/alan9820/.openclaw/workspace/articles")
from ig_story_poster import post_feed

caption = """🌍 委內瑞拉地震增至 235 人遇難、4,300 人受傷，2 名中國公民亦不幸遇難。中美兩國均表示願意提供人道援助，聯合國救援隊已抵達災區，代總統統籌軍方展開大規模救援行動。

#HorizonTeam #AI報新聞 #委內瑞拉 #地震"""

result = post_feed(
    image_path="/home/alan9820/.openclaw/workspace/articles/2026-06-26_venezuela/venezuela_earthquake_final.jpg",
    caption=caption,
    schedule_minutes=2
)
print("RESULT:", result)
