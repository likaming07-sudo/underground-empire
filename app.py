from flask import Flask, request, jsonify, render_template
from google import genai
import os
import json
import random
import time

app = Flask(__name__)

# ============================================================
# Gemini
# ============================================================

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("⚠️ 尚未設定 GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY) if API_KEY else None

MODEL = "gemini-3.5-flash"


# ============================================================
# Gemini 呼叫器
# ============================================================

def call_gemini(
    prompt,
    system_instruction,
    json_mode=False,
    max_retries=5
):

    if not client:
        raise RuntimeError("尚未設定 GEMINI_API_KEY")

    for attempt in range(max_retries):

        try:

            config = {
                "system_instruction": system_instruction,
                "temperature": 0.9
            }

            if json_mode:
                config["response_mime_type"] = "application/json"

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config
            )

            if not response.text:
                raise RuntimeError("Gemini 沒有返回文字")

            return response.text.strip()

        except Exception as e:

            error_text = str(e)

            temporary_error = (
                "503" in error_text
                or "429" in error_text
                or "500" in error_text
                or "UNAVAILABLE" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if not temporary_error:
                raise

            wait_time = min(
                2 ** attempt,
                20
            )

            time.sleep(wait_time)

    raise RuntimeError(
        "Gemini 目前無法使用，請稍後再試。"
    )


# ============================================================
# 新遊戲
# ============================================================

def new_game():

    return {

        "player": {

            "name": "你",
            "age": 18,
            "month": 1,

            "cash": 0,
            "assets": 0,
            "company_value": 0,

            "legal_business": 0,
            "power": 0,
            "reputation": 0,

            "police_attention": 0,
            "health": 100,

            "alive": True,
            "arrested": False,
            "listed": False
        },

        "brothers": {

            "阿龍": {

                "age": 18,
                "loyalty": 88,
                "trust": 80,
                "ability": 65,

                "alive": True,

                "personality":
                    "沉穩、重義氣、保護兄弟",

                "relationship":
                    "從小一起長大的兄弟"
            },

            "阿虎": {

                "age": 18,
                "loyalty": 78,
                "trust": 70,
                "ability": 75,

                "alive": True,

                "personality":
                    "衝動、好勝、敢冒險",

                "relationship":
                    "從小一起長大的兄弟"
            },

            "阿豪": {

                "age": 18,
                "loyalty": 92,
                "trust": 85,
                "ability": 58,

                "alive": True,

                "personality":
                    "冷靜、聰明、擅長分析",

                "relationship":
                    "從小一起長大的兄弟"
            }
        },

        "love_interest": None,

        "npcs": {},

        "world": {

            "location": "台灣",
            "year": 2026,
            "month": 1,

            "factions": [],
            "allies": [],
            "enemies": [],
            "news": []
        },

        "flags": [],

        "history": []
    }


# ============================================================
# Game Master
# ============================================================

SYSTEM_PROMPT = r"""
你是「地下帝國：AI人生」的遊戲主持人。

這是一個長篇虛構人生 RPG。

玩家18歲開始。

玩家出生於台灣。

玩家初始：

現金 0
資產 0
勢力 0

玩家有三個兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。

==================================================
核心規則
==================================================

每個月是一回合。

每回合必須：

1. 發生一件合理事件。
2. 有劇情。
3. NPC 有自然對話。
4. NPC 有自己的性格與利益。
5. NPC 能根據過去事件改變態度。
6. 世界不會只圍著玩家轉。
7. 給玩家三個建議選項。
8. 玩家也可以完全自由行動。

三個選項不是限制。

不要替玩家做重大決定。

不要替玩家說話。

不要替玩家決定玩家真正想做什麼。

玩家輸入的自由行動才是玩家的真正決定。

==================================================
人物
==================================================

NPC 必須像真人。

重要 NPC 可以有：

性格
利益
恐懼
目標
秘密
對玩家的看法

NPC 可以：

拒絕玩家
幫助玩家
欺騙玩家
嫉妒玩家
離開玩家
與玩家合作
與玩家發生衝突

==================================================
三兄弟
==================================================

三兄弟不是工具人。

他們有自己的想法。

玩家做出他們不能接受的事情：

可能降低信任。
可能降低忠誠。
可能發生爭吵。

玩家保護兄弟：

可能增加忠誠。

兄弟也可以自己提出建議。

==================================================
戀愛
==================================================

戀愛角色不是單純數值。

戀愛角色有：

性格
夢想
生活
朋友
家庭
底線
喜好
討厭的事情

戀愛角色可以主動找玩家。

如果玩家欺騙對方：

信任下降。

如果玩家忽略對方：

關係可能變淡。

==================================================
世界
==================================================

世界會自己發展。

可能出現：

商人
企業家
警察
律師
記者
投資人
競爭者
朋友
敵人
普通市民
地方人物
公司
合法企業
地下勢力

其他 NPC 也可能互相合作、競爭或發生變化。

==================================================
人生
==================================================

玩家可能：

賺錢
失敗
破產
建立公司
發展合法事業
建立勢力
戀愛
失戀
結婚
被捕
退出地下世界
讓公司上市

==================================================
劇情風格
==================================================

像長篇犯罪／商業／人生影集。

不要每個月都是大事件。

事件大小要有變化。

可以出現：

日常
兄弟聚會
家庭
學習
工作
商業
投資
公司發展
感情
社會新聞
警方調查
媒體
競爭者

犯罪內容只能是虛構劇情與抽象結果。

不要提供現實世界可直接執行的犯罪方法。

不要提供武器製造、毒品製造、洗錢、逃避警方追查等實際操作。

==================================================
輸出格式
==================================================

【劇情】

約 500～800 字。

不要過度冗長。

要有自然對話。

【目前狀況】

約 3～5 行。

【你的選擇】

1. xxx
2. xxx
3. xxx

【自由行動】

玩家可以完全自由輸入。

再次提醒：

3個選項不是限制。
"""


# ============================================================
# 生成劇情
# ============================================================

def generate_story(state):

    recent_history = state["history"][-6:]

    data = {

        "game_state": {

            "player": state["player"],

            "brothers": state["brothers"],

            "love_interest":
                state["love_interest"],

            "flags":
                state["flags"],

            "recent_history":
                recent_history
        },

        "task":
            "請生成這個月的新事件與劇情。"
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    return call_gemini(
        prompt,
        SYSTEM_PROMPT
    )


# ============================================================
# 行動結果
# ============================================================

RESULT_PROMPT = r"""
你現在是「地下帝國：AI人生」的劇情裁判。

玩家剛剛做了一個行動。

根據：

1. 玩家目前狀態
2. 最近歷史
3. 本月事件
4. 玩家行動

決定合理的劇情結果。

不要讓玩家自動成功。

玩家可能：

成功
部分成功
失敗
遇到意外
改變 NPC 關係
造成未來伏筆

不要替玩家做下一個重大決定。

不要直接讓玩家突然成為世界首富。

結果約 300～600 字。

只描述故事結果。

犯罪相關內容只能停留在虛構、抽象層次。
"""


def resolve_action(
    state,
    action,
    current_story
):

    recent_history = state["history"][-6:]

    data = {

        "game_state": {

            "player": state["player"],

            "brothers": state["brothers"],

            "love_interest":
                state["love_interest"],

            "flags":
                state["flags"],

            "recent_history":
                recent_history
        },

        "current_story":
            current_story,

        "player_action":
            action
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    return call_gemini(
        prompt,
        RESULT_PROMPT
    )


# ============================================================
# 數值判定
# ============================================================

STATE_PROMPT = r"""
你是 RPG 遊戲數值判定器。

根據玩家行動與劇情結果，
判斷合理的數值變化。

只輸出 JSON。

不要輸出任何其他文字。

JSON：

{
 "cash_change": 0,
 "assets_change": 0,
 "company_value_change": 0,
 "legal_business_change": 0,
 "power_change": 0,
 "reputation_change": 0,
 "police_attention_change": 0,
 "health_change": 0,

 "brothers": {
   "阿龍": {
     "loyalty_change": 0,
     "trust_change": 0
   },
   "阿虎": {
     "loyalty_change": 0,
     "trust_change": 0
   },
   "阿豪": {
     "loyalty_change": 0,
     "trust_change": 0
   }
 },

 "love": {
   "affection_change": 0,
   "trust_change": 0
 },

 "new_flags": [],
 "remove_flags": [],

 "death": false,
 "arrested": false,
 "listed": false
}

普通事件不要突然增加大量金錢。

不要突然讓玩家增加大量勢力。

重大事件才允許大幅變化。

所有變化必須符合劇情。

所有數值變化盡量控制在 -10 到 +10。

特殊重大事件才可以超過。

health 0～100。

police_attention 0～100。

兄弟 loyalty 0～100。

兄弟 trust 0～100。

戀愛 affection 0～100。

戀愛 trust 0～100。
"""


def calculate_changes(
    state,
    action,
    story
):

    data = {

        "player":
            state["player"],

        "brothers": {

            name: {

                "loyalty":
                    b["loyalty"],

                "trust":
                    b["trust"],

                "alive":
                    b["alive"]

            }

            for name, b
            in state["brothers"].items()
        },

        "love_interest":
            state["love_interest"],

        "player_action":
            action,

        "story_result":
            story
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    text = call_gemini(
        prompt,
        STATE_PROMPT,
        json_mode=True
    )

    text = text.replace(
        "```json",
        ""
    ).replace(
        "```",
        ""
    ).strip()

    try:

        return json.loads(text)

    except Exception:

        return {}


# ============================================================
# 套用數值
# ============================================================

def apply_changes(
    state,
    changes
):

    p = state["player"]

    fields = [

        "cash",
        "assets",
        "company_value",
        "legal_business",
        "power",
        "reputation",
        "police_attention",
        "health"
    ]

    for field in fields:

        key = field + "_change"

        value = changes.get(
            key,
            0
        )

        if isinstance(
            value,
            (int, float)
        ):

            value = max(
                -1000000,
                min(
                    1000000,
                    value
                )
            )

            p[field] += value

    p["cash"] = max(
        0,
        p["cash"]
    )

    p["assets"] = max(
        0,
        p["assets"]
    )

    p["company_value"] = max(
        0,
        p["company_value"]
    )

    p["legal_business"] = max(
        0,
        min(
            100,
            p["legal_business"]
        )
    )

    p["power"] = max(
        0,
        p["power"]
    )

    p["reputation"] = max(
        0,
        p["reputation"]
    )

    p["police_attention"] = max(
        0,
        min(
            100,
            p["police_attention"]
        )
    )

    p["health"] = max(
        0,
        min(
            100,
            p["health"]
        )
    )

    # 兄弟

    brothers = changes.get(
        "brothers",
        {}
    )

    for name, data in brothers.items():

        if name not in state["brothers"]:
            continue

        b = state["brothers"][name]

        b["loyalty"] += data.get(
            "loyalty_change",
            0
        )

        b["trust"] += data.get(
            "trust_change",
            0
        )

        b["loyalty"] = max(
            0,
            min(
                100,
                b["loyalty"]
            )
        )

        b["trust"] = max(
            0,
            min(
                100,
                b["trust"]
            )
        )

    # 戀愛

    love = state["love_interest"]

    if love:

        love_data = changes.get(
            "love",
            {}
        )

        love["affection"] += love_data.get(
            "affection_change",
            0
        )

        love["trust"] += love_data.get(
            "trust_change",
            0
        )

        love["affection"] = max(
            0,
            min(
                100,
                love["affection"]
            )
        )

        love["trust"] = max(
            0,
            min(
                100,
                love["trust"]
            )
        )

        affection = love["affection"]

        if affection < 20:
            love["relationship"] = "陌生"

        elif affection < 40:
            love["relationship"] = "朋友"

        elif affection < 60:
            love["relationship"] = "曖昧"

        elif affection < 80:
            love["relationship"] = "交往"

        elif affection < 95:
            love["relationship"] = "深愛"

        else:
            love["relationship"] = "終身伴侶"

    # Flags

    for flag in changes.get(
        "new_flags",
        []
    ):

        if flag not in state["flags"]:

            state["flags"].append(flag)

    for flag in changes.get(
        "remove_flags",
        []
    ):

        if flag in state["flags"]:

            state["flags"].remove(flag)

    # 結局

    if changes.get(
        "death",
        False
    ):

        p["alive"] = False

    if changes.get(
        "arrested",
        False
    ):

        p["arrested"] = True

    if changes.get(
        "listed",
        False
    ):

        p["listed"] = True


# ============================================================
# 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業收入

    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            * random.randint(
                100,
                300
            )
        )

        p["cash"] += income

    # 公司成長

    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            * random.randint(
                100,
                500
            )
        )

        p["company_value"] += growth

    # 月份

    p["month"] += 1

    state["world"]["month"] = p["month"]

    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        state["world"]["month"] = 1

        for b in state["brothers"].values():

            b["age"] += 1


# ============================================================
# 戀愛 NPC
# ============================================================

def create_love_interest(state):

    if state["love_interest"]:
        return

    candidates = [

        {

            "name": "林雨晴",

            "personality":
                "聰明、溫柔、獨立",

            "likes":
                ["誠實", "陪伴", "責任感"],

            "dislikes":
                ["欺騙", "失約"],

            "dream":
                "開一家自己的咖啡店",

            "affection": 10,
            "trust": 10,

            "relationship":
                "陌生"
        },

        {

            "name": "陳若涵",

            "personality":
                "活潑、勇敢、喜歡冒險",

            "likes":
                ["自由", "冒險", "幽默"],

            "dislikes":
                ["控制", "無聊"],

            "dream":
                "環遊世界",

            "affection": 10,
            "trust": 10,

            "relationship":
                "陌生"
        },

        {

            "name": "許雅婷",

            "personality":
                "成熟、理性、有原則",

            "likes":
                ["穩定", "誠實", "上進"],

            "dislikes":
                ["謊言", "不負責任"],

            "dream":
                "建立自己的事業",

            "affection": 10,
            "trust": 10,

            "relationship":
                "陌生"
        }
    ]

    state["love_interest"] = random.choice(
        candidates
    )


# ============================================================
# 記憶
# ============================================================

def add_memory(
    state,
    action,
    story
):

    memory = {

        "age":
            state["player"]["age"],

        "month":
            state["player"]["month"],

        "player_action":
            action,

        "story":
            story[-2500:]
    }

    state["history"].append(
        memory
    )

    if len(
        state["history"]
    ) > 30:

        state["history"] = (
            state["history"][-30:]
        )


# ============================================================
# 網頁首頁
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# ============================================================
# 新遊戲 API
# ============================================================

@app.route(
    "/api/new_game",
    methods=["POST"]
)
def api_new_game():

    state = new_game()

    try:

        story = generate_story(
            state
        )

        return jsonify({

            "success": True,

            "state": state,

            "story": story

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# 玩家行動 API
# ============================================================

@app.route(
    "/api/action",
    methods=["POST"]
)
def api_action():

    try:

        data = request.get_json()

        state = data.get(
            "state"
        )

        action = data.get(
            "action",
            ""
        )

        current_story = data.get(
            "story",
            ""
        )

        if not state:

            return jsonify({

                "success": False,

                "error":
                    "找不到遊戲狀態"

            }), 400

        if not action:

            action = (
                "玩家選擇暫時不採取行動。"
            )

        # AI 判定劇情

        result = resolve_action(
            state,
            action,
            current_story
        )

        # AI 判定數值

        changes = calculate_changes(
            state,
            action,
            result
        )

        # 套用數值

        apply_changes(
            state,
            changes
        )

        # 記憶

        add_memory(
            state,
            action,
            result
        )

        # 世界推進

        world_tick(
            state
        )

        # 等待一秒
        # 網頁前端也會配合顯示

        return jsonify({

            "success": True,

            "state": state,

            "result": result,

            "changes": changes

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# 下一個月劇情
# ============================================================

@app.route(
    "/api/next_month",
    methods=["POST"]
)
def api_next_month():

    try:

        state = request.get_json()

        p = state["player"]

        # 隨機戀愛 NPC

        if (

            state["love_interest"] is None

            and p["age"] >= 18

            and random.random() < 0.25

        ):

            create_love_interest(
                state
            )

        story = generate_story(
            state
        )

        return jsonify({

            "success": True,

            "state": state,

            "story": story

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# 啟動
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )
