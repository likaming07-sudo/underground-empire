import streamlit as st
import json
import random
import time

from google import genai
from google.genai import types


# ============================================================
# ① 網頁設定
# ============================================================

st.set_page_config(
    page_title="地下帝國：AI人生",
    page_icon="👑",
    layout="wide"
)


# ============================================================
# ② Gemini API
# ============================================================

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = None


if not API_KEY:
    st.error("找不到 GEMINI_API_KEY")
    st.info(
        "請到 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY。"
    )
    st.stop()


client = genai.Client(api_key=API_KEY)

# 官方目前的穩定模型
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = r"""
你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的地下勢力人生 RPG。

玩家18歲開始，出生於台灣。

玩家沒有錢、沒有資產、沒有背景。

三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。


==================================================
【核心世界觀】
==================================================

這不是正經商業人生模擬器。

這是一個「地下帝國／黑道勢力」題材的人生模擬 RPG。

玩家可以從普通人開始，逐漸接觸：

街頭人物
小商家
地方勢力
地下人物
競爭勢力
自己的兄弟
警方
媒體
企業人物
更高層的勢力

但所有人物都必須合理出現。

玩家不能因為第一個月做一件小事，
就突然認識地下世界大人物。

人物必須透過事件、關係、聲望、勢力逐步接觸。


==================================================
【世界時間】
==================================================

每個月是一回合。

世界必須有自己的運作。

世界不能只圍著玩家轉。

不要每個月都發生重大事件。

事件大小必須有變化。

普通月份：

工作
學習
家庭
朋友
兄弟
日常生活
街頭生活
小型人際事件

中型事件：

地下人物
勢力衝突
競爭者
利益衝突
小型交易
人際衝突
地方勢力
警方注意
感情

大型事件：

建立地下勢力
重大勢力衝突
大型利益事件
重大人物
警方調查
媒體事件
勢力危機
兄弟關係重大變化

重大事件不能連續每個月發生。

不要為了刺激而每個月硬塞大事件。


==================================================
【玩家成長】
==================================================

玩家必須從普通人慢慢成長。

開局：

現金0
資產0
公司估值0
合法事業0
地下勢力0
聲望0

不能因為一個普通行動突然變成有錢人。

不能突然成為地下世界老大。

不能突然認識總裁、部長、政治人物或地下世界大人物。

人物與世界必須有合理的接觸理由。


玩家還是普通人時：

主要接觸：

普通人
同學
同事
鄰居
小商家
地方人物
普通街頭人物

玩家開始建立勢力後：

才逐漸接觸：

地方勢力
地下人物
競爭勢力
更有影響力的人

玩家聲望與地下勢力提高後：

才可能接觸更高層人物。


==================================================
【地下勢力】
==================================================

地下勢力是重要核心數值。

power 越高：

可以接觸更大的勢力
可以影響更多 NPC
可能產生更大的衝突
可能引起警方注意
可能產生更多利益
也可能產生更多風險

但 power 不能無理由暴增。

普通行動：

power通常 0～2

重要事件：

power可能小幅增加

大型勢力事件：

才可以出現較大的變化。

不要因為玩家說一句「我要當老大」，
就直接增加大量勢力。


==================================================
【現金與資產】
==================================================

玩家開局：

cash = 0

assets = 0

不能無中生有。

玩家必須透過合理劇情獲得金錢。

不能因為一次普通行動直接得到巨額財富。

現金變化必須符合玩家目前的身分與勢力。

玩家越弱：

收入越小。

玩家逐漸建立自己的勢力與事業：

收入才可以逐漸提高。


==================================================
【合法事業】
==================================================

legal_business 可以存在。

但這不是遊戲主軸。

它只是玩家地下勢力之外的一個可能發展方向。

不要把遊戲變成普通企業經營模擬器。


==================================================
【戀愛規則】
==================================================

玩家開局沒有女朋友。

不要第一個月直接生成女友。

不要自動讓玩家愛上一個人。

戀愛必須自然發生。

可能經過：

陌生人
↓
認識
↓
普通朋友
↓
熟悉
↓
曖昧
↓
交往

戀愛 NPC 必須有：

性格
家庭
工作或學業
夢想
價值觀
喜好
底線
自己的生活

她不是玩家工具人。

她可以拒絕玩家。

她可以生氣。

她可以失望。

她可以離開玩家。

她也可以主動做自己的事情。

不要因為玩家是主角，
就讓所有戀愛 NPC 喜歡玩家。


==================================================
【關係數值】
==================================================

一般 NPC：

relationship
affection
trust
respect

陌生人：

affection通常0～2
trust通常0～2
respect通常0～2

一次普通對話不能大幅增加。

重要人物尤其不能亂加。

例如玩家第一次見到重要人物：

好感 +0
信任 +0
尊重 +1

而不是：

好感 +10
信任 +10

重要人物的關係必須慢慢建立。

除非玩家做出真正重大、合理、長期的事情，
否則一次最多小幅變化。


==================================================
【三兄弟】
==================================================

阿龍：

沉穩
重義氣
保護兄弟

阿虎：

衝動
好勝
敢冒險

阿豪：

冷靜
聰明
擅長分析

三兄弟不是工具人。

他們有自己的想法。

玩家做出不同選擇時，
三人的反應可以不同。

例如：

阿龍可能重視兄弟安全。

阿虎可能支持冒險。

阿豪可能認為某個選擇風險太高。

不要讓三個兄弟每次都同意玩家。


==================================================
【兄弟關係數值】
==================================================

每個兄弟都有：

loyalty
trust
respect

普通事件：

通常變化 -2～+2

重大事件：

通常變化 -5～+5

不要亂加。

如果玩家做出兄弟不能接受的事情：

忠誠可以下降。
信任可以下降。
尊重可以下降。

如果玩家保護兄弟、共同經歷重大事件：

可以增加。

三個兄弟的數值必須獨立判定。


==================================================
【NPC】
==================================================

NPC不是工具人。

NPC有自己的：

利益
恐懼
性格
目標
底線
關係
生活

NPC可以：

幫助玩家
拒絕玩家
欺騙玩家
嫉妒玩家
競爭
離開
背叛
改變態度

不要所有 NPC 都對玩家友善。


==================================================
【玩家自由】
==================================================

玩家可以自由輸入任何合理行動。

不要只限制在三個選項。

每回合必須提供三個 AI 建議行動。

但是：

玩家永遠可以自己輸入第四種行動。

不要替玩家說話。

不要替玩家做重大決定。

不要擅自讓玩家答應事情。

不要擅自替玩家選擇三個選項之一。


==================================================
【三個建議選項】
==================================================

每回合必須生成：

option_1
option_2
option_3

三個選項不能只是換句話說。

應該有不同方向。

例如：

1. 跟阿豪討論
2. 去接觸某個人物
3. 留在原地觀察

玩家可以完全不選。

玩家也可以自己輸入行動。

三個選項必須符合目前劇情與玩家目前能力。

不能提供玩家目前根本做不到的選項。


==================================================
【犯罪內容】
==================================================

可以存在虛構地下勢力、黑道、犯罪與警方劇情。

但是不要提供現實世界可以直接執行的犯罪方法。

犯罪內容只描述：

事件
結果
風險
人物反應
法律後果

不要輸出：

具體犯罪操作
規避警方的方法
藏匿犯罪證據的方法
製造武器的方法
毒品製作或取得方法
現實世界犯罪教學

重點放在劇情與角色互動。


==================================================
【AI任務】
==================================================

每次玩家完成一個行動後：

1. 判斷玩家行動是否合理
2. 判斷成功、部分成功或失敗
3. 產生自然劇情
4. 讓 NPC 按照自己的性格反應
5. 更新關係
6. 更新玩家數值
7. 決定下一個月發生什麼
8. 保持世界連續性
9. 產生三個下一回合建議行動

不要讓玩家永遠成功。

不要突然讓玩家暴富。

不要突然讓玩家成為地下世界老大。

不要突然讓所有 NPC 喜歡玩家。

不要讓劇情一直高速發展。

人生要有普通月份。


==================================================
【重要：劇情長度】
==================================================

story：

約 300～700 字。

action_result：

約 300～700 字。

next_month_story：

約 200～500 字。

三個 options：

每個約 20～60 字。

不要寫成小說超長篇。

保持遊戲感。


==================================================
【輸出】
==================================================

你必須只輸出合法 JSON。

不要 Markdown。

不要 ```json。

格式：

{
  "story": "本回合劇情",

  "action_result": "玩家行動結果",

  "next_month_story": "下一個月開場劇情",

  "options": [
    "建議行動一",
    "建議行動二",
    "建議行動三"
  ],

  "changes": {
    "cash_change": 0,
    "assets_change": 0,
    "company_value_change": 0,
    "legal_business_change": 0,
    "power_change": 0,
    "reputation_change": 0,
    "police_attention_change": 0,
    "health_change": 0
  },

  "brothers": {
    "阿龍": {
      "loyalty_change": 0,
      "trust_change": 0,
      "respect_change": 0
    },
    "阿虎": {
      "loyalty_change": 0,
      "trust_change": 0,
      "respect_change": 0
    },
    "阿豪": {
      "loyalty_change": 0,
      "trust_change": 0,
      "respect_change": 0
    }
  },

  "love": {
    "created": false,
    "name": "",
    "personality": "",
    "affection_change": 0,
    "trust_change": 0,
    "respect_change": 0
  },

  "flags_add": [],
  "flags_remove": [],

  "death": false,
  "arrested": false,
  "listed": false
}

只輸出 JSON。
"""


