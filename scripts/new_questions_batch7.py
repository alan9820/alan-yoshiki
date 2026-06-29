#!/usr/bin/env python3
"""Batch 7: 科技 (tec-37 to tec-72), 金融 (fin-37 to fin-72)"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/alan9820/.openclaw/workspace/alan-yoshiki")
QUESTIONS_FILE = ROOT / "questions.json"

NEW_QUESTIONS = [
    # ===== 科技 (tec-37 to tec-72) =====
    {"id": "tec-37", "cat": "科技", "q": "「Apple」iPhone 採用嘅作業系統叫？", "opts": ["Android", "iOS", "Windows", "HarmonyOS"], "a": 1},
    {"id": "tec-38", "cat": "科技", "q": "「Android」作業系統由邊間公司開發？", "opts": ["Apple", "Google", "Microsoft", "Samsung"], "a": 1},
    {"id": "tec-39", "cat": "科技", "q": "「Windows」作業系統由邊間公司開發？", "opts": ["Apple", "Google", "Microsoft", "IBM"], "a": 2},
    {"id": "tec-40", "cat": "科技", "q": "「Linux」作業系統最為人知嘅發行版本包括以下邊個？", "opts": ["Ubuntu", "Debian", "Fedora", "以上皆是"], "a": 3},
    {"id": "tec-41", "cat": "科技", "q": "「HTTP」全稱係咩？", "opts": ["HyperText Transfer Protocol", "High Transfer Text Protocol", "Hyper Text Transfer Process", "High Text Transfer Protocol"], "a": 0},
    {"id": "tec-42", "cat": "科技", "q": "「HTTPS」入面個「S」代表咩？", "opts": ["Server", "Secure", "Standard", "Speed"], "a": 1},
    {"id": "tec-43", "cat": "科技", "q": "「URL」全稱係咩？", "opts": ["Uniform Resource Locator", "Universal Resource Link", "Uniform Reference Locator", "Universal Routing Link"], "a": 0},
    {"id": "tec-44", "cat": "科技", "q": "「IP 地址」主要用嚟做咩？", "opts": ["加密通訊", "識別網絡上嘅裝置", "壓縮檔案", "圖像渲染"], "a": 1},
    {"id": "tec-45", "cat": "科技", "q": "「DNS」主要功能係咩？", "opts": ["防火牆", "將域名轉換成 IP", "加密電郵", "病毒掃描"], "a": 1},
    {"id": "tec-46", "cat": "科技", "q": "「Wi-Fi」由邊間公司聯盟推廣？", "opts": ["Wi-Fi Alliance", "IEEE 802.11 標準", "B 同 C 都對", "ISO"], "a": 2},
    {"id": "tec-47", "cat": "科技", "q": "「藍牙」（Bluetooth）技術名稱源自邊個歷史人物？", "opts": ["Harald Bluetooth（丹麥國王）", "Beethoven", "Bell（電話之父）", "Edison"], "a": 0},
    {"id": "tec-48", "cat": "科技", "q": "「5G」主要邊個頻段使用？", "opts": ["低頻（<1 GHz）", "中頻（3–6 GHz）", "高頻（毫米波 24+ GHz）", "B 同 C 都係"], "a": 3},
    {"id": "tec-49", "cat": "科技", "q": "「晶片」主要用邊種材料製造？", "opts": ["銅", "矽（Silicon）", "塑膠", "金"], "a": 1},
    {"id": "tec-50", "cat": "科技", "q": "「CPU」全稱係咩？", "opts": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Control Processing Unit"], "a": 0},
    {"id": "tec-51", "cat": "科技", "q": "「GPU」全稱係咩？", "opts": ["General Processing Unit", "Graphics Processing Unit", "Graphical Performance Unit", "General Purpose Utility"], "a": 1},
    {"id": "tec-52", "cat": "科技", "q": "「RAM」用嚟做咩？", "opts": ["永久儲存", "短期記憶（運行中）", "散熱", "音效"], "a": 1},
    {"id": "tec-53", "cat": "科技", "q": "「SSD」相對「HDD」嘅主要優勢係？", "opts": ["容量大好多", "速度更快、無機械部件", "更平", "更易維修"], "a": 1},
    {"id": "tec-54", "cat": "科技", "q": "「USB」全稱係咩？", "opts": ["Universal Serial Bus", "Unified System Bridge", "Ultra Speed Bus", "United Serial Board"], "a": 0},
    {"id": "tec-55", "cat": "科技", "q": "「HDMI」主要用嚟傳輸咩？", "opts": ["聲音同影像", "電力", "純文字", "純聲音"], "a": 0},
    {"id": "tec-56", "cat": "科技", "q": "「QR Code」最初由邊間日本公司發明？", "opts": ["Sony", "Denso Wave（電裝）", "Toyota", "Panasonic"], "a": 1},
    {"id": "tec-57", "cat": "科技", "q": "「JPEG」係咩類型檔案？", "opts": ["音訊", "影像（圖片）", "文字", "影片"], "a": 1},
    {"id": "tec-58", "cat": "科技", "q": "「MP3」係咩類型檔案？", "opts": ["音訊", "影片", "圖片", "文件"], "a": 0},
    {"id": "tec-59", "cat": "科技", "q": "「PDF」全稱係咩？", "opts": ["Portable Document Format", "Personal Document File", "Print Document Format", "Public Data File"], "a": 0},
    {"id": "tec-60", "cat": "科技", "q": "「Git」主要用嚟做咩？", "opts": ["影像編輯", "版本控制", "音效處理", "繪圖"], "a": 1},
    {"id": "tec-61", "cat": "科技", "q": "「GitHub」係咩類型嘅平台？", "opts": ["社交網絡", "代碼托管／協作", "電商", "遊戲"], "a": 1},
    {"id": "tec-62", "cat": "科技", "q": "「API」全稱係咩？", "opts": ["Application Programming Interface", "Advanced Programming Interface", "Application Process Integration", "Automated Program Interface"], "a": 0},
    {"id": "tec-63", "cat": "科技", "q": "「JavaScript」主要運行喺邊個環境？", "opts": ["只係瀏覽器", "瀏覽器同 Node.js 等伺服器端", "只係伺服器", "只係手機 App"], "a": 1},
    {"id": "tec-64", "cat": "科技", "q": "「Python」以易讀同多用於邊類範疇聞名？", "opts": ["科學計算、AI 同數據分析", "純硬件編程", "純影視剪輯", "純遊戲機"], "a": 0},
    {"id": "tec-65", "cat": "科技", "q": "「虛擬實境」（VR）裝置例子包括？", "opts": ["Meta Quest", "Apple Vision Pro", "HTC Vive", "以上皆是"], "a": 3},
    {"id": "tec-66", "cat": "科技", "q": "「擴增實境」（AR）最常見嘅消費例子係？", "opts": ["Pokémon GO", "Microsoft Word", "PowerPoint", "Excel"], "a": 0},
    {"id": "tec-67", "cat": "科技", "q": "「比特幣」（Bitcoin）採用邊種底層技術？", "opts": ["雲計算", "區塊鏈", "大數據", "物聯網"], "a": 1},
    {"id": "tec-68", "cat": "科技", "q": "「物聯網」（IoT）全稱係？", "opts": ["Internet of Things", "Integration of Technology", "Intelligent Online Tools", "Internal Object Tracking"], "a": 0},
    {"id": "tec-69", "cat": "科技", "q": "「雲端運算」（Cloud Computing）邊間公司嘅平台最知名？", "opts": ["Amazon AWS", "Microsoft Azure", "Google Cloud", "以上皆是"], "a": 3},
    {"id": "tec-70", "cat": "科技", "q": "「機械學習」（Machine Learning）係邊個範疇嘅子集？", "opts": ["人工智能（AI）", "區塊鏈", "物聯網", "雲端"], "a": 0},
    {"id": "tec-71", "cat": "科技", "q": "「深度學習」（Deep Learning）主要用咩結構？", "opts": ["神經網絡", "邏輯樹", "關聯式數據庫", "排序演算法"], "a": 0},
    {"id": "tec-72", "cat": "科技", "q": "「Tesla」嘅自動駕駛系統叫咩名？", "opts": ["Autopilot", "Waymo", "Cruise", "BlueCruise"], "a": 0},

    # ===== 金融 (fin-37 to fin-72) =====
    {"id": "fin-37", "cat": "金融", "q": "「股票」代表咩？", "opts": ["公司嘅債務", "公司嘅擁有權一部分", "政府債券", "基金單位"], "a": 1},
    {"id": "fin-38", "cat": "金融", "q": "「債券」（Bond）代表咩？", "opts": ["公司擁有權", "借貸債務（債權）", "外匯", "期權"], "a": 1},
    {"id": "fin-39", "cat": "金融", "q": "「IPO」全稱係咩？", "opts": ["Initial Public Offering", "Internal Profit Operation", "Investment Portfolio Option", "International Public Offer"], "a": 0},
    {"id": "fin-40", "cat": "金融", "q": "「恆生指數」（Hang Seng Index）主要反映邊個市場？", "opts": ["東京", "香港", "新加坡", "上海"], "a": 1},
    {"id": "fin-41", "cat": "金融", "q": "「S&P 500」指數包含幾多間公司？", "opts": ["100", "500", "1000", "2000"], "a": 1},
    {"id": "fin-42", "cat": "金融", "q": "「道瓊斯工業平均指數」（Dow Jones）源於邊個國家？", "opts": ["美國", "英國", "日本", "香港"], "a": 0},
    {"id": "fin-43", "cat": "金融", "q": "「納斯達克」（NASDAQ）以邊類公司為主？", "opts": ["傳統工業", "科技同高成長公司", "房地產", "能源"], "a": 1},
    {"id": "fin-44", "cat": "金融", "q": "「外匯」（Forex）市場全球最大，每個交易日成交量以幾多計？", "opts": ["億美元", "萬億美元", "千億美元", "百億美元"], "a": 1},
    {"id": "fin-45", "cat": "金融", "q": "「MPF」全稱係咩？", "opts": ["Mandatory Provident Fund", "Mainland Provident Fund", "Mandatory Pension Fund", "Mainland Pension Fund"], "a": 0},
    {"id": "fin-46", "cat": "金融", "q": "「強積金」（MPF）係邊個地區嘅退休保障制度？", "opts": ["香港", "新加坡", "台灣", "澳門"], "a": 0},
    {"id": "fin-47", "cat": "金融", "q": "「聯繫匯率制度」下港幣盯住邊隻貨幣？", "opts": ["英鎊", "日圓", "美元", "人民幣"], "a": 2},
    {"id": "fin-48", "cat": "金融", "q": "「ETF」全稱係咩？", "opts": ["Exchange-Traded Fund", "Equity Trust Fund", "Exchange Transaction Fee", "Equity Trade Finance"], "a": 0},
    {"id": "fin-49", "cat": "金融", "q": "「REIT」係咩類型投資工具？", "opts": ["不動產投資信託基金", "純股票基金", "債券基金", "貨幣基金"], "a": 0},
    {"id": "fin-50", "cat": "金融", "q": "「對沖基金」（Hedge Fund）一般邊類投資者可以參與？", "opts": ["任何公眾", "合格投資者／機構", "只限政府", "只限銀行"], "a": 1},
    {"id": "fin-51", "cat": "金融", "q": "「PE」（Private Equity）係咩類型投資？", "opts": ["私募股權", "公開股權", "政府債券", "外匯"], "a": 0},
    {"id": "fin-52", "cat": "金融", "q": "「VC」（Venture Capital）主要投資邊類公司？", "opts": ["成熟大型公司", "初創／高成長公司", "只投資房地產", "只投資債券"], "a": 1},
    {"id": "fin-53", "cat": "金融", "q": "「股票回購」（Buyback）係指公司做咩？", "opts": ["賣出自己股票", "買返自己股票", "發行新股", "派發股息"], "a": 1},
    {"id": "fin-54", "cat": "金融", "q": "「派息」一般嚟講，股息係由邊度嚟？", "opts": ["公司利潤", "政府補貼", "銀行貸款", "投資者口袋"], "a": 0},
    {"id": "fin-55", "cat": "金融", "q": "「通脹」（Inflation）係指咩？", "opts": ["物價持續上升", "物價持續下跌", "失業率上升", "利率上升"], "a": 0},
    {"id": "fin-56", "cat": "金融", "q": "「通縮」（Deflation）係指咩？", "opts": ["物價持續上升", "物價持續下跌", "貨幣升值", "利率下跌"], "a": 1},
    {"id": "fin-57", "cat": "金融", "q": "「GDP」全稱係咩？", "opts": ["Gross Domestic Product", "General Domestic Production", "Global Domestic Product", "Gross Development Plan"], "a": 0},
    {"id": "fin-58", "cat": "金融", "q": "「CPI」全稱係咩？", "opts": ["Consumer Price Index", "Corporate Profit Index", "Consumer Product Index", "Cost Price Indicator"], "a": 0},
    {"id": "fin-59", "cat": "金融", "q": "「PMI」用嚟衡量邊樣嘢？", "opts": ["製造業／服務業景氣", "個人收入", "公司派息", "政府債務"], "a": 0},
    {"id": "fin-60", "cat": "金融", "q": "「聯儲局」（Federal Reserve）係邊個國家嘅央行？", "opts": ["美國", "英國", "歐盟", "日本"], "a": 0},
    {"id": "fin-61", "cat": "金融", "q": "「歐洲央行」（ECB）總部設喺邊個城市？", "opts": ["法蘭克福", "巴黎", "布魯塞爾", "盧森堡"], "a": 0},
    {"id": "fin-62", "cat": "金融", "q": "「日本央行」叫咩名？", "opts": ["BOJ（Bank of Japan）", "BEA", "FSA", "BOE"], "a": 0},
    {"id": "fin-63", "cat": "金融", "q": "「中國人民銀行」係邊個國家嘅央行？", "opts": ["中國", "香港", "台灣", "新加坡"], "a": 0},
    {"id": "fin-64", "cat": "金融", "q": "「SWIFT」主要用於咩？", "opts": ["國際銀行間結算", "本地 ATM 網絡", "信用卡支付", "股票買賣"], "a": 0},
    {"id": "fin-65", "cat": "金融", "q": "「LIBOR」曾經係全球最重要嘅咩利率基準？", "opts": ["銀行同業拆息", "信用卡利率", "個人房貸利率", "政府債券利率"], "a": 0},
    {"id": "fin-66", "cat": "金融", "q": "「美聯儲」加息通常會令到美元？", "opts": ["走強（升值）", "走弱（貶值）", "無影響", "波動性下降"], "a": 0},
    {"id": "fin-67", "cat": "金融", "q": "「牛市」（Bull Market）一般指？", "opts": ["市場下跌", "市場上升", "橫行", "波動劇烈"], "a": 1},
    {"id": "fin-68", "cat": "金融", "q": "「熊市」（Bear Market）一般指？", "opts": ["市場下跌", "市場上升", "橫行", "波動平靜"], "a": 0},
    {"id": "fin-69", "cat": "金融", "q": "「做空」（Short Selling）指投資者做咩？", "opts": ["買入期望升值", "先借貨再賣，期望跌價後平倉", "持有現金等跌", "只買指數"], "a": 1},
    {"id": "fin-70", "cat": "金融", "q": "「IPO」上市後，內部人士一般有咩限制？", "opts": ["完全自由買賣", "鎖定期（Lock-up Period）", "永久禁售", "只可賣不可買"], "a": 1},
    {"id": "fin-71", "cat": "金融", "q": "「家庭信託」（Family Trust）主要用嚟？", "opts": ["購買股票", "遺產規劃同資產保護", "外匯對沖", "純粹儲蓄"], "a": 1},
    {"id": "fin-72", "cat": "金融", "q": "「保險」最基本嘅原理係？", "opts": ["投資高回報", "集合多人分攤風險", "投機市場", "炒賣外匯"], "a": 1},
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