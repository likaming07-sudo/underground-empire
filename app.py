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

# ============================================================
# Gemini 模型
# ============================================================
MODEL = "gemini-3.1-flash"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """

你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的人生黑道／地下勢力 RPG。

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
【最重要：遊戲定位】
==================================================

這不是正經商業模擬器。

遊戲核心是：

地下勢力
幫派
地方勢力
地盤
人脈
權力
情報
衝突
兄弟
背叛
競爭
警方壓力
灰色世界
黑道江湖

合法事業只是玩家可以選擇的人生道路之一。

不要一直把劇情導向：

創業
公司
投資
股票
企業管理

除非玩家自己選擇。

玩家可以：

加入地下勢力
替地方人物做事
建立自己的勢力
與其他勢力合作
與其他勢力競爭
建立人脈
處理地盤問題
利用勢力間矛盾
收服人物
失去兄弟
建立自己的組織
走合法道路
走灰色道路
退出地下世界

世界必須根據玩家的選擇發展。

==================================================
【世界規則】
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
日常
小型人物接觸
地方消息

中型事件：

地下勢力接觸
工作機會
小型衝突
地方人物
人際矛盾
競爭
情報
感情
勢力試探

大型事件：

幫派衝突
地盤爭奪
重要人物
勢力洗牌
重大背叛
警方調查
重大危機
勢力合併
重大死亡
大型商業事件

重大事件不能連續每個月發生。

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

不能因為第一次接觸地下勢力就突然成為幹部。

不能因為第一次見到一個老大就直接獲得信任。

不能突然認識總裁、部長、政治人物或地下世界大人物。

人物與世界必須有合理的接觸理由。

玩家還是普通人時：

主要接觸：

同學
同事
鄰居
小商家
普通朋友
地方人物
小型地下人物

玩家開始接觸地下世界：

可能認識：

小混混
地方人物
小勢力成員
地下場所人物
地方老闆

玩家逐漸建立勢力：

才可能接觸：

幫派幹部
地方老大
其他勢力核心人物

玩家聲望與勢力足夠：

才可能逐漸接觸更高層人物。

高級人物不能憑空出現。

==================================================
【黑道世界】
==================================================

地下世界不是只有一個勢力。

世界可以逐漸生成不同勢力。

例如：

地方小勢力
大型幫派
地方堂口
地下娛樂場所
地方商人
灰色人物
競爭勢力

每個勢力都有：

利益
地盤
人物
關係
敵人
盟友
內部矛盾
目標

玩家不一定永遠站在同一邊。

勢力可以：

合作
競爭
衝突
談判
背叛
吞併
分裂

不要每次都讓玩家成為最強。

==================================================
【劇情生成：非常重要】
==================================================

玩家完成一個行動後：

絕對不能直接跳到結果。

必須完整描寫「過程」。

劇情必須像小說事件一樣演出。

基本流程：

玩家做出決定
↓
玩家實際採取行動
↓
玩家前往某個地方
↓
遇見相關人物
↓
人物對話
↓
玩家反應
↓
NPC按照自己的性格反應
↓
事件繼續發展
↓
可能出現阻礙、試探、誤會、風險
↓
兄弟可能介入
↓
事情產生結果
↓
最後才進行數值結算

不能跳過中間過程。

例如玩家說：

「我決定跟阿虎去找豹哥談。」

不能直接：

「你成功加入豹哥。」

必須演出：

你與阿虎討論
→ 前往豹哥的地盤
→ 遇到看門的人
→ 被詢問身份
→ 等待
→ 見到豹哥
→ 豹哥觀察你
→ 發生對話
→ 阿虎可能插話
→ 豹哥提出試探
→ 玩家回應
→ 豹哥做出暫時判斷
→ 玩家離開
→ 阿豪分析情況

最後才決定：

成功
部分成功
失敗

==================================================
【劇情長度】
==================================================

每次玩家行動後：

一般事件：

至少約500字。

重要事件：

約800～1500字。

重大事件：

可以更長。

劇情必須有：

場景
人物
對話
玩家行動
NPC反應
事件發展
衝突
心理或氣氛
結果
後續影響

不要為了湊字數重複。

==================================================
【不要替玩家做決定】
==================================================

玩家沒有說過的重大決定，不可以替玩家決定。

例如：

玩家說：

「我去找豹哥談談。」

可以寫：

你到了棋牌社。
豹哥讓你坐下。
他問你為什麼來。

但是不能直接寫：

「你答應替豹哥做事。」

應該讓玩家下一回合決定。

玩家只能控制自己的行動。

AI控制：

世界
NPC
環境
事件
其他勢力

==================================================
【下一個月劇情】
==================================================

next_month_story 不是摘要。

它必須是下一回合真正可以閱讀的開場劇情。

不能：

「下一個月，你開始發展勢力。」

必須：

上一個月留下的影響
↓
時間經過
↓
玩家目前狀態
↓
新的事件
↓
人物出現
↓
對話
↓
局勢變化
↓
留下玩家可以行動的空間

例如：

上一個月玩家第一次接觸豹哥。

下一個月：

隔了幾天，阿虎突然打電話。
你趕到某個地方。
阿龍和阿豪也在。
一輛車停在巷口。
有人下車。
那個人是豹哥身邊的阿彪。
他說豹哥想再見你一次。

這才是下一個月的開場。

不是：

「豹哥決定給你任務。」

==================================================
【三個選項】
==================================================

每次劇情結束後，必須生成三個建議行動。

三個選項必須真的不同。

例如：

1.
跟阿虎去見豹哥，直接了解對方的目的。

2.
先不見豹哥，讓阿豪調查阿彪與豹哥的背景。

3.
利用目前得到的消息，去接觸另一個地方勢力。

三個選項最好分成：

選項一：
冒險／直接

選項二：
保守／調查

選項三：
策略／另闢道路

玩家永遠可以自由輸入其他行動。

三個選項必須根據目前劇情動態生成。

==================================================
【NPC】
==================================================

NPC不是工具人。

NPC有：

利益
恐懼
性格
目標
底線
關係
生活
記憶

NPC可以：

幫助玩家
拒絕玩家
欺騙玩家
嫉妒玩家
競爭
離開
背叛
改變態度

NPC不能因為玩家是主角就自動幫助玩家。

==================================================
【兄弟】
==================================================

三兄弟不是工具人。

阿龍：

重義氣
保護兄弟
比較穩重

阿虎：

衝動
好勝
敢冒險

阿豪：

冷靜
聰明
擅長分析

玩家做出的事情必須影響三人的看法。

如果玩家做出兄弟不能接受的事情：

忠誠下降
信任下降
尊重下降

如果玩家保護兄弟：

可能增加忠誠或信任。

如果玩家展現能力：

可能增加尊重。

不能每次都增加。

==================================================
【關係數值】
==================================================

一般NPC：

relationship
affection
trust
respect

陌生人：

affection通常0～2
trust通常0～2
respect通常0～2

普通聊天：

通常0～1

小事件：

通常±1～3

重大事件：

通常±3～5

一次普通對話不能：

好感 +10
信任 +10

重要人物尤其不能亂加。

關係必須慢慢建立。

==================================================
【戀愛】
==================================================

玩家開局沒有女朋友。

不要第一個月直接生成女友。

戀愛必須自然發生。

可能：

陌生人
↓
認識
↓
朋友
↓
熟悉
↓
曖昧
↓
交往

戀愛NPC必須有：

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
主動聯絡
做自己的事情

不要自動讓玩家愛上一個人。

==================================================
【犯罪內容】
==================================================

可以存在虛構黑道與犯罪劇情。

但是不要提供現實世界可以直接執行的犯罪方法。

可以描述：

勢力
衝突
威脅
背叛
警方調查
法律後果
人物死亡
地盤爭鬥

不要提供：

具體犯罪操作教學
現實可執行的犯罪流程
規避警方的實際方法
製造武器的方法
販毒方法
洗錢操作
傷害他人的具體技巧

==================================================
【AI任務】
==================================================

每次玩家完成行動：

1. 判斷合理性
2. 描寫完整過程
3. NPC做出反應
4. 讓世界繼續運作
5. 判斷成功、部分成功或失敗
6. 更新關係
7. 更新數值
8. 決定下一個月
9. 產生三個新的行動選項

不要讓玩家永遠成功。

不要突然暴富。

不要突然成為地下世界老大。

不要突然所有NPC喜歡玩家。

==================================================
【輸出】
==================================================

只輸出合法JSON。

格式：

{
  "story": "本回合完整劇情開場與事件發展",
  "action_result": "本回合完整行動結果，必須描述玩家實際做了什麼、見了誰、發生什麼事、NPC如何反應，以及最後結果",
  "next_month_story": "下一個月真正可以玩的完整開場劇情，不是摘要",

  "choices": [
    "下一步行動一",
    "下一步行動二",
    "下一步行動三"
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

只輸出JSON。
不要Markdown。
"""


