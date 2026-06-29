#!/usr/bin/env python3
"""Batch 4: 電影 (mov-37 to mov-72), 音樂 (mus-37 to mus-72)"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/alan9820/.openclaw/workspace/alan-yoshiki")
QUESTIONS_FILE = ROOT / "questions.json"

NEW_QUESTIONS = [
    # ===== 電影 (mov-37 to mov-72) =====
    {"id": "mov-37", "cat": "電影", "q": "《鐵達尼號》（Titanic）導演係邊個？", "opts": ["史匹堡", "卡梅隆 James Cameron", "諾蘭", "李安"], "a": 1},
    {"id": "mov-38", "cat": "電影", "q": "《鐵達尼號》入面飾演 Rose 嘅女演員係？", "opts": ["Kate Winslet", "Scarlett Johansson", "Nicole Kidman", "Emma Stone"], "a": 0},
    {"id": "mov-39", "cat": "電影", "q": "《哈利波特》系列電影飾演 Harry Potter 嘅演員係？", "opts": ["Daniel Radcliffe", "Rupert Grint", "Tom Felton", "Elijah Wood"], "a": 0},
    {"id": "mov-40", "cat": "電影", "q": "《魔戒》（Lord of the Rings）電影三部曲導演係？", "opts": ["Peter Jackson", "Steven Spielberg", "Christopher Nolan", "James Cameron"], "a": 0},
    {"id": "mov-41", "cat": "電影", "q": "《魔戒》入面要將「魔戒」丟入邊度先可以摧毀佢？", "opts": ["Mount Doom（末日火山）", "A black hole", "The Sun", "海底深淵"], "a": 0},
    {"id": "mov-42", "cat": "電影", "q": "《蜘蛛俠》嘅真名叫咩名？", "opts": ["Peter Parker", "Bruce Wayne", "Tony Stark", "Clark Kent"], "a": 0},
    {"id": "mov-43", "cat": "電影", "q": "《蝙蝠俠》（Batman）嘅真名叫咩名？", "opts": ["Peter Parker", "Bruce Wayne", "Tony Stark", "Clark Kent"], "a": 1},
    {"id": "mov-44", "cat": "電影", "q": "《Iron Man》嘅真名叫咩名？", "opts": ["Tony Stark", "Bruce Banner", "Peter Parker", "Steve Rogers"], "a": 0},
    {"id": "mov-45", "cat": "電影", "q": "《超人》（Superman）嘅真名叫咩名？", "opts": ["Clark Kent", "Bruce Wayne", "Peter Parker", "Tony Stark"], "a": 0},
    {"id": "mov-46", "cat": "電影", "q": "《美國隊長》嘅真名叫咩名？", "opts": ["Steve Rogers", "Tony Stark", "Bruce Banner", "Peter Parker"], "a": 0},
    {"id": "mov-47", "cat": "電影", "q": "《綠巨人浩克》嘅真名叫咩名？", "opts": ["Bruce Banner", "Tony Stark", "Peter Parker", "Steve Rogers"], "a": 0},
    {"id": "mov-48", "cat": "電影", "q": "Marvel 系列《Avengers》第一集上映年份？", "opts": ["2008 年", "2010 年", "2012 年", "2014 年"], "a": 2},
    {"id": "mov-49", "cat": "電影", "q": "《黑豹》（Black Panther）嘅真名叫咩名？", "opts": ["T'Challa", "Killmonger", "Shuri", "Okoye"], "a": 0},
    {"id": "mov-50", "cat": "電影", "q": "《星球大戰》（Star Wars）系列入面嘅天行者叫咩名？", "opts": ["Luke Skywalker", "Han Solo", "Yoda", "Darth Vader"], "a": 0},
    {"id": "mov-51", "cat": "電影", "q": "《星球大戰》嘅黑武士真名係？", "opts": ["Anakin Skywalker", "Luke Skywalker", "Obi-Wan", "Palpatine"], "a": 0},
    {"id": "mov-52", "cat": "電影", "q": "《E.T. 外星人》導演係邊個？", "opts": ["Steven Spielberg", "George Lucas", "James Cameron", "Ridley Scott"], "a": 0},
    {"id": "mov-53", "cat": "電影", "q": "《侏羅紀公園》入面主要展示咩動物？", "opts": ["機械人", "恐龍", "外星人", "古代魚"], "a": 1},
    {"id": "mov-54", "cat": "電影", "q": "《奪寶奇兵》（Indiana Jones）飾演 Indy 嘅演員係？", "opts": ["Harrison Ford", "Tom Cruise", "Brad Pitt", "Matt Damon"], "a": 0},
    {"id": "mov-55", "cat": "電影", "q": "《史力加》動畫電影系列由邊間公司製作？", "opts": ["Disney", "Pixar／DreamWorks", "Sony", "Universal"], "a": 1},
    {"id": "mov-56", "cat": "電影", "q": "《哈利波特》系列入面霍格華茲嘅校長叫？", "opts": ["麥教授", "天狼星", "鄧不利多 Dumbledore", "石內卜"], "a": 2},
    {"id": "mov-57", "cat": "電影", "q": "《變形金剛》（Transformers）主要係邊類機械人？", "opts": ["太空船", "汽車／機械人", "潛艇", "飛機"], "a": 1},
    {"id": "mov-58", "cat": "電影", "q": "《功夫熊貓》（Kung Fu Panda）主角叫咩名？", "opts": ["阿波 Po", "師父", "悍嬌虎", "阿龍"], "a": 0},
    {"id": "mov-59", "cat": "電影", "q": "《千與千尋》（Spirited Away）導演係？", "opts": ["宮崎駿", "新海誠", "細田守", "押井守"], "a": 0},
    {"id": "mov-60", "cat": "電影", "q": "《天氣之子》同《你的名字》嘅導演係？", "opts": ["新海誠 Makoto Shinkai", "宮崎駿", "是枝裕和", "北野武"], "a": 0},
    {"id": "mov-61", "cat": "電影", "q": "《七宗罪》（Se7en）導演係？", "opts": ["David Fincher", "Quentin Tarantino", "Christopher Nolan", "Martin Scorsese"], "a": 0},
    {"id": "mov-62", "cat": "電影", "q": "《低俗小說》（Pulp Fiction）導演係？", "opts": ["Quentin Tarantino", "David Fincher", "Coen Brothers", "Martin Scorsese"], "a": 0},
    {"id": "mov-63", "cat": "電影", "q": "《上游》（Inception）導演係？", "opts": ["Christopher Nolan", "Denis Villeneuve", "Ridley Scott", "James Cameron"], "a": 0},
    {"id": "mov-64", "cat": "電影", "q": "《上流寄生族》（Parasite）係邊個國家嘅電影？", "opts": ["韓國", "日本", "中國", "泰國"], "a": 0},
    {"id": "mov-65", "cat": "電影", "q": "《上流寄生族》導演係邊個？", "opts": ["奉俊昊 Bong Joon-ho", "朴贊郁", "李滄東", "是枝裕和"], "a": 0},
    {"id": "mov-66", "cat": "電影", "q": "《花木蘭》（2020 真人版）花木蘭嘅飾演者係？", "opts": ["劉亦菲", "章子怡", "范冰冰", "楊紫瓊"], "a": 0},
    {"id": "mov-67", "cat": "電影", "q": "《卧虎藏龍》導演係邊個？", "opts": ["李安 Ang Lee", "張藝謀", "陳凱歌", "王家衛"], "a": 0},
    {"id": "mov-68", "cat": "電影", "q": "《英雄》（2002）導演係邊個？", "opts": ["張藝謀", "李安", "陳凱歌", "王家衛"], "a": 0},
    {"id": "mov-69", "cat": "電影", "q": "《一個人的武林》係邊類型港產片？", "opts": ["文藝片", "武打動作片", "恐怖片", "愛情片"], "a": 1},
    {"id": "mov-70", "cat": "電影", "q": "《無間道》係邊年出品嘅港產片？", "opts": ["2000 年", "2002 年", "2004 年", "2008 年"], "a": 1},
    {"id": "mov-71", "cat": "電影", "q": "《英雄本色》飾演「小馬哥」嘅演員係？", "opts": ["周潤發", "周星馳", "張國榮", "梁朝偉"], "a": 0},
    {"id": "mov-72", "cat": "電影", "q": "「奧斯卡金像獎」英文叫？", "opts": ["Academy Awards / Oscars", "Golden Globe", "BAFTA", "Cannes"], "a": 0},

    # ===== 音樂 (mus-37 to mus-72) =====
    {"id": "mus-37", "cat": "音樂", "q": "「鋼琴」一般有幾多個鍵？", "opts": ["76", "82", "88", "100"], "a": 2},
    {"id": "mus-38", "cat": "音樂", "q": "「小提琴」有幾多條弦？", "opts": ["3", "4", "5", "6"], "a": 1},
    {"id": "mus-39", "cat": "音樂", "q": "「結他」（Guitar）一般有幾多條弦（標準）？", "opts": ["4", "5", "6", "7"], "a": 2},
    {"id": "mus-40", "cat": "音樂", "q": "以下邊個係古典音樂作曲家？", "opts": ["莫扎特 Mozart", "Taylor Swift", "Ed Sheeran", "Drake"], "a": 0},
    {"id": "mus-41", "cat": "音樂", "q": "「貝多芬」最著名嘅交響曲邊首？", "opts": ["第五號（命運）", "第一號", "第九號（合唱）", "第七號"], "a": 0},
    {"id": "mus-42", "cat": "音樂", "q": "「莫扎特」係邊國作曲家？", "opts": ["德國", "奧地利", "意大利", "法國"], "a": 1},
    {"id": "mus-43", "cat": "音樂", "q": "「蕭邦」（Chopin）係邊國作曲家？", "opts": ["德國", "波蘭", "匈牙利", "奧地利"], "a": 1},
    {"id": "mus-44", "cat": "音樂", "q": "「柴可夫斯基」主要作品包括？", "opts": ["天鵝湖", "魔笛", "土耳其進行曲", "悲愴奏鳴曲"], "a": 0},
    {"id": "mus-45", "cat": "音樂", "q": "「鄧麗君」係邊個地方嘅歌手？", "opts": ["香港", "台灣", "日本", "B 同 C 都對"], "a": 3},
    {"id": "mus-46", "cat": "音樂", "q": "「張國榮」嘅代表作有咩？", "opts": ["Monica", "K 歌之王", "十年", "滄海一聲笑"], "a": 0},
    {"id": "mus-47", "cat": "音樂", "q": "「梅艷芳」嘅代表作有咩？", "opts": ["似水流年", "壞女孩", "夕陽之歌", "B 同 C 都對"], "a": 3},
    {"id": "mus-48", "cat": "音樂", "q": "「陳奕迅」嘅代表作有咩？", "opts": ["十年", "K 歌之王", "富士山下", "以上皆是"], "a": 3},
    {"id": "mus-49", "cat": "音樂", "q": "「Twins」組合成員係邊兩位？", "opts": ["蔡卓妍同鍾欣潼", "容祖兒同楊千嬅", "謝霆鋒同陳奕迅", "林夕同黃偉文"], "a": 0},
    {"id": "mus-50", "cat": "音樂", "q": "「Beatles」係邊國樂隊？", "opts": ["美國", "英國", "愛爾蘭", "加拿大"], "a": 1},
    {"id": "mus-51", "cat": "音樂", "q": "「Beatles」核心成員包括以下邊位？", "opts": ["John Lennon", "Mick Jagger", "David Bowie", "Freddie Mercury"], "a": 0},
    {"id": "mus-52", "cat": "音樂", "q": "「Queen」樂隊主唱叫咩名？", "opts": ["Freddie Mercury", "Brian May", "Roger Taylor", "John Deacon"], "a": 0},
    {"id": "mus-53", "cat": "音樂", "q": "「Bohemian Rhapsody」係邊個樂隊嘅歌？", "opts": ["Queen", "Beatles", "Pink Floyd", "Led Zeppelin"], "a": 0},
    {"id": "mus-54", "cat": "音樂", "q": "「Adele」係邊國歌手？", "opts": ["美國", "英國", "澳洲", "加拿大"], "a": 1},
    {"id": "mus-55", "cat": "音樂", "q": "「Taylor Swift」係邊國歌手？", "opts": ["美國", "英國", "加拿大", "澳洲"], "a": 0},
    {"id": "mus-56", "cat": "音樂", "q": "「BTS」係邊國男子組合？", "opts": ["日本", "韓國", "中國", "泰國"], "a": 1},
    {"id": "mus-57", "cat": "音樂", "q": "「BLACKPINK」係邊間公司旗下女子組合？", "opts": ["SM", "JYP", "YG", "HYBE"], "a": 2},
    {"id": "mus-58", "cat": "音樂", "q": "「周杰倫」係邊個地方嘅歌手？", "opts": ["香港", "台灣", "中國大陸", "新加坡"], "a": 1},
    {"id": "mus-59", "cat": "音樂", "q": "「周杰倫」嘅代表作有咩？", "opts": ["青花瓷", "稻香", "晴天", "以上皆是"], "a": 3},
    {"id": "mus-60", "cat": "音樂", "q": "「容祖兒」嘅代表作有咩？", "opts": ["揮著翅膀的女孩", "痛愛", "心之焰", "以上皆是"], "a": 3},
    {"id": "mus-61", "cat": "音樂", "q": "「C 調」喺音階上係邊個音？", "opts": ["Do", "Re", "Mi", "Fa"], "a": 0},
    {"id": "mus-62", "cat": "音樂", "q": "「五線譜」上面有幾條線？", "opts": ["3", "4", "5", "6"], "a": 2},
    {"id": "mus-63", "cat": "音樂", "q": "「指揮家」通常喺樂團中負責咩？", "opts": ["獨奏", "控制整體節奏同演繹", "後勤", "樂器維修"], "a": 1},
    {"id": "mus-64", "cat": "音樂", "q": "「香港管弦樂團」英文簡稱係？", "opts": ["HKPO", "HK Phil", "HKSymphony", "HKOrch"], "a": 1},
    {"id": "mus-65", "cat": "音樂", "q": "「聯合國國歌」嘅曲主要源自邊首樂曲？", "opts": ["貝多芬第九號交響曲（快樂頌）", "莫扎特安魂曲", "蕭邦夜曲", "巴哈 G 弦之歌"], "a": 0},
    {"id": "mus-66", "cat": "音樂", "q": "「Hip Hop」文化廣義上起源於邊個國家？（70 年代）", "opts": ["美國（紐約 Bronx）", "牙買加", "古巴", "巴西"], "a": 0},
    {"id": "mus-67", "cat": "音樂", "q": "「Rapper」通常係指邊類音樂人？", "opts": ["饒舌／說唱歌手", "歌劇歌手", "DJ", "Bassist"], "a": 0},
    {"id": "mus-68", "cat": "音樂", "q": "「廣東歌」入面，「K 歌之王」係邊個歌手嘅代表作？", "opts": ["陳奕迅", "張學友", "劉德華", "黎明"], "a": 0},
    {"id": "mus-69", "cat": "音樂", "q": "以下邊位唔係 1990 年代「香港四大天王」之一？", "opts": ["張學友", "劉德華", "譚詠麟", "郭富城"], "a": 2},
    {"id": "mus-70", "cat": "音樂", "q": "「王菲」嘅代表作有咩？", "opts": ["紅豆", "容易受傷的女人", "執迷不悔", "以上皆是"], "a": 3},
    {"id": "mus-71", "cat": "音樂", "q": "「林夕」係邊個領域嘅代表人物？", "opts": ["粵語流行曲填詞人", "電影導演", "畫家", "演員"], "a": 0},
    {"id": "mus-72", "cat": "音樂", "q": "「黃偉文」係咩身份？", "opts": ["粵語流行曲填詞人", "歌手", "DJ", "鋼琴家"], "a": 0},
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