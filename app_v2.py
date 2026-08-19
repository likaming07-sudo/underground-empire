import streamlit as st
import json
import random
import time
from typing import List
from pydantic import BaseModel, Field
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
        "請到 Streamlit Cloud → App Settings → Secrets "
        "設定 GEMINI_API_KEY。"
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

# Gemini 3.1 系列目前可使用的 Flash-Lite 模型
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI 結構化輸出 Schema
#
# 這裡故意不用 Optional[str]。
# 避免之前：
#
# set_love_interest.type = ['string', 'null']
#
# 的 Schema 錯誤。
# ============================================================

class Changes(BaseModel):
    cash_change: int = 0
    assets_change: int = 0
    company_value_change: int = 0
    legal_business_change: int = 0
    power_change: int = 0
    reputation_change: int = 0
    police_attention_change: int = 0
    health_change: int = 0


class BrotherChange(BaseModel):
    loyalty_change: int = 0
    trust_change: int = 0
    respect_change: int = 0


class BrothersChanges(BaseModel):
    阿龍: BrotherChange = Field(default_factory=BrotherChange)
    阿虎: BrotherChange = Field(default_factory=BrotherChange)
    阿豪: BrotherChange = Field(default_factory=BrotherChange)


class LoveResult(BaseModel):
    # 永遠是 true / false，不允許 null
    created: bool = False

    # 沒有建立 NPC 時就使用空字串
    name: str = ""

    personality: str = ""

    background: str = ""

    occupation: str = ""

    dream: str = ""

    values: str = ""

    boundary: str = ""

    # 如果是玩家已經認識的人，可以指定其名字
    existing_name: str = ""

    affection_change: int = 0
    trust_change: int = 0
    respect_change: int = 0

    # 是否把這個人設為目前最重要的感情對象
    select_as_interest: bool = False


class AIResult(BaseModel):
    story: str

    action_result: str

    next_month_story: str

    changes: Changes = Field(default_factory=Changes)

    brothers: BrothersChanges = Field(
        default_factory=BrothersChanges
    )

    love: LoveResult = Field(
        default_factory=LoveResult
    )

    flags_add: List[str] = Field(
        default_factory=list
    )

    flags_remove: List[str] = Field(
        default_factory=list
    )

    death: bool = False

    arrested: bool = False

    listed: bool = False


# ============================================================
# ④ AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的人生 RPG。

玩家18歲開始，出生於台灣普通家庭。

玩家：

現金 0
資產 0
公司估值 0
合法事業 0
地下勢力 0
聲望 0

玩家沒有背景、沒有特殊能力、沒有特殊人脈。

三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。


============================================================
【世界規則】
============================================================

每個月是一回合。

世界必須自己運作。

世界不能只圍著玩家轉。

不要每個月都發生重大事件。

事件大小必須有變化。

普通月份應該佔大多數：

工作
學習
家庭
朋友
兄弟
生活
休息
小型機會

中型事件：

工作機會
商業機會
人際衝突
競爭
感情
小型危機
朋友事件

大型事件：

成立公司
重大商業機會
企業危機
警方調查
重大人物
媒體事件

大型事件不能連續每個月發生。

玩家18歲初期尤其不要頻繁發生大型事件。


============================================================
【玩家成長】
============================================================

玩家必須從普通人慢慢成長。

不能：

突然暴富
突然獲得大量資產
突然認識總裁
突然認識部長
突然認識大企業家
突然成為地下世界大人物
突然擁有巨大勢力

人物與世界必須有合理接觸理由。

玩家還是普通人時：

主要接觸：

同學
同事
鄰居
朋友
普通商家
小型企業
一般社會人士

玩家工作穩定後：

可以逐漸認識：

主管
老闆
客戶
合作夥伴

玩家建立事業後：

才可能逐漸認識：

企業家
投資人
業界人士

玩家聲望提高後：

才可能接觸：

媒體
大型企業
重要人物

所有人物都必須有合理出現原因。


============================================================
【經濟規則】
============================================================

玩家必須靠合理行動賺錢。

一般工作：

每月收入應該有限。

小型生意：

需要投入資金、時間或人脈。

公司：

需要逐步建立。

不能因為一次普通行動就增加數十萬、數百萬資產。

如果玩家目前沒有資金：

不能無理由投資大型企業。

如果玩家資金不足：

可以：

找工作
學習技能
找合作夥伴
存錢
接小型工作

世界經濟必須符合玩家目前階段。


