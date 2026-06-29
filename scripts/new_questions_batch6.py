#!/usr/bin/env python3
"""Batch 6: 國家 (cn-37 to cn-72), 新聞 (news-37 to news-72)"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/alan9820/.openclaw/workspace/alan-yoshiki")
QUESTIONS_FILE = ROOT / "questions.json"

NEW_QUESTIONS = [
    # ===== 國家 (cn-37 to cn-72) =====
    {"id": "cn-37", "cat": "國家", "q": "「加拿大」嘅首都係邊個城市？", "opts": ["多倫多", "渥太華 Ottawa", "溫哥華", "蒙特利爾"], "a": 1},
    {"id": "cn-38", "cat": "國家", "q": "「澳洲」最大城市係？", "opts": ["坎培拉", "悉尼", "墨爾本", "布里斯本"], "a": 1},
    {"id": "cn-39", "cat": "國家", "q": "「澳洲」嘅法定首都係？", "opts": ["悉尼", "墨爾本", "坎培拉", "珀斯"], "a": 2},
    {"id": "cn-40", "cat": "國家", "q": "「美國」首府（首都）係邊個城市？", "opts": ["紐約", "洛杉磯", "華盛頓 D.C.", "芝加哥"], "a": 2},
    {"id": "cn-41", "cat": "國家", "q": "「英國」首府（首都）係邊個城市？", "opts": ["Manchester", "倫敦 London", "Liverpool", "Birmingham"], "a": 1},
    {"id": "cn-42", "cat": "國家", "q": "「法國」首府（首都）係邊個城市？", "opts": ["巴黎", "馬賽", "里昂", "尼斯"], "a": 0},
    {"id": "cn-43", "cat": "國家", "q": "「德國」首府（首都）係邊個城市？", "opts": ["慕尼黑", "柏林", "漢堡", "法蘭克福"], "a": 1},
    {"id": "cn-44", "cat": "國家", "q": "「意大利」首府（首都）係邊個城市？", "opts": ["米蘭", "威尼斯", "羅馬", "佛羅倫斯"], "a": 2},
    {"id": "cn-45", "cat": "國家", "q": "「西班牙」首府（首都）係邊個城市？", "opts": ["巴塞隆拿", "馬德里", "華倫西亞", "西維爾"], "a": 1},
    {"id": "cn-46", "cat": "國家", "q": "「葡萄牙」首府（首都）係邊個城市？", "opts": ["波圖", "里斯本", "法魯", "科英布拉"], "a": 1},
    {"id": "cn-47", "cat": "國家", "q": "「荷蘭」首府（首都）係邊個城市？", "opts": ["鹿特丹", "阿姆斯特丹", "海牙", "烏特勒支"], "a": 1},
    {"id": "cn-48", "cat": "國家", "q": "「比利時」首府（首都）係邊個城市？", "opts": ["布魯日", "安特衛普", "布魯塞爾", "根特"], "a": 2},
    {"id": "cn-49", "cat": "國家", "q": "「瑞士」首府（首都）係邊個城市？", "opts": ["蘇黎世", "日內瓦", "伯恩 Bern", "巴塞爾"], "a": 2},
    {"id": "cn-50", "cat": "國家", "q": "「奧地利」首府（首都）係邊個城市？", "opts": ["薩爾斯堡", "維也納 Vienna", "格拉茨", "因斯布魯克"], "a": 1},
    {"id": "cn-51", "cat": "國家", "q": "「瑞典」首府（首都）係邊個城市？", "opts": ["哥德堡", "斯德哥爾摩", "馬爾默", "烏普薩拉"], "a": 1},
    {"id": "cn-52", "cat": "國家", "q": "「挪威」首府（首都）係邊個城市？", "opts": ["奧斯陸", "卑爾根", "斯塔萬格", "特羅姆瑟"], "a": 0},
    {"id": "cn-53", "cat": "國家", "q": "「丹麥」首府（首都）係邊個城市？", "opts": ["哥本哈根", "奧胡斯", "奧爾堡", "歐登塞"], "a": 0},
    {"id": "cn-54", "cat": "國家", "q": "「芬蘭」首府（首都）係邊個城市？", "opts": ["赫爾辛基", "坦佩雷", "圖爾庫", "奧盧"], "a": 0},
    {"id": "cn-55", "cat": "國家", "q": "「波蘭」首府（首都）係邊個城市？", "opts": ["克拉科夫", "華沙", "格但斯克", "波茲南"], "a": 1},
    {"id": "cn-56", "cat": "國家", "q": "「土耳其」首府（首都）係邊個城市？", "opts": ["伊斯坦布爾", "安卡拉 Ankara", "伊茲密爾", "安塔利亞"], "a": 1},
    {"id": "cn-57", "cat": "國家", "q": "「沙特阿拉伯」首府（首都）係邊個城市？", "opts": ["麥加", "利雅得 Riyadh", "吉達", "麥地那"], "a": 1},
    {"id": "cn-58", "cat": "國家", "q": "「阿聯酋」（UAE）首府（首都）係邊個城市？", "opts": ["杜拜", "阿布扎比", "沙迦", "阿吉曼"], "a": 1},
    {"id": "cn-59", "cat": "國家", "q": "「以色列」首府（首都）係邊個城市？", "opts": ["特拉維夫", "耶路撒冷", "海法", "貝爾謝巴"], "a": 1},
    {"id": "cn-60", "cat": "國家", "q": "「印度」首府（首都）係邊個城市？", "opts": ["孟買", "新德里 New Delhi", "班加羅爾", "加爾各答"], "a": 1},
    {"id": "cn-61", "cat": "國家", "q": "「巴基斯坦」首府（首都）係邊個城市？", "opts": ["喀拉蚩", "拉合爾", "伊斯蘭堡 Islamabad", "白沙瓦"], "a": 2},
    {"id": "cn-62", "cat": "國家", "q": "「韓國」首府（首都）係邊個城市？", "opts": ["釜山", "首爾 Seoul", "仁川", "大邱"], "a": 1},
    {"id": "cn-63", "cat": "國家", "q": "「泰國」首府（首都）係邊個城市？", "opts": ["清邁", "曼谷 Bangkok", "布吉", "芭堤雅"], "a": 1},
    {"id": "cn-64", "cat": "國家", "q": "「越南」首府（首都）係邊個城市？", "opts": ["胡志明市", "河內", "峴港", "海防"], "a": 1},
    {"id": "cn-65", "cat": "國家", "q": "「新加坡」首府（首都）係邊個城市？", "opts": ["新加坡 Singapore", "兀蘭", "裕廊", "勿洛"], "a": 0},
    {"id": "cn-66", "cat": "國家", "q": "「馬來西亞」首府（首都）係邊個城市？", "opts": ["吉隆坡", "檳城", "新山", "亞庇"], "a": 0},
    {"id": "cn-67", "cat": "國家", "q": "「菲律賓」首府（首都）係邊個城市？", "opts": ["宿霧", "馬尼拉 Manila", "達沃", "碧瑤"], "a": 1},
    {"id": "cn-68", "cat": "國家", "q": "「印尼」首府（首都）係邊個城市？", "opts": ["泗水", "雅加達（將遷至努山塔拉）", "萬隆", "棉蘭"], "a": 1},
    {"id": "cn-69", "cat": "國家", "q": "「南非」有三個首都，其中行政首都係？", "opts": ["開普敦", "比勒陀利亞 Pretoria", "布隆方丹", "約翰內斯堡"], "a": 1},
    {"id": "cn-70", "cat": "國家", "q": "「紐西蘭」首府（首都）係邊個城市？", "opts": ["奧克蘭", "惠靈頓 Wellington", "基督城", "但尼丁"], "a": 1},
    {"id": "cn-71", "cat": "國家", "q": "「埃及」首府（首都）係邊個城市？", "opts": ["亞歷山大", "開羅 Cairo", "盧克索", "阿斯旺"], "a": 1},
    {"id": "cn-72", "cat": "國家", "q": "「肯尼亞」首府（首都）係邊個城市？", "opts": ["內羅畢 Nairobi", "蒙巴薩", "基蘇木", "埃爾多雷特"], "a": 0},

    # ===== 新聞 (news-37 to news-72) =====
    {"id": "news-37", "cat": "新聞", "q": "「2020 東京奧運」因為疫情延期到邊一年舉辦？", "opts": ["2020 年", "2021 年", "2022 年", "2023 年"], "a": 1},
    {"id": "news-38", "cat": "新聞", "q": "「2022 冬季奧運」喺邊個城市舉辦？", "opts": ["首爾", "北京", "東京", "札幌"], "a": 1},
    {"id": "news-39", "cat": "新聞", "q": "「2024 巴黎奧運」喺邊度開幕？", "opts": ["塞納河", "巴黎鐵塔", "羅浮宮", "凱旋門"], "a": 0},
    {"id": "news-40", "cat": "新聞", "q": "「Tesla」行政總裁 Elon Musk 同時創辦咗邊間太空公司？", "opts": ["NASA", "SpaceX", "Blue Origin", "Virgin Galactic"], "a": 1},
    {"id": "news-41", "cat": "新聞", "q": "「OpenAI」總部主要設喺邊度？", "opts": ["紐約", "三藩市（舊金山）灣區", "倫敦", "東京"], "a": 1},
    {"id": "news-42", "cat": "新聞", "q": "「NVIDIA」以咩類硬件最為聞名？", "opts": ["CPU", "GPU（顯示卡）", "記憶體", "硬碟"], "a": 1},
    {"id": "news-43", "cat": "新聞", "q": "「Microsoft」總部設喺邊個州？", "opts": ["加州", "紐約州", "華盛頓州", "德州"], "a": 2},
    {"id": "news-44", "cat": "新聞", "q": "「Apple」創辦人之一係？", "opts": ["Steve Jobs", "Jeff Bezos", "Larry Page", "Sergey Brin"], "a": 0},
    {"id": "news-45", "cat": "新聞", "q": "「Google」母公司叫咩名？", "opts": ["Alphabet", "Meta", "Apple", "Microsoft"], "a": 0},
    {"id": "news-46", "cat": "新聞", "q": "「Facebook」母公司改名為？", "opts": ["Meta", "Alphabet", "Amazon", "Tesla"], "a": 0},
    {"id": "news-47", "cat": "新聞", "q": "「Amazon」創辦人係邊個？", "opts": ["Jeff Bezos", "Elon Musk", "Bill Gates", "Mark Zuckerberg"], "a": 0},
    {"id": "news-48", "cat": "新聞", "q": "「Tesla」早期最大股東之一，曾幫公司度過難關嘅係邊個？", "opts": ["Elon Musk", "JB Straubel", "Martin Eberhard", "以上皆曾參與"], "a": 3},
    {"id": "news-49", "cat": "新聞", "q": "「ChatGPT」嘅 GPT 全稱主要係咩？", "opts": ["Generative Pre-trained Transformer", "General Purpose Tool", "Graphical Processing Transformer", "Generated Predictive Text"], "a": 0},
    {"id": "news-50", "cat": "新聞", "q": "「區塊鏈」（Blockchain）最為人知嘅應用係？", "opts": ["加密貨幣（如 Bitcoin）", "電郵", "瀏覽器", "雲端儲存"], "a": 0},
    {"id": "news-51", "cat": "新聞", "q": "「Bitcoin」（比特幣）由化名邊位人士喺 2008 年發表論文提出？", "opts": ["Vitalik Buterin", "Satoshi Nakamoto", "Elon Musk", "Mark Zuckerberg"], "a": 1},
    {"id": "news-52", "cat": "新聞", "q": "「以太坊」（Ethereum）共同創辦人包括邊位？", "opts": ["Vitalik Buterin", "Satoshi Nakamoto", "Brian Armstrong", "Changpeng Zhao"], "a": 0},
    {"id": "news-53", "cat": "新聞", "q": "「Apple」首款智能手機 iPhone 喺邊年發佈？", "opts": ["2005 年", "2007 年", "2009 年", "2011 年"], "a": 1},
    {"id": "news-54", "cat": "新聞", "q": "「WhatsApp」最初由邊兩位創辦人創立？", "opts": ["Jan Koum 同 Brian Acton", "Mark Zuckerberg 同 Sheryl Sandberg", "Evan Spiegel 同 Bobby Murphy", "Jack Dorsey 同 Biz Stone"], "a": 0},
    {"id": "news-55", "cat": "新聞", "q": "「Instagram」最初由邊兩位創辦人創立？", "opts": ["Kevin Systrom 同 Mike Krieger", "Mark Zuckerberg 同 Dustin Moskovitz", "Evan Spiegel 同 Bobby Murphy", "Jack Dorsey 同 Biz Stone"], "a": 0},
    {"id": "news-56", "cat": "新聞", "q": "「ChatGPT」首次公開發佈大概喺邊年？", "opts": ["2020 年", "2022 年", "2023 年（廣受關注）", "2025 年"], "a": 2},
    {"id": "news-57", "cat": "新聞", "q": "「2024 美國總統大選」由邊位當選？", "opts": ["Donald Trump", "Joe Biden", "Kamala Harris", "Ron DeSantis"], "a": 0},
    {"id": "news-58", "cat": "新聞", "q": "「2022 卡塔爾世界盃」冠軍係邊隊？", "opts": ["巴西", "法國", "阿根廷", "德國"], "a": 2},
    {"id": "news-59", "cat": "新聞", "q": "「2026 世界盃」將由邊三國合辦？", "opts": ["美國、加拿大、墨西哥", "美國、加拿大、英國", "美國、墨西哥、巴西", "美國、英國、阿根廷"], "a": 0},
    {"id": "news-60", "cat": "新聞", "q": "「香港」2022 年新一屆特首係邊位？", "opts": ["林鄭月娥", "李家超", "梁振英", "曾蔭權"], "a": 1},
    {"id": "news-61", "cat": "新聞", "q": "「英國」2022 年首相係邊位（首位印度裔首相）？", "opts": ["Boris Johnson", "Liz Truss", "Rishi Sunak", "Keir Starmer"], "a": 2},
    {"id": "news-62", "cat": "新聞", "q": "「英女王伊利沙伯二世」喺邊年逝世？", "opts": ["2020 年", "2021 年", "2022 年", "2023 年"], "a": 2},
    {"id": "news-63", "cat": "新聞", "q": "「日本」前首相安倍晉三喺邊年遇刺身亡？", "opts": ["2020 年", "2021 年", "2022 年", "2023 年"], "a": 2},
    {"id": "news-64", "cat": "新聞", "q": "「COVID-19」（新冠疫情）由世界衛生組織定為「全球大流行」大概喺邊年？", "opts": ["2018 年", "2019 年", "2020 年", "2021 年"], "a": 2},
    {"id": "news-65", "cat": "新聞", "q": "「COVID-19」病毒被認為源自邊類動物？", "opts": ["蝙蝠（可能經中間宿主）", "雞", "豬", "狗"], "a": 0},
    {"id": "news-66", "cat": "新聞", "q": "「世衛」（WHO）總部設喺邊個城市？", "opts": ["紐約", "日內瓦", "巴黎", "倫敦"], "a": 1},
    {"id": "news-67", "cat": "新聞", "q": "「聯合國」總部位於邊個城市？", "opts": ["紐約", "日內瓦", "巴黎", "維也納"], "a": 0},
    {"id": "news-68", "cat": "新聞", "q": "「G7」包括以下邊個成員國？", "opts": ["中國", "俄羅斯", "美國", "印度"], "a": 2},
    {"id": "news-69", "cat": "新聞", "q": "「G20」有幾多個成員國（包括歐盟）？", "opts": ["7", "20", "27", "50"], "a": 1},
    {"id": "news-70", "cat": "新聞", "q": "「歐盟」（EU）總部主要設喺邊個城市？", "opts": ["巴黎", "布魯塞爾", "柏林", "羅馬"], "a": 1},
    {"id": "news-71", "cat": "新聞", "q": "「北約」（NATO）總部設喺邊個城市？", "opts": ["紐約", "布魯塞爾", "巴黎", "華盛頓"], "a": 1},
    {"id": "news-72", "cat": "新聞", "q": "「2024 巴黎奧運」閉幕禮中，下屆 2028 奧運主辦城市片段中見到邊個城市？", "opts": ["東京", "洛杉磯", "巴黎", "悉尼"], "a": 1},
]


def main():
    with open(QUESTIONS_FILE, "r") as f:
        data = json.load(f)
    existing_ids = set(q["id"] for q in data["questions"])
    
    errors = []
    for q in NEW_QUESTIONS:
        if q["id"] in existing_ids:
            errors.append(f"Duplicate ID: {q['id']}")
        if len(q["opts"]) != 4:
            errors.append(f"{q['id']}: opts not 4")
        if len(set(q["opts"])) != 4:
            errors.append(f"{q['id']}: opts duplicates")
        if not (0 <= q["a"] <= 3):
            errors.append(f"{q['id']}: a out of range")
    
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        sys.exit(1)
    
    print(f"Validation OK. {len(NEW_QUESTIONS)} questions ready.")
    cats = {}
    for q in NEW_QUESTIONS:
        cats[q['cat']] = cats.get(q['cat'], 0) + 1
    print(f"By cat: {cats}")


if __name__ == "__main__":
    main()