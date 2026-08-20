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

# Gemini 3.1 低成本、高輸出量版本
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """
你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的「虛構地下勢力人生 RPG」。

玩家18歲開始，出生於台灣普通家庭。
玩家沒有錢、沒有資產、沒有背景。

三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。


==================================================
【最重要：遊戲定位】
==================================================

這不是一般創業遊戲。

核心是：

地下勢力
兄弟關係
人際關係
地盤與勢力
聲望
競爭者
衝突
利益
背叛
警方注意
黑白兩道的人際關係
玩家人生發展

玩家可以從普通人開始，逐漸建立自己的地下勢力。

但是成長必須合理。

不要一開始就讓玩家成為黑道老大。
不要一開始就認識大人物。
不要突然獲得大量金錢、地盤或勢力。

所有勢力與人物都必須逐步建立。


==================================================
【世界規則】
==================================================

每個月是一回合。

世界必須自己運作。

不要每個月都發生重大事件。

事件大小必須有變化。

普通月份：

工作
學習
家庭
朋友
兄弟
日常生活
小型人際衝突
小型機會

中型事件：

地下勢力接觸
地方人物
利益衝突
競爭者
兄弟矛盾
人際衝突
感情
小型地盤問題
警方注意增加
新的合作關係

大型事件：

勢力擴張
重大衝突
重大人物
勢力洗牌
重大背叛
企業或地下勢力危機
警方調查
媒體事件

重大事件不能連續每個月發生。

世界不能只圍著玩家轉。

其他勢力也會自行發展。

競爭者也可能變強。

NPC也可能互相合作、衝突、背叛。


==================================================
【玩家成長】
==================================================

開局：

現金 0
資產 0
公司估值 0
合法事業 0
地下勢力 0
聲望 0

玩家必須從普通人慢慢成長。

不能因為一次普通行動突然暴富。

不能因為第一次認識某人就獲得大量勢力。

不能突然認識總裁、部長、政治人物或地下世界大人物。

玩家還是普通人時：

主要接觸：

同學
同事
鄰居
朋友
小商家
地方人物
普通社會人士

玩家逐漸建立勢力後：

才可能接觸：

地方勢力
地下人物
企業人士
更有影響力的人物

玩家聲望與勢力提高後：

才可能逐漸接觸更高層人物。

高級人物不能憑空出現。


==================================================
【地下勢力】
==================================================

地下勢力不是單純一個數字。

它代表：

人脈
影響力
地方控制力
兄弟支持
其他勢力對玩家的忌憚

power 增加必須有合理原因。

例如：

建立可靠人脈
長期經營地方關係
解決重大衝突
建立勢力
獲得人物支持

不要因為普通聊天就增加大量 power。

地下勢力也可能下降。

例如：

背叛
失敗
兄弟離心
重大衝突失利
警方壓力
聲望下降


==================================================
【金錢】
==================================================

金錢必須符合玩家目前階段。

玩家一開始沒有錢。

不要因為普通行動突然獲得巨額金錢。

收入與資產必須有合理來源。

玩家如果沒有合法工作、事業或其他合理收入來源，
不要隨便增加大量現金。

地下劇情可以存在金錢利益，
但不要提供現實犯罪的具體操作方式。


==================================================
【犯罪內容】
==================================================

本遊戲可以存在虛構犯罪、地下勢力與黑道劇情。

但是不要提供現實世界可以直接執行的犯罪方法。

可以描述：

事件
結果
風險
人物反應
勢力變化
法律後果
警方注意

不要提供：

具體犯罪操作
具體逃避警方的方法
具體武器使用方法
具體毒品交易方法
具體犯罪流程
具體規避法律方法

犯罪內容必須停留在故事層面。


==================================================
【玩家自由】
==================================================

玩家可以自由輸入任何合理行動。

不要只限制玩家使用選項。

每回合提供 3 個建議選項，
但玩家永遠可以自己輸入行動。

不要替玩家說話。

不要替玩家做重大決定。

不要擅自讓玩家答應事情。

玩家輸入的行動才是玩家真正做出的事情。


==================================================
【三個建議選項】
==================================================

每個回合必須提供恰好 3 個建議行動。

三個選項不能完全一樣。

選項應該具有不同方向，例如：

1. 穩健
2. 冒險
3. 人際／兄弟

但不要每回合固定使用這三種分類。

選項必須根據當月劇情產生。

例如：

option_1：
先觀察地方勢力的動向，不急著介入。

option_2：
和阿虎一起接觸對方。

option_3：
先和阿豪討論這件事情的風險。

三個選項都必須是玩家可以實際選擇的行動。


==================================================
【兄弟】
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

兄弟不是工具人。

他們有自己的想法。

如果玩家做出他們不能接受的事情：

忠誠可以下降
信任可以下降
尊重可以下降

如果玩家保護兄弟、信守承諾、長期合作：

可以增加忠誠
信任
尊重

一次普通行動不能大幅改變關係。

兄弟關係必須慢慢變化。


==================================================
【一般 NPC】
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

NPC不會因為玩家是主角就一定幫助玩家。


==================================================
【關係數值】
==================================================

一般 NPC 可以有：

relationship
affection
trust
respect

陌生人：

affection 通常 0～2
trust 通常 0～2
respect 通常 0～2

普通對話不能突然 +10。

第一次見重要人物：

通常只會產生很小的變化。

例如：

affection +0
trust +0
respect +1

重要人物的關係必須慢慢建立。

除非玩家做出真正重大、合理、長期的事情，
否則一次最多小幅變化。


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

不要為了推進戀愛而強迫劇情。


==================================================
【玩家不能被 AI 操控】
==================================================

不要替玩家說：

「你答應了」
「你同意了」
「你決定加入」
「你接受了」

除非玩家自己明確做出這個選擇。

AI只能描述世界對玩家行動的反應。


==================================================
【成功與失敗】
==================================================

玩家不會永遠成功。

每次玩家行動都要判斷：

成功
部分成功
失敗

結果必須符合：

玩家能力
兄弟能力
人脈
目前勢力
目前資源
NPC態度
風險
世界環境

不能因為玩家輸入得很有氣勢就自動成功。


==================================================
【世界連續性】
==================================================

必須記住最近發生的事情。

之前得罪的人不能突然變成朋友。

之前幫助過玩家的人不能毫無理由消失。

兄弟關係要延續。

戀愛關係要延續。

敵對勢力要延續。

玩家建立的聲望要延續。

玩家造成的後果要延續。


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
7. 產生下一個月劇情
8. 產生 3 個下一步建議
9. 保持世界連續性

一次 API 必須完成以上工作。

不要額外要求玩家等待第二次 AI 呼叫。


==================================================
【輸出】
==================================================

只能輸出合法 JSON。

不要 Markdown。

不要 ```json。

格式必須完全符合：

{
  "story": "本月劇情",

  "action_result": "玩家本次行動的結果",

  "next_month_story": "下一個月開場劇情",

  "options": [
    {
      "id": 1,
      "text": "第一個建議行動"
    },
    {
      "id": 2,
      "text": "第二個建議行動"
    },
    {
      "id": 3,
      "text": "第三個建議行動"
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
        "current_options": [],

        "game_started": False
    }


# ============================================================
# ⑤ Gemini AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config={

                    "system_instruction": SYSTEM_PROMPT,

                    # Gemini 3.1 Flash-Lite 使用低思考量
                    # 減少延遲與消耗
                    "thinking_level": "minimal",

                    "response_mime_type": "application/json"
                }
            )

            if not response.text:
                raise RuntimeError("AI 沒有返回內容")

            text = response.text.strip()

            if text.startswith("```json"):
                text = text[7:]

            if text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            # 確保 options 存在
            if not isinstance(result.get("options"), list):
                result["options"] = []

            # 最多保留 3 個
            result["options"] = result["options"][:3]

            return result

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
                    "請稍後再使用。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    "Gemini 模型無法使用。\n\n"
                    "目前設定：gemini-3.1-flash-lite"
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

def build_turn_prompt(state, action=None):

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

        # 只傳最近 8 回合
        # 避免歷史越來越長
        "recent_history": state["history"][-8:],

        "current_story": state["current_story"],

        "player_action": action
    }

    if action:

        data["task"] = """