============================================================
【兄弟】
============================================================

兄弟不是工具人。

三個兄弟都有自己的：

性格
利益
目標
底線
能力
情緒

他們可以：

支持玩家
反對玩家
拒絕玩家
爭吵
嫉妒
失望
離開
改變想法

如果玩家做出兄弟不能接受的事情：

忠誠
信任
尊重

可以下降。

不要讓兄弟永遠無條件支持玩家。


============================================================
【一般 NPC】
============================================================

NPC不是工具人。

NPC有：

利益
恐懼
性格
目標
底線
家庭
工作
人際關係

NPC可以：

幫助玩家
拒絕玩家
欺騙玩家
競爭
嫉妒
離開
改變態度

NPC不會因為玩家是主角就自動喜歡玩家。


============================================================
【感情系統】
============================================================

玩家開局沒有女朋友。

不要第一個月直接送女朋友。

感情必須自然發生。

可能流程：

陌生人
↓
認識
↓
熟悉
↓
普通朋友
↓
關係變好
↓
曖昧
↓
交往

但是：

不是所有女性 NPC 都會成為戀愛對象。

玩家可能：

對某人沒有感覺
喜歡 A
喜歡 B
同時認識多人
最後選擇其中一人
誰都沒有追到
被拒絕
關係惡化

不要替玩家決定「玩家愛上誰」。

玩家的感情應該透過玩家自己的行動逐漸形成。


============================================================
【女性 NPC】
============================================================

女性 NPC 必須是完整人物。

她必須有：

姓名
性格
家庭背景
工作或學業
夢想
價值觀
喜好
底線
自己的生活

她不是玩家工具人。

她可以：

拒絕玩家
不喜歡玩家
對玩家沒有感覺
生氣
失望
忙於自己的生活
主動聯絡
主動做事情
與其他人交往
離開玩家

不要因為玩家選擇「聊天」就自動增加大量好感。

第一次認識：

好感通常 0～3
信任通常 0～3
尊重通常 0～3

普通互動：

一次最多小幅變化。

重要關係必須慢慢建立。


============================================================
【感情出現頻率】
============================================================

不要每個月都生成新女性 NPC。

感情只是人生的一部分。

可能連續數個月都沒有新的感情事件。

女性 NPC 必須在合理場景出現：

工作
學校
朋友介紹
社交活動
興趣
店家
社區
合作
日常生活

不要憑空出現。


============================================================
【關係數值】
============================================================

一般 NPC與感情 NPC可以有：

affection
trust
respect

數值 0～100。

陌生人：

affection 0～2
trust 0～2
respect 0～2

第一次見重要人物：

通常不會突然變成朋友。

例如：

第一次見企業家：

affection +0
trust +0
respect +1

而不是：

affection +10
trust +10


============================================================
【玩家自由】
============================================================

玩家可以自由輸入任何合理行動。

不要只限制三個選項。

玩家永遠可以自己輸入行動。

不要替玩家說話。

不要替玩家決定想法。

不要替玩家決定感情。

不要擅自讓玩家答應事情。

不要擅自讓玩家做重大決定。


============================================================
【犯罪內容】
============================================================

虛構犯罪劇情可以存在。

但是：

不要提供現實世界可以直接執行的犯罪方法。

不要提供：

具體操作步驟
工具
逃避警方方法
藏匿證據方法
規避法律技巧

犯罪劇情只能描述：

事件
人物反應
風險
後果
法律結果

重點是故事，而不是犯罪教學。


============================================================
【玩家失敗】
============================================================

玩家不是無敵的。

玩家可能：

失敗
被拒絕
賠錢
失去工作
朋友疏遠
兄弟失望
商業失敗
感情失敗

但是不要為了虐玩家而故意讓所有事情失敗。

結果必須根據行動合理判斷。


============================================================
【時間】
============================================================

每次玩家完成一個行動：

就是一個月。

系統會在玩家行動後進入下一個月。

下一個月的劇情必須自然銜接。

不要讓時間突然跳十年。

除非遊戲狀態合理。


============================================================
【AI任務】
============================================================

每次玩家完成一個行動後：

1. 判斷行動是否合理
2. 判斷成功、部分成功或失敗
3. 產生自然劇情
4. 讓 NPC 按照性格反應
5. 更新關係
6. 更新數值
7. 決定下一個月開場
8. 保持世界連續性
9. 不讓玩家突然暴富
10. 不讓所有 NPC 喜歡玩家


