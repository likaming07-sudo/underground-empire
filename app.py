import streamlit as st
import json
import random
import time
from google import genai


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
    st.info("請到 Streamlit Cloud → Settings → Secrets 設定 API Key。")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Gemini 3.1 Flash-Lite
# Google 官方目前的穩定模型名稱
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """

你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的人生 RPG。

這不是單純的正經商業模擬器。

玩家會從普通人開始，在虛構的地下世界中逐漸接觸不同人物、勢力、利益衝突與人生事件。

玩家18歲開始，出生於台灣。

玩家：

現金0
資產0
公司估值0
合法事業0
地下勢力0
聲望0
警方注意度0

玩家沒有背景。

三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。

==================================================
【最重要：遊戲核心】
==================================================

這是一個「地下帝國：AI人生」模擬器。

核心玩法：

人生
兄弟
人際關係
地下勢力
利益
衝突
聲望
警方注意度
感情
事業
選擇
後果

玩家必須從普通人慢慢成長。

不能開局就變成大人物。

不能突然成為地下世界老大。

不能突然得到大量財富。

不能突然認識總裁、富豪、政治人物或地下世界最高層人物。

所有人物都必須有合理的接觸原因。

==================================================
【世界規則】
==================================================

每個月是一回合。

世界必須自己運作。

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
地方消息
小型人際事件
小型利益問題

中型事件：

工作機會
商業機會
地方勢力接觸
人際衝突
感情
競爭者
利益衝突
兄弟分歧

大型事件：

重大勢力衝突
重大利益事件
重大警方關注
重大人物出現
媒體事件
勢力重組
重大背叛
重大危機

重大事件不能連續每個月發生。

大型事件之後，世界應該逐漸恢復正常。

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
警方注意度0

玩家沒有背景。

玩家還是普通人時：

主要接觸：

同學
同事
鄰居
普通朋友
小商家
地方人物
普通工作相關人士

玩家逐漸建立人脈後：

可能接觸：

地方商家
地方人物
小型勢力
競爭者
中間人物

玩家地位提高後：

才可能接觸更重要的人物。

人物必須一層一層出現。

==================================================
【地下勢力】
==================================================

地下勢力是本遊戲的重要核心數值。

地下勢力不能突然暴增。

地下勢力可以受到：

人脈
兄弟
聲望
事件
利益
長期合作
衝突
玩家選擇

影響。

玩家地下勢力低時：

只能接觸低層級人物。

玩家地下勢力逐漸提高：

才可以慢慢接觸更大的勢力。

不要因為玩家一句話就讓整個地下世界臣服。

==================================================
【警方注意度】
==================================================

警方注意度是重要的世界反應數值。

警方注意度越高：

警方可能更加關注玩家。

可能出現：

盤查
調查
消息
警方人物
法律問題
媒體注意

但是不要每個月都讓警方出現。

警方也有自己的工作與調查方向。

玩家如果長期低調：

警方注意度可能維持低水平。

==================================================
【兄弟】
==================================================

阿龍、阿虎、阿豪不是工具人。

三個兄弟都有自己的：

個性
價值觀
底線
情緒
利益
判斷

他們可以：

幫助玩家
拒絕玩家
反對玩家
提醒玩家
爭吵
失望
嫉妒
支持
離開
改變態度

如果玩家做出兄弟不能接受的事情：

忠誠
信任
尊重

可以下降。

如果玩家長期照顧兄弟、信任兄弟、與兄弟共同經歷重大事件：

可以逐漸提高。

普通事件：

一次通常只變化 ±1～2。

重大事件：

可以變化 ±3～5。

不要亂加。

==================================================
【一般 NPC】
==================================================

NPC 不是工具人。

NPC 必須有：

利益
恐懼
性格
目標
底線
關係
生活

NPC 可以：

幫助玩家
拒絕玩家
欺騙玩家
嫉妒玩家
競爭
離開
改變態度

玩家不能控制 NPC。

==================================================
【戀愛】
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

她可以：

拒絕玩家
生氣
失望
離開
主動做自己的事情

戀愛關係必須慢慢建立。

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

第一次見重要人物：

通常不會突然產生高好感。

例如：

好感 +0
信任 +0
尊重 +1

而不是：

好感 +10
信任 +10

重要人物的關係必須慢慢建立。

==================================================
【玩家自由】
==================================================

玩家可以自由輸入任何合理行動。

不要只限制在三個選項。

每回合提供三個建議選項。

但是玩家永遠可以自己輸入。

不要替玩家說話。

不要替玩家做重大決定。

不要擅自讓玩家答應事情。

==================================================
【劇情品質】
==================================================

不要把劇情寫成簡短事件摘要。

每回合必須像長篇人生 RPG。

劇情應該包含：

1. 場景
2. 人物出場
3. 人物反應
4. 對話
5. 玩家行動
6. 事件發展
7. 成功、部分成功或失敗
8. NPC反應
9. 對玩家數值或人際關係的影響
10. 留下後續發展可能

普通事件：

約500～800字。

中型事件：

約700～1100字。

大型事件：

約900～1400字。

不要為了湊字數重複內容。

對話應該自然。

不要每個 NPC 都用相同語氣。

不要每個月都高潮。

人生必須有平淡月份。

==================================================
【三個建議選項】
==================================================

每回合必須提供三個建議行動。

三個選項必須真正不同。

例如：

第一個：
保守、觀察、降低風險。

第二個：
與兄弟合作、積極處理。

第三個：
冒險、強硬、高風險。

但是不要固定永遠使用這三種。

選項必須根據目前劇情產生。

三個選項不能只是換句話說。

每個選項必須可能導向不同結果。

選項必須符合玩家目前：

年齡
能力
金錢
人脈
地下勢力
聲望
警方注意度
兄弟關係

不能給玩家目前根本做不到的事情。

==================================================
【犯罪內容】
==================================================

這是虛構地下世界遊戲。

可以出現：

地下勢力
犯罪事件
利益衝突
警方調查
法律問題
黑道人物
衝突
背叛
勢力競爭

但是不要提供現實世界可以直接執行的犯罪方法。

不要提供：

具體犯罪操作步驟
逃避警方的方法
躲避監視的方法
武器使用方法
製造違法物品的方法
實際犯罪技巧

只描述：

事件
結果
風險
人物反應
法律後果
人際後果

==================================================
【AI任務】
==================================================

每次玩家完成一個行動後：

1. 判斷玩家行動是否合理
2. 判斷成功、部分成功或失敗
3. 產生完整劇情
4. 讓 NPC 按照自己的性格反應
5. 更新關係
6. 更新玩家數值
7. 決定下一個月發生什麼
8. 保持世界連續性
9. 產生三個不同的建議行動

不要讓玩家永遠成功。

不要突然讓玩家暴富。

不要突然讓玩家成為地下世界老大。

不要突然讓所有 NPC 喜歡玩家。

==================================================
【輸出】
==================================================

你必須只輸出合法 JSON。

格式：

{
  "story": "完整的本月開場劇情",

  "action_result": "如果玩家有行動，描述完整的行動結果；如果是新遊戲則為空字串",

  "next_month_story": "下一個月的開場劇情",

  "choices": [
    {
      "text": "第一個建議行動",
      "risk": "低",
      "style": "保守"
    },
    {
      "text": "第二個建議行動",
      "risk": "中",
      "style": "積極"
    },
    {
      "text": "第三個建議行動",
      "risk": "高",
      "style": "冒險"
    }
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

不要使用 Markdown。

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

        "game_started": False
    }


# ============================================================
# ⑤ AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config={

                    "system_instruction": SYSTEM_PROMPT,

                    "response_mime_type": "application/json"
                }
            )

            if not response.text:

                raise RuntimeError(
                    "AI 沒有返回內容"
                )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text[7:]

            elif text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            return result

        except json.JSONDecodeError:

            if attempt < retries - 1:

                time.sleep(2)
                continue

            raise RuntimeError(
                "AI 回傳的內容不是合法 JSON。"
            )

        except Exception as e:

            error_text = str(e)

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

            if "404" in error_text:

                raise RuntimeError(
                    "Gemini 模型無法使用。\n\n"
                    "目前模型："
                    f"{MODEL}\n\n"
                    "請確認你的 Gemini API Key "
                    "可以使用 Gemini 3.1 Flash-Lite。"
                )

            if (
                "401" in error_text
                or
                "403" in error_text
            ):

                raise RuntimeError(
                    "Gemini API Key 無效或沒有 API 權限。"
                )

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

        "brothers":
            state["brothers"],

        "love_interest":
            state["love_interest"],

        "flags":
            state["flags"],

        "recent_history":
            state["history"][-8:],

        "current_story":
            state["current_story"],

        "player_action":
            action
    }

    if action:

        data["task"] = """

