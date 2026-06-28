#!/usr/bin/env python3
"""Post Trump World Cup news to Buffer Instagram feed."""
import sys
sys.path.insert(0, "/home/alan9820/.openclaw/workspace/articles")
from ig_story_poster import post_feed

caption = """🏆 特朗普將於世界盃決賽親手頒獎！FIFA 主席因凡蒂諾確認，特朗普將於 7 月 19 日喺新澤西 MetLife 體育場嘅世界盃決賽上，向冠軍球隊頒發獎盃。係佢連續第二年參與世界盃頒獎儀式。⚽🇺🇸

#HorizonTeam #AI報新聞 #世界盃 #FIFA"""

result = post_feed(
    image_path="/home/alan9820/.openclaw/workspace/articles/2026-06-26_trump_worldcup/worldcup_trump_v1_final.jpg",
    caption=caption,
    schedule_minutes=2
)
print("RESULT:", result)