============================================================
【重要】
============================================================

你必須輸出符合指定 JSON Schema 的資料。

不要輸出 Markdown。

不要輸出 ```json。

不要在 JSON 外面加入說明。

所有欄位都必須符合 Schema。


============================================================
【Love 特別規則】
============================================================

love.created：

如果本回合沒有新感情 NPC：

false

如果合理地出現一個新的女性 NPC：

true

created=true 時：

name
personality
background
occupation
dream
values
boundary

都必須填寫。

如果沒有創造新 NPC：

這些欄位全部填空字串。

existing_name：

如果本回合正在互動的是已經存在的女性 NPC，
可以填她的名字。

如果沒有：

空字串。

select_as_interest：

只有在玩家的行動和劇情真的足以讓某個 NPC 成為目前重要感情對象時才使用 true。

不要因為第一次見面就 true。

不要自動讓玩家愛上她。


============================================================
【數值限制】
============================================================

cash_change：

普通事件通常 -500～5000。

大型且合理的收入可能更高，
但必須符合玩家目前階段。

assets_change：

必須有合理購買或取得來源。

company_value_change：

只有玩家有事業、公司或合理商業活動時才增加。

legal_business_change：

通常 0～5。

power_change：

普通人生階段通常接近 0。

reputation_change：

普通事件通常 -2～3。

police_attention_change：

沒有法律問題時通常 0。

health_change：

普通月份通常 -2～2。

不要亂改數值。


============================================================
【死亡與逮捕】
============================================================

death：

只有極端合理劇情才能 true。

不要隨便殺死玩家。

arrested：

只有劇情真的導致警方逮捕時才 true。

listed：

只有公司真的完成合理上市條件時才 true。


============================================================
【第一個月】
============================================================

如果是新遊戲第一回合：

玩家18歲。

沒有錢。

沒有公司。

沒有資產。

沒有勢力。

沒有女朋友。

不要生成大型事件。

不要生成企業家。

不要生成地下世界大人物。

可以從：

找工作
學習
家庭
兄弟
朋友
生活

開始。

感情 NPC 不要強制出現。


============================================================
【整體風格】
============================================================

這是一個長篇人生模擬器。

劇情要像真實人生：

有無聊月份
有普通月份
有開心月份
有失敗月份
有機會
有衝突
有意外
有成長

不要每個月都像電影高潮。

世界必須慢慢發展。
"""


# ============================================================
# ⑤ 新遊戲
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

        # 不再只有單一女友欄位
        "love_npcs": [],

        # 目前最重要的感情對象
        "selected_love": "",

        "flags": [],

        "history": [],

        "current_story": None,

        "current_result": None,

        "game_started": False
    }


# ============================================================
# ⑥ AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    last_error = None

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM_PROMPT,

                    response_mime_type="application/json",

                    response_schema=AIResult,

                    temperature=0.85,

                    thinking_config=types.ThinkingConfig(
                        thinking_level="low"
                    )
                )
            )

            if not response.text:

                raise RuntimeError(
                    "AI 沒有返回內容。"
                )

            result = AIResult.model_validate_json(
                response.text
            )

            return result.model_dump()

        except Exception as e:

            last_error = e
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
                    "Gemini API 額度或速率限制已達上限。\n\n"
                    "請稍後再試，或確認你的 Gemini API "
                    "方案與額度。"
                )

            if (
                "401" in error_text
                or
                "403" in error_text
            ):

                raise RuntimeError(
                    "Gemini API Key 無效，"
                    "或目前 API Key 沒有 Gemini API 權限。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    f"找不到 Gemini 模型：{MODEL}\n\n"
                    "請確認 API Key 所使用的 Gemini API "
                    "是否支援這個模型。"
                )

            if attempt < retries - 1:

                time.sleep(2)
                continue

    raise RuntimeError(
        f"AI 發生錯誤：{last_error}"
    )


# ============================================================
# ⑦ 建立本回合 Prompt
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

        "love_npcs": state.get(
            "love_npcs",
            []
        ),

        "selected_love": state.get(
            "selected_love",
            ""
        ),

        "flags": state["flags"],

        "recent_history": state["history"][-10:],

        "current_story": state["current_story"],

        "player_action": action
    }

    if action:

        data["task"] = """
玩家已經完成本月行動。

請根據玩家目前的：

年齡
資產
工作
人際關係
兄弟關係
感情
過去事件

判斷這次行動。

請：

1. 產生行動結果
2. 判斷成功、部分成功或失敗
3. 更新合理數值
4. 更新 NPC 關係
5. 如果合理，可以讓世界產生新的小事件
6. 如果合理，可以建立新的 NPC
7. 決定下一個月開場
8. 保持故事連續

注意：

不要替玩家做下一個月的重大選擇。

下一個月只能描述「發生了什麼」，
不要替玩家決定「玩家一定要怎麼做」。
"""

    else:

        data["task"] = """
這是新遊戲。

請生成：

18歲・第1個月

的開場劇情。

玩家：

現金0
資產0
公司0
合法事業0
地下勢力0
聲望0
沒有女朋友

請從普通人生開始。

可以是：

工作
學習
家庭
兄弟
朋友
生活

不要大型事件。

不要突然認識：

總裁
部長
政治人物
大企業家
地下世界大人物

也不要強制生成戀愛 NPC。

第一個月可以完全沒有感情事件。
"""

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# ⑧ 安全數值
# ============================================================

def safe_int(value):

    try:

        return int(value)

    except Exception:

        return 0


# ============================================================
# ⑨ 套用玩家數值
# ============================================================

def apply_player_changes(
    state,
    result
):

    p = state["player"]

    changes = result.get(
        "changes",
        {}
    )

    money_fields = [

        "cash",
        "assets",
        "company_value"
    ]

    stat_fields = [

        "legal_business",
        "power",
        "reputation",
        "police_attention",
        "health"
    ]

    for field in money_fields:

        key = field + "_change"

        value = safe_int(
            changes.get(
                key,
                0
            )
        )

        # 防止 AI 一次亂塞超大數值
        value = max(
            -100000,
            min(
                100000,
                value
            )
        )

        p[field] += value

    for field in stat_fields:

        key = field + "_change"

        value = safe_int(
            changes.get(
                key,
                0
            )
        )

        value = max(
            -10,
            min(
                10,
                value
            )
        )

        p[field] += value

    # --------------------------------------------------------
    # 最低限制
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


# ============================================================
# ⑩ 套用兄弟關係
# ============================================================

def apply_brother_changes(
    state,
    result
):

    brothers = result.get(
        "brothers",
        {}
    )

    for name in state["brothers"]:

        if name not in brothers:

            continue

        changes = brothers[name]

        b = state["brothers"][name]

        for field in [

            "loyalty",
            "trust",
            "respect"

        ]:

            key = field + "_change"

            value = safe_int(
                changes.get(
                    key,
                    0
                )
            )

            value = max(
                -5,
                min(
                    5,
                    value
                )
            )

            b[field] += value

            b[field] = max(
                0,
                min(
                    100,
                    b[field]
                )
            )


# ============================================================
# ⑪ 感情 NPC
# ============================================================

def find_love_npc(
    state,
    name
):

    if not name:

        return None

    for npc in state["love_npcs"]:

        if npc["name"] == name:

            return npc

    return None


def apply_love_changes(
    state,
    result
):

    love_data = result.get(
        "love",
        {}
    )

    # --------------------------------------------------------
    # ① 建立新 NPC
    # --------------------------------------------------------

    if love_data.get(
        "created",
        False
    ):

        name = str(
            love_data.get(
                "name",
                ""
            )
        ).strip()

        if name:

            existing = find_love_npc(
                state,
                name
            )

            if existing is None:

                npc = {

                    "name": name,

                    "personality":
                        love_data.get(
                            "personality",
                            "個性獨立"
                        ),

                    "background":
                        love_data.get(
                            "background",
                            ""
                        ),

                    "occupation":
                        love_data.get(
                            "occupation",
                            ""
                        ),

                    "dream":
                        love_data.get(
                            "dream",
                            ""
                        ),

                    "values":
                        love_data.get(
                            "values",
                            ""
                        ),

                    "boundary":
                        love_data.get(
                            "boundary",
                            ""
                        ),

                    "affection": 1,

                    "trust": 1,

                    "respect": 1,

                    "relationship": "認識"
                }

                state["love_npcs"].append(
                    npc
                )


    # --------------------------------------------------------
    # ② 更新既有 NPC
    # --------------------------------------------------------

    target_name = love_data.get(
        "existing_name",
        ""
    ).strip()

    if not target_name:

        if love_data.get(
            "created",
            False
        ):

            target_name = love_data.get(
                "name",
                ""
            ).strip()

    npc = find_love_npc(
        state,
        target_name
    )

    if npc:

        affection_change = max(
            -5,
            min(
                5,
                safe_int(
                    love_data.get(
                        "affection_change",
                        0
                    )
                )
            )
        )

        trust_change = max(
            -5,
            min(
                5,
                safe_int(
                    love_data.get(
                        "trust_change",
                        0
                    )
                )
            )
        )

        respect_change = max(
            -5,
            min(
                5,
                safe_int(
                    love_data.get(
                        "respect_change",
                        0
                    )
                )
            )
        )

        npc["affection"] += (
            affection_change
        )

        npc["trust"] += (
            trust_change
        )

        npc["respect"] += (
            respect_change
        )

        npc["affection"] = max(
            0,
            min(
                100,
                npc["affection"]
            )
        )

        npc["trust"] = max(
            0,
            min(
                100,
                npc["trust"]
            )
        )

        npc["respect"] = max(
            0,
            min(
                100,
                npc["respect"]
            )
        )

        affection = npc["affection"]

        if affection < 10:

            npc["relationship"] = "陌生"

        elif affection < 25:

            npc["relationship"] = "認識"

        elif affection < 45:

            npc["relationship"] = "熟悉"

        elif affection < 65:

            npc["relationship"] = "朋友"

        elif affection < 80:

            npc["relationship"] = "曖昧"

        elif affection < 95:

            npc["relationship"] = "交往"

        else:

            npc["relationship"] = "深度交往"

        # ----------------------------------------------------
        # 不允許第一次見面直接變成戀愛對象
        # ----------------------------------------------------

        if (
            love_data.get(
                "select_as_interest",
                False
            )
            and
            npc["affection"] >= 50
            and
            npc["trust"] >= 40
        ):

            state["selected_love"] = (
                npc["name"]
            )


# ============================================================
# ⑫ Flags
# ============================================================

def apply_flags(
    state,
    result
):

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


# ============================================================
# ⑬ 結局
# ============================================================

def apply_endings(
    state,
    result
):

    p = state["player"]

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
# ⑭ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # --------------------------------------------------------
    # 合法事業被動收益
    #
    # 不讓 AI 每次亂加錢後又自動爆賺。
    # --------------------------------------------------------

    business = p["legal_business"]

    if business > 0:

        base_income = int(
            business *
            random.randint(
                20,
                80
            )
        )

        # 根據玩家目前階段限制被動收益
        base_income = min(
            base_income,
            5000
        )

        p["cash"] += base_income

    # --------------------------------------------------------
    # 公司成長
    # --------------------------------------------------------

    if business >= 10:

        growth = int(
            business *
            random.randint(
                20,
                100
            )
        )

        growth = min(
            growth,
            10000
        )

        p["company_value"] += growth

    # --------------------------------------------------------
    # 進入下一個月
    # --------------------------------------------------------

    p["month"] += 1

    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for brother in state["brothers"].values():

            brother["age"] += 1


# ============================================================
# ⑮ 人生記憶
# ============================================================

def add_memory(
    state,
    action,
    result
):

    p = state["player"]

    memory = {

        "age":
            p["age"],

        "month":
            p["month"],

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

    # 最多保留40回合
    if len(
        state["history"]
    ) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑯ 存檔
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


# ============================================================
# ⑰ 舊存檔相容
# ============================================================

def normalize_loaded_game(game):

    # 舊版可能只有 love_interest
    if "love_npcs" not in game:

        game["love_npcs"] = []

        old_love = game.get(
            "love_interest"
        )

        if old_love:

            game["love_npcs"].append(
                old_love
            )

    if "selected_love" not in game:

        game["selected_love"] = ""

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

    if "save_version" not in game:

        game["save_version"] = 2

    # 玩家欄位補齊
    player_defaults = new_game()["player"]

    for key, value in player_defaults.items():

        if key not in game["player"]:

            game["player"][key] = value

    # 兄弟欄位補齊
    default_brothers = new_game()["brothers"]

    for name, default in default_brothers.items():

        if name not in game["brothers"]:

            game["brothers"][name] = default

        else:

            for key, value in default.items():

                if key not in game["brothers"][name]:

                    game["brothers"][name][key] = value

    return game


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

        return normalize_loaded_game(
            game
        )

    except json.JSONDecodeError:

        raise ValueError(
            "存檔檔案不是有效的 JSON。"
        )

    except Exception as e:

        raise ValueError(
            f"讀取存檔失敗：{e}"
        )


# ============================================================
# ⑱ CSS
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
# ⑲ Session State
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


state = st.session_state.game

p = state["player"]


# ============================================================
# ⑳ 標題
# ============================================================

st.markdown(
    '<div class="main-title">👑 地下帝國：AI人生</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI 驅動的人生模擬 RPG</div>',
    unsafe_allow_html=True
)


# ============================================================
# ㉑ 存檔 / 讀檔
# ============================================================

with st.expander("💾 存檔 / 讀檔"):

    st.caption(
        "建議每玩幾個月就下載一次存檔。"
        "存檔為 JSON，可以之後重新上傳。"
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
# ㉒ 開始畫面
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

        你可以找工作、學習、建立事業、
        發展人際關係，也可能經歷失敗。

        感情不會開局直接送給你。

        世界也不會因為你是玩家就永遠順利。
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
# ㉓ 結局
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

        st.session_state.game = new_game()

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

        st.session_state.game = new_game()

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

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


# ============================================================
# ㉔ 玩家狀態
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
# ㉕ 三兄弟
# ============================================================

with st.expander("👊 三兄弟"):

    for name, brother in state["brothers"].items():

        st.write(
            f"### {name}"
        )

        st.write(

            f"忠誠：{brother['loyalty']}　"
            f"信任：{brother['trust']}　"
            f"尊重：{brother['respect']}　"
            f"能力：{brother['ability']}"
        )

        st.caption(
            brother["personality"]
        )


# ============================================================
# ㉖ 感情 NPC
# ============================================================

with st.expander("❤️ 感情 / 人際"):

    love_npcs = state.get(
        "love_npcs",
        []
    )

    if not love_npcs:

        st.write(
            "目前還沒有特別的感情對象。"
        )

        st.caption(
            "感情會隨著人生自然發展。"
        )

    else:

        for npc in love_npcs:

            is_selected = (
                npc["name"]
                ==
                state.get(
                    "selected_love",
                    ""
                )
            )

            title = npc["name"]

            if is_selected:

                title += " ❤️"

            st.markdown(
                f"### {title}"
            )

            st.write(
                f"關係：{npc['relationship']}"
            )

            st.write(
                f"好感：{npc['affection']}/100"
            )

            st.write(
                f"信任：{npc['trust']}/100"
            )

            st.write(
                f"尊重：{npc['respect']}/100"
            )

            st.write(
                f"性格：{npc['personality']}"
            )

            if npc.get("occupation"):

                st.write(
                    f"工作／學業：{npc['occupation']}"
                )

            if npc.get("dream"):

                st.write(
                    f"夢想：{npc['dream']}"
                )

            if npc.get("values"):

                st.write(
                    f"價值觀：{npc['values']}"
                )

            st.divider()


# ============================================================
# ㉗ 第一個月開場
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

            state["current_result"] = None

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉘ 本月劇情
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
# ㉙ 玩家行動
# ============================================================

st.subheader(
    "🎮 你的行動"
)

with st.form(
    "action_form",
    clear_on_submit=True
):

    action = st.text_area(

        "你想做什麼？",

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
# ㉚ 執行一回合
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

    # --------------------------------------------------------
    # 劇情結果
    # --------------------------------------------------------

    result_text = result.get(
        "action_result",
        "這個行動產生了一些變化。"
    )

    # --------------------------------------------------------
    # 套用數值
    # --------------------------------------------------------

    apply_player_changes(
        state,
        result
    )

    apply_brother_changes(
        state,
        result
    )

    apply_love_changes(
        state,
        result
    )

    apply_flags(
        state,
        result
    )

    apply_endings(
        state,
        result
    )

    # --------------------------------------------------------
    # 人生記憶
    # --------------------------------------------------------

    add_memory(
        state,
        action,
        result
    )

    # --------------------------------------------------------
    # 下一個月
    # --------------------------------------------------------

    world_tick(
        state
    )

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

    state["current_result"] = (
        result_text
    )

    # --------------------------------------------------------
    # 重新整理
    # --------------------------------------------------------

    st.rerun()


# ============================================================
# ㉛ 上一回合結果
# ============================================================

if state.get("current_result"):

    st.subheader(
        "🎬 上一回合結果"
    )

    st.markdown(

        f'<div class="result-box">'
        f'{state["current_result"]}'
        f'</div>',

        unsafe_allow_html=True
    )


# ============================================================
# ㉜ 人生記錄
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
# ㉝ 重新開始
# ============================================================

st.divider()

if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = new_game()

    st.rerun()