# ============================================================
# ④ 新遊戲
# ============================================================

def new_game():

    return {

        "save_version": 2,

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
                "respect": 80,
                "ability": 65,
                "personality": "沉穩、重義氣、保護兄弟"
            },

            "阿虎": {
                "age": 18,
                "loyalty": 78,
                "trust": 70,
                "respect": 72,
                "ability": 75,
                "personality": "衝動、好勝、敢冒險"
            },

            "阿豪": {
                "age": 18,
                "loyalty": 92,
                "trust": 85,
                "respect": 86,
                "ability": 58,
                "personality": "冷靜、聰明、擅長分析"
            }
        },

        "love_interest": None,

        "flags": [],
        "history": [],

        "current_story": None,
        "current_result": None,

        "options": [],

        "game_started": False
    }


# ============================================================
# ⑤ AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    for attempt in range(retries):

        try:

            # Gemini 3.1 Flash-Lite
            # 正確使用 ThinkingConfig
            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,

                temperature=0.85,

                response_mime_type="application/json",

                thinking_config=types.ThinkingConfig(
                    thinking_level="minimal"
                )
            )

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config=config
            )

            if not response.text:

                raise RuntimeError(
                    "AI 沒有返回內容"
                )

            text = response.text.strip()

            # 防止模型偶爾還是加 Markdown
            if text.startswith("```json"):
                text = text[7:]

            if text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            return result

        except Exception as e:

            error_text = str(e)

            # 免費額度
            if (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < retries - 1:

                    time.sleep(3)

                    continue

                raise RuntimeError(
                    "Gemini 免費額度已達上限。\n\n"
                    "這不是存檔系統的問題，"
                    "請等 API 額度恢復後再玩。"
                )

            # 模型不存在
            if (
                "404" in error_text
                or
                "NOT_FOUND" in error_text
            ):

                raise RuntimeError(
                    "Gemini 模型無法使用。\n\n"
                    "目前程式使用："
                    "gemini-3.1-flash-lite"
                )

            # API Key
            if (
                "401" in error_text
                or
                "403" in error_text
            ):

                raise RuntimeError(
                    "Gemini API Key 無效或沒有 API 權限。"
                )

            # 其他錯誤重試
            if attempt < retries - 1:

                time.sleep(2)

                continue

            raise RuntimeError(
                f"AI 發生錯誤：{error_text}"
            )

    raise RuntimeError(
        "AI 暫時無法使用。"
    )


# ============================================================
# ⑥ 建立 AI 回合資料
# ============================================================

def build_turn_prompt(
    state,
    action=None
):

    p = state["player"]

    data = {

        "current_date": {

            "age": p["age"],

            "month": p["month"]
        },

        "player": p,

        "brothers": state["brothers"],

        "love_interest": state["love_interest"],

        "flags": state["flags"],

        "recent_history": state["history"][-8:],

        "current_story": state["current_story"],

        "previous_options": state.get(
            "options",
            []
        ),

        "player_action": action
    }

    if action:

        data["task"] = """

玩家已經完成本月行動。

請：

1. 判斷行動結果
2. 產生劇情結果
3. 更新玩家數值
4. 更新 NPC 關係
5. 更新兄弟關係
6. 判斷是否有戀愛發展
7. 決定下一個月開場劇情
8. 生成下一個月的三個不同建議行動

注意：

這一回合只處理玩家實際輸入的行動。

不要替玩家額外做其他重大決定。

不要因為玩家輸入一個簡單行動，
就直接讓玩家成為大人物。

世界必須自然發展。
"""

    else:

        data["task"] = """

這是新遊戲。

請生成18歲第1個月的開場劇情。

玩家目前：

沒有女友
沒有錢
沒有資產
沒有公司
沒有勢力
沒有背景

這不是正經企業經營遊戲。

這是一個地下勢力人生模擬 RPG。

但玩家目前只是普通18歲年輕人。

可以從：

工作
學業
家庭
兄弟
朋友
生活
地方人物
小型事件

開始。

不要直接讓玩家認識：

高官
富豪
大企業家
地下世界大人物

戀愛角色不要在開局直接出現。

同時產生三個符合目前身分的建議行動。

三個選項必須方向不同。
"""

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑦ 安全數值
# ============================================================

def safe_number(value):

    if isinstance(
        value,
        (int, float)
    ):

        return value

    return 0


# ============================================================
# ⑧ 套用數值
# ============================================================

def apply_changes(
    state,
    result
):

    p = state["player"]

    changes = result.get(
        "changes",
        {}
    )

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

        value = safe_number(
            changes.get(
                key,
                0
            )
        )

        if field in [

            "cash",
            "assets",
            "company_value"

        ]:

            value = max(
                -100000,
                min(100000, value)
            )

        else:

            value = max(
                -10,
                min(10, value)
            )

        p[field] += value

    # --------------------------------------------------------
    # 基本限制
    # --------------------------------------------------------

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
        min(100, p["legal_business"])
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
        min(100, p["police_attention"])
    )

    p["health"] = max(
        0,
        min(100, p["health"])
    )


    # ========================================================
    # 兄弟
    # ========================================================

    brothers = result.get(
        "brothers",
        {}
    )

    for name, data in brothers.items():

        if name not in state["brothers"]:
            continue

        b = state["brothers"][name]

        for field in [

            "loyalty",
            "trust",
            "respect"

        ]:

            key = field + "_change"

            value = safe_number(
                data.get(
                    key,
                    0
                )
            )

            value = max(
                -5,
                min(5, value)
            )

            b[field] += value

            b[field] = max(
                0,
                min(100, b[field])
            )


    # ========================================================
    # 戀愛
    # ========================================================

    love_data = result.get(
        "love",
        {}
    )

    if state["love_interest"]:

        love = state["love_interest"]

        affection_change = safe_number(
            love_data.get(
                "affection_change",
                0
            )
        )

        trust_change = safe_number(
            love_data.get(
                "trust_change",
                0
            )
        )

        respect_change = safe_number(
            love_data.get(
                "respect_change",
                0
            )
        )

        affection_change = max(
            -5,
            min(5, affection_change)
        )

        trust_change = max(
            -5,
            min(5, trust_change)
        )

        respect_change = max(
            -5,
            min(5, respect_change)
        )

        love["affection"] += affection_change
        love["trust"] += trust_change
        love["respect"] += respect_change

        love["affection"] = max(
            0,
            min(100, love["affection"])
        )

        love["trust"] = max(
            0,
            min(100, love["trust"])
        )

        love["respect"] = max(
            0,
            min(100, love["respect"])
        )

        affection = love["affection"]

        if affection < 20:

            love["relationship"] = "陌生"

        elif affection < 40:

            love["relationship"] = "認識"

        elif affection < 60:

            love["relationship"] = "朋友"

        elif affection < 75:

            love["relationship"] = "曖昧"

        elif affection < 90:

            love["relationship"] = "交往"

        else:

            love["relationship"] = "深度交往"


    # ========================================================
    # 新戀愛角色
    # ========================================================

    if (
        state["love_interest"] is None
        and
        love_data.get(
            "created",
            False
        )
    ):

        # 防止開局直接出現
        if (
            p["age"] > 18
            or
            p["month"] > 2
        ):

            name = love_data.get(
                "name",
                ""
            )

            if name:

                state["love_interest"] = {

                    "name":
                        name,

                    "personality":
                        love_data.get(
                            "personality",
                            "個性獨立"
                        ),

                    "affection":
                        1,

                    "trust":
                        1,

                    "respect":
                        1,

                    "relationship":
                        "認識"
                }


    # ========================================================
    # Flags
    # ========================================================

    for flag in result.get(
        "flags_add",
        []
    ):

        if flag not in state["flags"]:

            state["flags"].append(
                flag
            )


    for flag in result.get(
        "flags_remove",
        []
    ):

        if flag in state["flags"]:

            state["flags"].remove(
                flag
            )


    # ========================================================
    # 結局
    # ========================================================

    if result.get(
        "death",
        False
    ):

        p["alive"] = False


    if result.get(
        "arrested",
        False
    ):

        p["arrested"] = True


    if result.get(
        "listed",
        False
    ):

        p["listed"] = True


