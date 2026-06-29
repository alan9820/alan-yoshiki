#!/usr/bin/env python3
"""Batch 3: 卡通 (cart-34 to cart-65), 食物 (food-37 to food-72)"""
import json
import sys
from pathlib import Path

ROOT = Path("/home/alan9820/.openclaw/workspace/alan-yoshiki")
QUESTIONS_FILE = ROOT / "questions.json"

NEW_QUESTIONS = [
    # ===== 卡通 (cart-34 to cart-65) =====
    {"id": "cart-34", "cat": "卡通", "q": "《鬼滅之刃》主角叫咩名？", "opts": ["炭治郎", "善逸", "伊之助", "義勇"], "a": 0},
    {"id": "cart-35", "cat": "卡通", "q": "《鬼滅之刃》入面炭治郎嘅家人（除妹妹）喺故事開始時畀邊個殺？", "opts": ["鬼", "鬼舞辻無慘", "蜘蛛山嘅鬼", "下弦之鬼"], "a": 1},
    {"id": "cart-36", "cat": "卡通", "q": "《進擊嘅巨人》主角叫咩名？", "opts": ["艾倫 Yeager", "米卡莎", "阿爾敏", "里維"], "a": 0},
    {"id": "cart-37", "cat": "卡通", "q": "《海賊王》入面「草帽海賊團」嘅船醫係邊個？", "opts": ["索隆", "娜美", "托尼托尼·喬巴", "騙人布"], "a": 2},
    {"id": "cart-38", "cat": "卡通", "q": "《海賊王》入面嘅「羅」全名係？", "opts": ["羅羅諾亞·索隆", "羅傑", "羅（Trafalgar Law）", "貝克曼"], "a": 2},
    {"id": "cart-39", "cat": "卡通", "q": "《龍珠》主角叫咩名？", "opts": ["達爾", "悟空", "比克", "菲利"], "a": 1},
    {"id": "cart-40", "cat": "卡通", "q": "《龍珠 Z》入面悟空變身後叫「超級撒亞人」，變身觸發多數因為咩？", "opts": ["食咗仙豆", "朋友被殺", "練功", "見到月亮"], "a": 1},
    {"id": "cart-41", "cat": "卡通", "q": "《火影忍者》主角鳴人嘅尾獸封印係邊隻？", "opts": ["一尾", "三尾", "九尾", "零尾"], "a": 2},
    {"id": "cart-42", "cat": "卡通", "q": "《火影忍者》入面鳴人嘅死敵兼朋友叫咩名？", "opts": ["佐助", "卡卡西", "自來也", "我愛羅"], "a": 0},
    {"id": "cart-43", "cat": "卡通", "q": "《蠟筆小新》主角小新嘅姓係咩？", "opts": ["野原", "櫻田", "松坂", "風間"], "a": 0},
    {"id": "cart-44", "cat": "卡通", "q": "《櫻桃小丸子》主角嘅全名係？", "opts": ["櫻桃子", "丸尾", "小玉", "花輪"], "a": 0},
    {"id": "cart-45", "cat": "卡通", "q": "《名偵探柯南》主角嘅真名係？", "opts": ["工藤新一", "服部平次", "毛利小五郎", "灰原哀"], "a": 0},
    {"id": "cart-46", "cat": "卡通", "q": "《名偵探柯南》入面邊個係經常被麻醉嘅大叔？", "opts": ["毛利小五郎", "阿笠博士", "鈴木園子", "目暮警官"], "a": 0},
    {"id": "cart-47", "cat": "卡通", "q": "《多啦A夢》大雄嘅朋友入面，好打但常常輸嘅叫？", "opts": ["靜香", "胖虎", "小夫", "出木杉"], "a": 1},
    {"id": "cart-48", "cat": "卡通", "q": "《多啦A夢》嘅道具「隨意門」（任意門）可以點用？", "opts": ["去任何地方", "變出食物", "時間旅行", "召喚精靈"], "a": 0},
    {"id": "cart-49", "cat": "卡通", "q": "《寵物小精靈》（寶可夢）主角叫咩名？", "opts": ["小智", "小茂", "小剛", "皮卡丘"], "a": 0},
    {"id": "cart-50", "cat": "卡通", "q": "《寵物小精靈》入面，最經典嘅「皮卡丘」屬於邊類？", "opts": ["火", "水", "電", "草"], "a": 2},
    {"id": "cart-51", "cat": "卡通", "q": "《足球小將》主角叫咩名？", "opts": ["大空翼", "日向小次郎", "若林源三", "岬太郎"], "a": 0},
    {"id": "cart-52", "cat": "卡通", "q": "《閃電傳真機》唔係以下邊套作品嘅角色？", "opts": ["足球小將", "足球小將翼", "閃電十一人", "閃電傳真機"], "a": 2},
    {"id": "cart-53", "cat": "卡通", "q": "《史力加》（Shrek）主角係咩生物？", "opts": ["王子", "巨魔 ogre", "龍", "巫師"], "a": 1},
    {"id": "cart-54", "cat": "卡通", "q": "《反斗奇兵》（Toy Story）入面，主角Andy最鍾意嘅牛仔公仔叫？", "opts": ["巴斯光年", "胡迪", "抱抱龍", "三眼仔"], "a": 1},
    {"id": "cart-55", "cat": "卡通", "q": "《米奇老鼠》（Mickey Mouse）邊間公司創造？", "opts": ["華納兄弟", "迪士尼", "夢工廠", "環球"], "a": 1},
    {"id": "cart-56", "cat": "卡通", "q": "《冰雪奇緣》（Frozen）主角姊妹分別叫？", "opts": ["Anna 同 Elsa", "Belle 同 Ariel", "Cinderella 同 Aurora", "Moana 同 Rapunzel"], "a": 0},
    {"id": "cart-57", "cat": "卡通", "q": "《史諾比》（Snoopy）出自邊套漫畫？", "opts": ["花生漫畫 Peanuts", "加菲貓", "史力加", "湯姆貓與傑利鼠"], "a": 0},
    {"id": "cart-58", "cat": "卡通", "q": "《加菲貓》最鍾意食咩？", "opts": ["壽司", "意大利粉 lasagna", "漢堡包", "壽司卷"], "a": 1},
    {"id": "cart-59", "cat": "卡通", "q": "《湯姆貓與傑利鼠》（Tom and Jerry）入面傑利係咩動物？", "opts": ["貓", "狗", "老鼠", "鴨"], "a": 2},
    {"id": "cart-60", "cat": "卡通", "q": "《超人特攻隊》（The Incredibles）嘅主角爸爸叫咩名？", "opts": ["Bob Parr", "Homer", "Peter", "Stan"], "a": 0},
    {"id": "cart-61", "cat": "卡通", "q": "《獵人》（HUNTER×HUNTER）主角叫咩名？", "opts": ["小傑", "奇犽", "雷歐力", "酷拉皮卡"], "a": 0},
    {"id": "cart-62", "cat": "卡通", "q": "《排球少年》主角所屬嘅高中球隊叫？", "opts": ["烏野高中", "青葉城西", "白鳥澤", "音駒"], "a": 0},
    {"id": "cart-63", "cat": "卡通", "q": "《咒術迴戰》主角叫咩名？", "opts": ["虎杖悠仁", "伏黑惠", "釘崎野薔薇", "五條悟"], "a": 0},
    {"id": "cart-64", "cat": "卡通", "q": "《天竺鼠車車》（Pui Pui Molcar）邊個國家製作？", "opts": ["日本", "韓國", "中國", "台灣"], "a": 0},
    {"id": "cart-65", "cat": "卡通", "q": "《天竺鼠車車》入面嘅角色其實係咩？", "opts": ["天竺鼠造型嘅車", "真嘅天竺鼠", "機械人", "飛船"], "a": 0},

    # ===== 食物 (food-37 to food-72) =====
    {"id": "food-37", "cat": "食物", "q": "「叉燒」屬於邊類菜式？", "opts": ["京菜", "粵菜", "川菜", "淮揚菜"], "a": 1},
    {"id": "food-38", "cat": "食物", "q": "「老婆餅」傳統上屬於邊地食品？", "opts": ["上海", "廣東", "台灣", "四川"], "a": 1},
    {"id": "food-39", "cat": "食物", "q": "「蛋撻」起源地最廣為人知嘅係邊度？", "opts": ["葡萄牙", "香港（受葡式影響）", "法國", "英國"], "a": 1},
    {"id": "food-40", "cat": "食物", "q": "「雲吞麵」係邊地代表食物？", "opts": ["上海", "香港／廣東", "四川", "北京"], "a": 1},
    {"id": "food-41", "cat": "食物", "q": "「咖喱魚蛋」係香港邊類食品代表？", "opts": ["酒樓菜", "街頭小食", "高級餐廳", "甜品"], "a": 1},
    {"id": "food-42", "cat": "食物", "q": "「絲襪奶茶」係邊度發明？", "opts": ["台灣", "香港", "澳門", "廣州"], "a": 1},
    {"id": "food-43", "cat": "食物", "q": "「菠萝油」（菠蘿包）入面通常夾住咩食？", "opts": ["牛油", "蛋黃醬", "芝士", "花生醬"], "a": 0},
    {"id": "food-44", "cat": "食物", "q": "「車厘子」英文係？", "opts": ["Cherry", "Strawberry", "Blueberry", "Plum"], "a": 0},
    {"id": "food-45", "cat": "食物", "q": "「奇異果」原產地喺邊？", "opts": ["澳洲", "紐西蘭", "中國", "南美"], "a": 2},
    {"id": "food-46", "cat": "食物", "q": "「士多啤梨」英文係？", "opts": ["Strawberry", "Cherry", "Peach", "Grape"], "a": 0},
    {"id": "food-47", "cat": "食物", "q": "「藍莓」英文係？", "opts": ["Blueberry", "Blackberry", "Cranberry", "Raspberry"], "a": 0},
    {"id": "food-48", "cat": "食物", "q": "「番茄」植物學上屬於邊類？", "opts": ["水果", "蔬菜", "穀物", "豆類"], "a": 0},
    {"id": "food-49", "cat": "食物", "q": "「韓式燒烤」嘅肉類通常用咩醃製？", "opts": ["咖喱", "醬油、糖、蒜、芝麻油", "沙嗲", "XO 醬"], "a": 1},
    {"id": "food-50", "cat": "食物", "q": "「壽司」嘅主要材料除咗飯仲有咩？", "opts": ["麵粉", "醋飯加海鮮／配料", "椰漿", "牛奶"], "a": 1},
    {"id": "food-51", "cat": "食物", "q": "「三文魚」英文係？", "opts": ["Salmon", "Tuna", "Cod", "Sardine"], "a": 0},
    {"id": "food-52", "cat": "食物", "q": "「吞拿魚」英文係？", "opts": ["Tuna", "Salmon", "Mackerel", "Herring"], "a": 0},
    {"id": "food-53", "cat": "食物", "q": "「拉麵」一般源自邊國？", "opts": ["中國（後傳日本）", "韓國", "泰國", "越南"], "a": 0},
    {"id": "food-54", "cat": "食物", "q": "「天婦羅」係邊國菜？", "opts": ["中國", "日本", "韓國", "泰國"], "a": 1},
    {"id": "food-55", "cat": "食物", "q": "「冬蔭功」湯係邊國菜？", "opts": ["越南", "泰國", "馬來西亞", "緬甸"], "a": 1},
    {"id": "food-56", "cat": "食物", "q": "「海南雞飯」發源地一般認為喺邊？", "opts": ["海南", "新加坡／馬來西亞", "泰國", "印尼"], "a": 1},
    {"id": "food-57", "cat": "食物", "q": "「越南河粉」英文叫？", "opts": ["Pho", "Ramen", "Pad Thai", "Dim Sum"], "a": 0},
    {"id": "food-58", "cat": "食物", "q": "「Pad Thai」係邊國菜？", "opts": ["泰國", "越南", "馬來西亞", "印尼"], "a": 0},
    {"id": "food-59", "cat": "食物", "q": "「韓式拌飯」叫咩名？", "opts": ["Bibimbap", "Kimchi", "Bulgogi", "Tteokbokki"], "a": 0},
    {"id": "food-60", "cat": "食物", "q": "「Kimchi」係咩？", "opts": ["韓式泡菜", "韓式燒肉", "韓式飯卷", "韓式辣醬"], "a": 0},
    {"id": "food-61", "cat": "食物", "q": "「意大利薄餅」英文叫？", "opts": ["Pizza", "Pasta", "Risotto", "Lasagna"], "a": 0},
    {"id": "food-62", "cat": "食物", "q": "「意大利粉」英文叫？", "opts": ["Pasta", "Bread", "Rice", "Soup"], "a": 0},
    {"id": "food-63", "cat": "食物", "q": "「千層麵」英文係？", "opts": ["Lasagna", "Pizza", "Ravioli", "Gnocchi"], "a": 0},
    {"id": "food-64", "cat": "食物", "q": "「法式長棍麵包」叫咩名？", "opts": ["Baguette", "Croissant", "Brioche", "Focaccia"], "a": 0},
    {"id": "food-65", "cat": "食物", "q": "「牛角包」英文係？", "opts": ["Croissant", "Baguette", "Pretzel", "Donut"], "a": 0},
    {"id": "food-66", "cat": "食物", "q": "「芝士」英文係？", "opts": ["Cheese", "Butter", "Cream", "Yogurt"], "a": 0},
    {"id": "food-67", "cat": "食物", "q": "「英式早餐茶」最常配邊樣嘢？", "opts": ["咖啡", "牛奶", "檸檬", "蜂蜜"], "a": 1},
    {"id": "food-68", "cat": "食物", "q": "「朱古力」英文係？", "opts": ["Chocolate", "Caramel", "Vanilla", "Candy"], "a": 0},
    {"id": "food-69", "cat": "食物", "q": "「抹茶」源自邊國？", "opts": ["中國（後傳日本）", "韓國", "印度", "日本原生"], "a": 0},
    {"id": "food-70", "cat": "食物", "q": "「臭豆腐」最常見嘅產地喺邊？", "opts": ["湖南／台灣", "四川", "北京", "上海"], "a": 0},
    {"id": "food-71", "cat": "食物", "q": "「四川」名菜「麻婆豆腐」嘅「麻」主要嚟自邊種調味料？", "opts": ["辣椒", "花椒", "胡椒", "八角"], "a": 1},
    {"id": "food-72", "cat": "食物", "q": "「北京」名菜「北京填鴨」主要食邊部分？", "opts": ["全隻烤", "皮", "肉", "骨"], "a": 1},
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