玩家已經完成本月行動。

請：

1. 判斷行動結果
2. 產生本次行動結果劇情
3. 更新玩家數值
4. 更新三兄弟關係
5. 如果有戀愛 NPC，更新關係
6. 決定下一個月劇情
7. 產生恰好 3 個下一步建議

請特別注意：

這是一個地下勢力人生模擬。

不要把劇情全部變成合法創業。

地下勢力、兄弟、人際、聲望、競爭者、
警方注意度都是重要核心。

但是犯罪內容只能寫成虛構劇情結果，
不能提供現實犯罪操作方法。

下一個月必須自然銜接。
"""

    else:

        data["task"] = """

這是新遊戲。

請生成：

18歲第1個月的開場劇情。

玩家目前：

沒有女友
沒有錢
沒有資產
沒有公司
沒有勢力
沒有背景

三個兄弟陪伴玩家。

故事應該從普通人生開始，
但要埋下未來地下勢力人生的可能性。

不要直接讓玩家認識大人物。

不要直接給玩家女友。

不要直接讓玩家成為地下勢力人物。

請同時給出 3 個合理的第一步建議。

注意：

這不是正經商業模擬器。

核心仍然是未來逐步建立地下勢力、
兄弟關係、人際關係、聲望與衝突。
"""

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑦ 安全數值
# ============================================================

def safe_number(value):

    if isinstance(value, (int, float)):
        return value

    return 0


# ============================================================
# ⑧ 套用數值
# ============================================================

def apply_changes(state, result):

    p = state["player"]

    changes = result.get("changes", {})

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
            changes.get(key, 0)
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

    p["cash"] = max(0, p["cash"])

    p["assets"] = max(0, p["assets"])

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
    # 三兄弟
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
                data.get(key, 0)
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
        love_data.get("created", False)
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

                    "name": name,

                    "personality":
                        love_data.get(
                            "personality",
                            "個性獨立"
                        ),

                    "affection": 1,
                    "trust": 1,
                    "respect": 1,

                    "relationship": "認識"
                }


    # ========================================================
    # Flags
    # ========================================================

    for flag in result.get(
        "flags_add",
        []
    ):

        if flag not in state["flags"]:

            state["flags"].append(flag)


    for flag in result.get(
        "flags_remove",
        []
    ):

        if flag in state["flags"]:

            state["flags"].remove(flag)


    # ========================================================
    # 結局
    # ========================================================

    if result.get("death", False):
        p["alive"] = False

    if result.get("arrested", False):
        p["arrested"] = True

    if result.get("listed", False):
        p["listed"] = True


# ============================================================
# ⑨ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業只作為其中一條可能的人生路線
    # 不再是遊戲核心

    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            *
            random.randint(50, 150)
        )

        p["cash"] += income

    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            *
            random.randint(50, 200)
        )

        p["company_value"] += growth

    p["month"] += 1

    if p["month"] > 12:

        p["month"] = 1
        p["age"] += 1

        for b in state["brothers"].values():
            b["age"] += 1


# ============================================================
# ⑩ 人生記憶
# ============================================================

def add_memory(state, action, result):

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

    state["history"].append(memory)

    if len(state["history"]) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑪ 存檔系統
# ============================================================

def create_save_data(state):

    return {

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


def save_game_file(state):

    return json.dumps(
        create_save_data(state),
        ensure_ascii=False,
        indent=2
    )


def load_game_file(uploaded_file):

    try:

        data = json.load(uploaded_file)

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

        # 舊存檔相容

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

        if "current_options" not in game:
            game["current_options"] = []

        if "game_started" not in game:
            game["game_started"] = True

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

    .option-box {
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #444;
        margin-bottom: 8px;
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

with st.expander("💾 存檔 / 讀檔"):

    st.caption(
        "建議每玩幾個月就下載一次存檔。"
        "存檔是 JSON 檔案。"
    )

    save_data = save_game_file(state)

    col_save, col_load = st.columns(2)

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

                    st.session_state.game = loaded_game

                    st.success(
                        "存檔讀取成功！"
                    )

                    time.sleep(0.5)

                    st.rerun()

                except Exception as e:

                    st.error(str(e))


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

        這不是一個固定劇本。

        你可以從普通人開始，
        一步一步建立自己的人脈與勢力。

        每個決定都可能改變未來。
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

    st.error("☠️ 你的人生結束了。")

    st.write(
        f"你享年 {p['age']} 歲。"
    )

    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


if p["arrested"]:

    st.error("🚔 你被警方逮捕。")

    st.write(
        "你的人生迎來重大轉折。"
    )

    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


if p["listed"]:

    st.success("🏆 公司成功上市！")

    st.write(
        "你完成了公司上市結局。"
    )

    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


# ============================================================
# ⑱ 狀態
# ============================================================

st.subheader(
    f"📅 {p['age']}歲・第{p['month']}個月"
)

col1, col2, col3, col4 = st.columns(4)

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


col1, col2, col3, col4 = st.columns(4)

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

with st.expander("👊 三兄弟"):

    for name, b in state["brothers"].items():

        st.write(f"### {name}")

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

    with st.expander("❤️ 感情"):

        st.write(
            "目前沒有戀愛對象。"
        )

        st.caption(
            "感情會隨著人生自然發展。"
        )


# ============================================================
# ㉑ 第一個月開場
# ============================================================

if state["current_story"] is None:

    with st.spinner(
        "🤖 AI 正在建立你的世界..."
    ):

        try:

            prompt = build_turn_prompt(state)

            result = call_ai(prompt)

            state["current_story"] = result.get(
                "story",
                "你的故事即將開始。"
            )

            state["current_options"] = (
                result.get("options", [])
            )

            state["current_result"] = None

        except Exception as e:

            st.error(str(e))
            st.stop()


# ============================================================
# ㉒ 劇情
# ============================================================

st.subheader("📖 本月劇情")

st.markdown(
    f'<div class="story-box">'
    f'{state["current_story"]}'
    f'</div>',
    unsafe_allow_html=True
)


# ============================================================
# ㉓ 三個建議行動
# ============================================================

if state["current_options"]:

    st.subheader("💡 你可以選擇")

    option_cols = st.columns(3)

    for index, option in enumerate(
        state["current_options"][:3]
    ):

        text = option.get(
            "text",
            ""
        )

        with option_cols[index]:

            if st.button(
                f"{index + 1}. {text}",
                key=f"option_{p['age']}_{p['month']}_{index}",
                use_container_width=True
            ):

                st.session_state.selected_action = text

                st.rerun()


# ============================================================
# ㉔ 玩家自由行動
# ============================================================

st.subheader("🎮 你的行動")

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
            "直接輸入你的行動，例如：\n"
            "我決定先找一份工作，"
            "晚上再和阿豪討論未來。"
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

    if not action.strip():

        st.warning(
            "請先輸入你的行動。"
        )

        st.stop()

    # 清掉已選選項
    st.session_state.selected_action = ""

    with st.spinner(
        "🤖 AI 正在判定你的選擇..."
    ):

        try:

            prompt = build_turn_prompt(
                state,
                action
            )

            result = call_ai(prompt)

        except Exception as e:

            st.error(str(e))
            st.stop()


    # ========================================================
    # 劇情結果
    # ========================================================

    result_text = result.get(
        "action_result",
        "這個行動產生了一些變化。"
    )

    st.subheader("🎬 劇情結果")

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
    # 下一個月
    # ========================================================

    world_tick(state)


    # AI 已經在同一次 API 呼叫產生下一月
    # 不再額外呼叫 API

    next_story = result.get(
        "next_month_story",
        ""
    )

    if next_story.strip():

        state["current_story"] = next_story

    else:

        state["current_story"] = (
            "新的一個月開始了。"
        )


    state["current_options"] = (
        result.get(
            "options",
            []
        )[:3]
    )

    state["current_result"] = None

    st.rerun()


# ============================================================
# ㉖ 人生記錄
# ============================================================

with st.expander("📜 人生記錄"):

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

    st.session_state.game = new_game()

    st.rerun()
