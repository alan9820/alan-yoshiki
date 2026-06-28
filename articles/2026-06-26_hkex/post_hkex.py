#!/usr/bin/env python3
"""Post HKEX financial news to Buffer Instagram feed."""
import sys
sys.path.insert(0, "/home/alan9820/.openclaw/workspace/articles")
from ig_story_poster import post_feed

caption = """📉 港股收市｜恒指跌 405 點 阿里跌 5% 舜宇跌 9% 網易、泡泡瑪特逆市升

恒指今日低開後跌幅擴大，曾跌 558 點，最終收報 22,671 點，跌 405 點，成交 3,421 億元。科指跌 3.4%，報 4,255 點。個股表現：阿里巴巴跌逾 5%、舜宇光學跌 9%、中芯國際跌 7%；網易逆市升 3%、泡泡瑪特升逾 1%。

#HorizonTeam #AI報新聞 #港股 #恒指"""

result = post_feed(
    image_path="/home/alan9820/.openclaw/workspace/articles/2026-06-26_hkex/hkex_final.jpg",
    caption=caption,
    schedule_minutes=2
)
print("RESULT:", result)