# ============================================================
# ⑨ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業只是世界背景的一部分
    if p["legal_business"] > 0:

        income = int(

            p["legal_business"]
            *
            random.randint(
                50,
                150
            )
        )

        p["cash"] += income


    if p["legal_business"] >= 10:

        growth = int(

            p["legal_business"]
            *
            random.randint(
                50,
                200
            )
        )

        p["company_value"] += growth


    # 月份推進
    p["month"] += 1

    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for b in state["brothers"].values():

            b["age"] += 1


# ============================================================
# ⑩ 人生記憶
# ============================================================

def add_memory(
    state,
    action,
    result
):

    memory = {

        "age":
            state["player"]["age"],

        "month":
            state["player"]["month"],

        "action":
            action,

        "result":
            result.get(
                "action_result",
                ""
            )[-2500:]
    }

    state["history"].append(
        memory
    )

    if len(
        state["history"]
    ) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑪ 存檔系統
# ============================================================

def create_save_data(state):

    save_data = {

        "game_name":
            "地下帝國：AI人生",

        "save_version":
            2,

        "saved_at":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "game":
            state
    }

    return save_data


def save_game_file(state):

    data = create_save_data(
        state
    )

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )


def load_game_file(uploaded_file):

    try:

        data = json.load(
            uploaded_file
        )

        if "game" not in data:

            raise ValueError(
                "這不是有效的地下帝國存檔。"
            )

        game = data["game"]

        if "player" not in game:

            raise ValueError(
                "存檔缺少玩家資料。"
            )

        if "brothers" not in game:

            raise ValueError(
                "存檔缺少兄弟資料。"
            )

        # 舊存檔補欄位
        if "love_interest" not in game:

            game["love_interest"] = None

        if "flags" not in game:

            game["flags"] = []

        if "history" not in game:

            game["history"] = []

        if "current_story" not in game:

            game["current_story"] = None

        if "current_result" not in game:

            game["current_result"] = None

        if "game_started" not in game:

            game["game_started"] = True

        if "options" not in game:

            game["options"] = []

        return game

    except json.JSONDecodeError:

        raise ValueError(
            "存檔檔案不是有效的 JSON。"
        )

    except Exception as e:

        raise ValueError(
            f"讀取存檔失敗：{e}"
        )