玩家已經完成本月行動。

請完整處理這個行動。

要求：

1. 判斷玩家行動是否合理
2. 判斷成功、部分成功或失敗
3. 生成完整劇情
4. 讓相關 NPC 有合理反應
5. 讓兄弟按照各自個性反應
6. 更新合理的數值
7. 更新合理的人際關係
8. 生成下一個月開場劇情
9. 生成三個不同方向的建議行動

不要直接讓玩家成功。

如果玩家的能力不足，可能失敗。

如果玩家選擇高風險行動，可能產生負面結果。

下一個月必須與本月事件自然銜接。

不要突然生成與前面完全無關的大事件。

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
沒有地下勢力
沒有聲望
沒有背景

玩家只有三個從小一起長大的兄弟。

請讓故事從普通人的生活開始。

可以出現：

工作
學業
家庭
朋友
兄弟
地方生活
小型機會
小型事件

不要直接讓玩家認識：

高官
富豪
大企業家
地下世界最高層人物
大型勢力首領

不要第一個月直接送女友。

劇情要有內容、場景、人物互動和對話。

最後提供三個符合玩家目前能力的行動選項。

action_result 請填空字串。

changes 全部保持合理。

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

        if not isinstance(data, dict):
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

    if not isinstance(love_data, dict):
        love_data = {}

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

    # 合法事業自然收入
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


    # 合法事業估值
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


    # 時間前進
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


        # 玩家舊存檔補欄位
        player_defaults = {

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
        }

        for key, value in player_defaults.items():

            if key not in game["player"]:

                game["player"][key] = value


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

        line-height: 1.9;

        font-size: 17px;

        white-space: pre-wrap;
    }


    .result-box {

        padding: 24px;

        border-radius: 12px;

        border: 1px solid #555;

        line-height: 1.9;

        font-size: 16px;

        white-space: pre-wrap;
    }


    .choice-box {

        padding: 16px;

        border-radius: 10px;

        border: 1px solid #444;

        min-height: 150px;
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


if "selected_action" not in st.session_state:

    st.session_state.selected_action = ""


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
    '<div class="subtitle">AI 驅動的地下世界人生模擬 RPG</div>',
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

                    st.session_state.game = (
                        loaded_game
                    )

                    st.session_state.selected_action = ""

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

        你可以過普通人生，
        也可以逐漸踏入地下世界。
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

        st.session_state.game = (
            new_game()
        )

        st.session_state.selected_action = ""

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

        st.session_state.game = (
            new_game()
        )

        st.session_state.selected_action = ""

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

        st.session_state.game = (
            new_game()
        )

        st.session_state.selected_action = ""

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

            state["current_story"] = (
                result.get(
                    "story",
                    "你的故事即將開始。"
                )
            )

            # 保存整個結果，包含三個選項
            state["current_result"] = result

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
# ㉓ 三個 AI 建議選項
# ============================================================

current_result = state.get(
    "current_result"
)

choices = []

if isinstance(
    current_result,
    dict
):

    choices = current_result.get(
        "choices",
        []
    )


if choices:

    st.subheader(
        "🎯 你可以怎麼做？"
    )

    choice_cols = st.columns(
        3
    )

    for i, choice in enumerate(
        choices[:3]
    ):

        if not isinstance(
            choice,
            dict
        ):

            continue

        text = choice.get(
            "text",
            "未知行動"
        )

        risk = choice.get(
            "risk",
            "未知"
        )

        style = choice.get(
            "style",
            ""
        )

        with choice_cols[i]:

            st.markdown(
                f"""
                <div class="choice-box">

                <strong>選項 {i + 1}</strong>

                <br><br>

                {text}

                <br><br>

                風險：{risk}

                <br>

                類型：{style}

                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                f"選擇 {i + 1}",
                key=f"choice_{i}",
                use_container_width=True
            ):

                st.session_state.selected_action = (
                    text
                )

                st.rerun()


# ============================================================
# ㉔ 玩家自由行動
# ============================================================

st.subheader(
    "🎮 你的行動"
)


selected_action = st.session_state.get(
    "selected_action",
    ""
)


with st.form(
    "action_form",
    clear_on_submit=True
):

    action = st.text_area(

        "你想做什麼？",

        value=selected_action,

        placeholder=(
            "可以直接輸入自己的行動。\n\n"
            "例如：\n"
            "我先不急著答應，回去跟阿豪討論這件事情。"
        ),

        height=140
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
    # 使用 AI 同一次回覆產生的下一月劇情
    # 不額外消耗 API
    # ========================================================

    next_story = result.get(
        "next_month_story",
        ""
    )


    if next_story.strip():

        state["current_story"] = (
            next_story
        )

    else:

        state["current_story"] = (
            "新的一個月開始了。"
        )


    # 重要：
    # 保存 result，讓下一月可以顯示三個選項
    state["current_result"] = result


    # 清掉已選的選項
    st.session_state.selected_action = ""


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

    st.session_state.game = (
        new_game()
    )

    st.session_state.selected_action = ""

    st.rerun()