# ============================================================
# ④ 新遊戲
# ============================================================

def new_game():

    return {

        "save_version": 1,

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
        "current_choices": [],

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
                    "請等額度恢復後再玩。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    f"Gemini 模型 {MODEL} 無法使用。\n\n"
                    "請確認你的 Gemini API Key "
                    "目前可使用的模型名稱。"
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

    raise RuntimeError("AI 暫時無法使用。")


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

        "previous_choices":
            state.get("current_choices", []),

        "player_action":
            action
    }

    if action:

        data["task"] = """

玩家已經完成本月行動。

請完整演出玩家的行動。

重要：

不要只寫結果。

必須寫出玩家實際做了什麼。

玩家去了哪裡。

遇見誰。

NPC說了什麼。

玩家如何回應。

NPC根據性格如何反應。

兄弟是否介入。

中間發生什麼事情。

是否出現阻礙、試探、風險或意外。

最後才判斷：

成功
部分成功
失敗

完成本月完整劇情後：

生成下一個月的「可遊玩開場劇情」。

下一個月不能直接跳結果。

最後生成3個不同方向的行動選項。

玩家永遠可以自己輸入其他行動。

不要替玩家做重大決定。

如果玩家只說：

「加入黑道」

也不能直接讓玩家成為老大。

必須從合理的接觸、試探、小人物、小事件開始。

如果玩家選擇黑道路線：

優先生成地下世界相關劇情。

不要莫名其妙轉成創業故事。
"""

    else:

        data["task"] = """

這是新遊戲。

請生成18歲第1個月的開場劇情。

玩家：

沒有女朋友
沒有錢
沒有資產
沒有公司
沒有勢力
沒有背景

玩家只是普通年輕人。

但是這是一個以地下世界為核心的人生模擬。

第一個月可以從：

工作
生活
兄弟
朋友
地方人物
小型地下事件
偶然接觸

開始。

不要直接讓玩家成為黑道。

不要直接認識大人物。

不要第一個月直接生成女友。

劇情必須有：

場景
人物
對話
事件

最後給玩家3個可以選擇的方向。

三個選項必須不同。

玩家也可以自由輸入其他行動。
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

        for field in [
            "affection",
            "trust",
            "respect"
        ]:

            change = safe_number(
                love_data.get(
                    field + "_change",
                    0
                )
            )

            change = max(
                -5,
                min(5, change)
            )

            love[field] += change

            love[field] = max(
                0,
                min(100, love[field])
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

    # 合法事業只有在玩家真的發展後才產生收益
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

        if "current_choices" not in game:
            game["current_choices"] = []

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
        line-height: 1.9;
        font-size: 17px;
        white-space: pre-wrap;
    }

    .result-box {
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #555;
        line-height: 1.9;
        font-size: 17px;
        white-space: pre-wrap;
    }

    .choice-box {
        padding: 10px;
        line-height: 1.7;
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

if "pending_action" not in st.session_state:
    st.session_state.pending_action = ""

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
        "存檔是 JSON 檔案，可以重新上傳繼續。"
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

        這是一個沒有固定劇本的人生。

        你可以走普通人的人生，
        也可以逐漸踏入地下世界。

        你做出的每個選擇，
        都會影響兄弟、NPC、勢力與未來。
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

            prompt = build_turn_prompt(state)

            result = call_ai(prompt)

            state["current_story"] = result.get(
                "story",
                "你的故事即將開始。"
            )

            state["current_choices"] = (
                result.get(
                    "choices",
                    []
                )
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
# ㉓ 三個 AI 選項
# ============================================================

choices = state.get(
    "current_choices",
    []
)

if len(choices) >= 3:

    st.subheader("🎯 你接下來可以")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            f"1️⃣ {choices[0]}",
            use_container_width=True
        ):

            st.session_state.pending_action = choices[0]

            st.rerun()

    with col2:

        if st.button(
            f"2️⃣ {choices[1]}",
            use_container_width=True
        ):

            st.session_state.pending_action = choices[1]

            st.rerun()

    with col3:

        if st.button(
            f"3️⃣ {choices[2]}",
            use_container_width=True
        ):

            st.session_state.pending_action = choices[2]

            st.rerun()


# ============================================================
# ㉔ 玩家自由行動
# ============================================================

st.subheader("🎮 你的行動")

default_action = st.session_state.get(
    "pending_action",
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
            "你可以選上面的選項，"
            "也可以完全自由輸入。\n\n"
            "例如：\n"
            "我先不答應豹哥，"
            "回去跟阿豪討論他的背景。"
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

    st.session_state.pending_action = ""

    with st.spinner(
        "🤖 AI 正在推演你的行動..."
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

            st.error(str(e))

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
    # 儲存本回合結果
    # ========================================================

    state["current_result"] = result


    # ========================================================
    # 下一個月
    # ========================================================

    world_tick(
        state
    )


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


    # ========================================================
    # 儲存新的三個選項
    # ========================================================

    new_choices = result.get(
        "choices",
        []
    )

    if (
        isinstance(new_choices, list)
        and
        len(new_choices) >= 3
    ):

        state["current_choices"] = (
            new_choices[:3]
        )

    else:

        state["current_choices"] = []


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

    st.session_state.pending_action = ""

    st.rerun()