# ============================================================
# ⑫ CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {

        text-align: center;

        font-size: 42px;

        font-weight: bold;

        margin-bottom: 8px;
    }


    .subtitle {

        text-align: center;

        color: #888;

        margin-bottom: 25px;
    }


    .story-box {

        padding: 24px;

        border-radius: 12px;

        border: 1px solid #444;

        line-height: 1.8;

        font-size: 17px;

        white-space: pre-wrap;
    }


    .result-box {

        padding: 20px;

        border-radius: 12px;

        border: 1px solid #555;

        line-height: 1.8;

        font-size: 16px;

        white-space: pre-wrap;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ⑬ Session
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


state = st.session_state.game

p = state["player"]


# ============================================================
# ⑭ 標題
# ============================================================

st.markdown(
    '<div class="main-title">👑 地下帝國：AI人生</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI 驅動的地下勢力人生模擬 RPG</div>',
    unsafe_allow_html=True
)


# ============================================================
# ⑮ 存檔 / 讀檔
# ============================================================

with st.expander(
    "💾 存檔 / 讀檔"
):

    st.caption(
        "建議每玩幾個月就下載一次存檔。"
        "存檔是 JSON 檔案，之後可以重新上傳繼續。"
    )

    save_data = save_game_file(
        state
    )

    col_save, col_load = st.columns(
        2
    )


    with col_save:

        st.download_button(

            label="💾 下載目前存檔",

            data=save_data,

            file_name=(
                f"地下帝國_"
                f"{p['age']}歲_"
                f"第{p['month']}個月.json"
            ),

            mime="application/json",

            use_container_width=True
        )


    with col_load:

        uploaded_file = st.file_uploader(

            "📂 選擇存檔",

            type=["json"],

            key="save_uploader"
        )


        if uploaded_file is not None:

            if st.button(
                "▶️ 載入這個存檔",
                use_container_width=True
            ):

                try:

                    loaded_game = load_game_file(
                        uploaded_file
                    )

                    st.session_state.game = \
                        loaded_game

                    st.success(
                        "存檔讀取成功！"
                    )

                    time.sleep(0.5)

                    st.rerun()

                except Exception as e:

                    st.error(
                        str(e)
                    )


# ============================================================
# ⑯ 開始遊戲
# ============================================================

if not state["game_started"]:

    st.markdown(
        """
        ## 你的故事開始了

        18歲。

        你出生於台灣普通家庭。

        沒有資產。

        沒有背景。

        沒有人脈。

        身上只有：

        ### 💰 $0

        但你有三個從小一起長大的兄弟：

        **阿龍**
        沉穩、重義氣。

        **阿虎**
        衝動、敢冒險。

        **阿豪**
        冷靜、擅長分析。

        這是一個沒有固定劇本的人生。

        你做的每一個選擇，
        都可能改變未來。

        你可以過普通人生。

        也可以逐漸建立自己的勢力。

        甚至走上一條完全不同的人生道路。
        """
    )


    if st.button(
        "🎮 開始人生",
        type="primary",
        use_container_width=True
    ):

        state["game_started"] = True

        st.rerun()


    st.stop()


# ============================================================
# ⑰ 結局
# ============================================================

if not p["alive"]:

    st.error(
        "☠️ 你的人生結束了。"
    )

    st.write(
        f"你享年 {p['age']} 歲。"
    )


    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = \
            new_game()

        st.rerun()


    st.stop()


if p["arrested"]:

    st.error(
        "🚔 你被警方逮捕。"
    )

    st.write(
        "你的人生迎來重大轉折。"
    )


    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = \
            new_game()

        st.rerun()


    st.stop()


if p["listed"]:

    st.success(
        "🏆 公司成功上市！"
    )

    st.write(
        "你完成了公司上市結局。"
    )


    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = \
            new_game()

        st.rerun()


    st.stop()


# ============================================================
# ⑱ 狀態
# ============================================================

st.subheader(
    f"📅 {p['age']}歲・第{p['month']}個月"
)


col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.metric(
        "💰 現金",
        f"${int(p['cash']):,}"
    )


with col2:

    st.metric(
        "🏠 資產",
        f"${int(p['assets']):,}"
    )


with col3:

    st.metric(
        "🏢 公司估值",
        f"${int(p['company_value']):,}"
    )


with col4:

    st.metric(
        "❤️ 健康",
        f"{int(p['health'])}/100"
    )


col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.metric(
        "🏦 合法事業",
        f"{int(p['legal_business'])}/100"
    )


with col2:

    st.metric(
        "👑 地下勢力",
        int(p["power"])
    )


with col3:

    st.metric(
        "⭐ 聲望",
        int(p["reputation"])
    )


with col4:

    st.metric(
        "👮 警方注意度",
        f"{int(p['police_attention'])}/100"
    )


# ============================================================
# ⑲ 三兄弟
# ============================================================

with st.expander(
    "👊 三兄弟"
):

    for name, b in state["brothers"].items():

        st.write(
            f"### {name}"
        )

        st.write(

            f"忠誠：{b['loyalty']}　"
            f"信任：{b['trust']}　"
            f"尊重：{b['respect']}　"
            f"能力：{b['ability']}"
        )

        st.caption(
            b["personality"]
        )


# ============================================================
# ⑳ 戀愛
# ============================================================

if state["love_interest"]:

    love = state["love_interest"]

    with st.expander(
        f"❤️ {love['name']}"
    ):

        st.write(
            f"關係：{love['relationship']}"
        )

        st.write(
            f"好感：{love['affection']}/100"
        )

        st.write(
            f"信任：{love['trust']}/100"
        )

        st.write(
            f"尊重：{love['respect']}/100"
        )

        st.write(
            f"性格：{love['personality']}"
        )

else:

    with st.expander(
        "❤️ 感情"
    ):

        st.write(
            "目前沒有戀愛對象。"
        )

        st.caption(
            "感情會隨著人生自然發展，"
            "不會開局直接送女友。"
        )


# ============================================================
# ㉑ 第一個月開場
# ============================================================

if state["current_story"] is None:

    with st.spinner(
        "🤖 AI 正在建立你的世界..."
    ):

        try:

            prompt = build_turn_prompt(
                state
            )

            result = call_ai(
                prompt
            )

            state["current_story"] = \
                result.get(
                    "story",
                    "你的故事即將開始。"
                )

            state["options"] = \
                result.get(
                    "options",
                    []
                )[:3]

            # 確保至少有三個選項
            while len(state["options"]) < 3:

                state["options"].append(
                    "自由輸入你想做的事情。"
                )

            state["current_result"] = None

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉒ 劇情
# ============================================================

st.subheader(
    "📖 本月劇情"
)

st.markdown(

    f'<div class="story-box">'
    f'{state["current_story"]}'
    f'</div>',

    unsafe_allow_html=True
)


# ============================================================
# ㉓ 三個 AI 建議
# ============================================================

st.subheader(
    "🎯 建議行動"
)

st.caption(
    "以下只是建議，你也可以自己輸入完全不同的行動。"
)


options = state.get(
    "options",
    []
)


if len(options) >= 3:

    option_cols = st.columns(3)

    for i in range(3):

        with option_cols[i]:

            if st.button(
                f"{i + 1}. {options[i]}",
                key=f"option_{i}",
                use_container_width=True
            ):

                st.session_state.selected_action = \
                    options[i]


# ============================================================
# ㉔ 玩家自由輸入
# ============================================================

st.subheader(
    "🎮 你的行動"
)


default_action = st.session_state.get(
    "selected_action",
    ""
)


with st.form(
    "action_form",
    clear_on_submit=True
):

    action = st.text_area(

        "你想做什麼？",

        value=default_action,

        placeholder=(
            "直接輸入你的行動，例如：\n"
            "我決定先跟阿豪聊聊，"
            "看看他對現在局勢有什麼看法。"
        ),

        height=120
    )


    submitted = st.form_submit_button(

        "⚡ 執行行動",

        type="primary",

        use_container_width=True
    )


# ============================================================
# ㉕ 執行一回合
# ============================================================

if submitted:

    # 清除已選擇的按鈕行動
    if "selected_action" in st.session_state:

        del st.session_state.selected_action


    if not action.strip():

        st.warning(
            "請先輸入你的行動。"
        )

        st.stop()


    with st.spinner(
        "🤖 AI 正在判定你的選擇..."
    ):

        try:

            prompt = build_turn_prompt(
                state,
                action
            )

            result = call_ai(
                prompt
            )

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


    # ========================================================
    # 劇情結果
    # ========================================================

    result_text = result.get(

        "action_result",

        "這個行動產生了一些變化。"
    )


    st.subheader(
        "🎬 劇情結果"
    )


    st.markdown(

        f'<div class="result-box">'
        f'{result_text}'
        f'</div>',

        unsafe_allow_html=True
    )


    # ========================================================
    # 套用數值
    # ========================================================

    apply_changes(
        state,
        result
    )


    # ========================================================
    # 記憶
    # ========================================================

    add_memory(
        state,
        action,
        result
    )


    # ========================================================
    # 進入下一個月
    # ========================================================

    world_tick(
        state
    )


    # ========================================================
    # 使用同一次 API 已產生的下一月劇情
    # 不額外消耗 API
    # ========================================================

    next_story = result.get(
        "next_month_story",
        ""
    )


    if next_story.strip():

        state["current_story"] = \
            next_story

    else:

        state["current_story"] = \
            "新的一個月開始了。"


    # ========================================================
    # 下一月三個選項
    # ========================================================

    new_options = result.get(
        "options",
        []
    )

    if not isinstance(
        new_options,
        list
    ):

        new_options = []


    state["options"] = new_options[:3]


    while len(state["options"]) < 3:

        state["options"].append(
            "自由輸入你想做的事情。"
        )


    state["current_result"] = None


    # ========================================================
    # 重新整理
    # ========================================================

    st.rerun()


# ============================================================
# ㉖ 人生記錄
# ============================================================

with st.expander(
    "📜 人生記錄"
):

    if not state["history"]:

        st.caption(
            "目前還沒有歷史記錄。"
        )

    else:

        for memory in reversed(
            state["history"][-10:]
        ):

            st.markdown(

                f"**{memory['age']}歲・"
                f"第{memory['month']}個月**"
            )

            st.write(
                f"你的行動：{memory['action']}"
            )

            st.write(
                memory["result"]
            )

            st.divider()


# ============================================================
# ㉗ 重新開始
# ============================================================

st.divider()


if st.button(

    "🔄 重新開始人生",

    use_container_width=True
):

    st.session_state.game = \
        new_game()

    if "selected_action" in st.session_state:

        del st.session_state.selected_action

    st.rerun()
