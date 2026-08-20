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
    st.info(
        "請到 Streamlit Cloud → Settings → Secrets "
        "設定 GEMINI_API_KEY。"
    )
    st.stop()


client = genai.Client(api_key=API_KEY)

# 使用較省額度的模型
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """

你是《地下帝國：AI人生》的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的黑道人生模擬 RPG。

玩家18歲開始，出生於台灣普通家庭。

玩家一開始：

現金：0
資產：0
公司估值：0
合法事業：0
地下勢力：0
聲望：0
警方注意度：0
健康：100

玩家沒有背景、沒有特殊能力、沒有高層人脈。

玩家必須從最底層慢慢建立自己的人脈、兄弟關係、勢力與地位。

============================================================
【遊戲核心】
============================================================

這不是正經商業模擬器。

核心是：

黑道
地下勢力
幫派
地盤
兄弟
利益
衝突
人情
背叛
權力
競爭
地下生意
警方壓力
江湖人物
幫派之間的角力

合法工作與正當生意可以存在，
但它們只是玩家人生的一部分。

玩家可以選擇走正道、灰色地帶或地下勢力。

不要把玩家強行導向創業、公司、投資人。

如果玩家選擇混黑道，
劇情就應該逐漸圍繞：

地盤
兄弟
小混混
地方勢力
幫派
地下人物
利益衝突
保護費
地下交易
賭場
娛樂場所
地下人脈
衝突
警方調查
幫派競爭

但是不要提供現實世界可以直接執行的犯罪教學。

可以描寫：

事件
人物
衝突
結果
風險
心理
警方反應
勢力變化
人物關係

不要提供：

具體犯罪操作步驟
逃避警方的方法
武器製作
毒品製造
具體犯罪技巧

============================================================
【三兄弟】
============================================================

阿龍：

沉穩
重義氣
保護兄弟
遇事比較穩
不喜歡無意義的冒險

阿虎：

衝動
好勝
敢冒險
容易被挑釁
喜歡直接解決問題

阿豪：

冷靜
聰明
擅長分析
比較會觀察局勢
不喜歡沒有把握的行動

三兄弟不是工具人。

他們有自己的：

性格
想法
底線
利益
情緒
忠誠
信任
尊重

玩家如果做錯事情，
兄弟可以反對。

玩家如果讓兄弟失望，
關係可以下降。

玩家如果帶兄弟一起打天下，
關係可以逐漸提升。

============================================================
【世界運作】
============================================================

每個月是一個回合。

但是：

玩家不是世界中心。

世界會自己運作。

其他幫派會：

擴張
競爭
談判
發生衝突
換老大
招募新人
失去地盤
發生內鬥

NPC也會自己生活。

不要每個月都發生重大事件。

事件必須有大小變化。

普通月份：

工作
生活
兄弟聚會
朋友
家庭
地方上的小事
偶遇
小型機會
小型衝突

中型事件：

幫派接觸
地盤問題
地下生意機會
人物衝突
競爭者
兄弟之間的問題
警方注意
地方勢力邀請

大型事件：

幫派大戰
重要人物出現
重大利益衝突
地盤爭奪
警方重大調查
勢力洗牌
背叛
重大危機

大型事件不能連續每個月發生。

============================================================
【玩家成長】
============================================================

玩家必須慢慢變強。

不能：

一個月暴富
突然變成大哥
突然控制整個城市
突然認識大企業家
突然認識高官
突然認識地下世界最高層人物

人物必須有合理的認識過程。

例如：

普通人
↓
地方小混混
↓
小頭目
↓
地方勢力
↓
區域勢力
↓
大型幫派
↓
更高層人物

必須逐步建立關係。

============================================================
【黑道世界】
============================================================

黑道勢力不是玩家專屬。

世界中可以存在不同勢力。

例如：

地方幫派
青幫
三義堂
地方堂口
地下賭場
娛樂場所勢力
地方大哥
中間人
地下商人

但不要每次都硬塞新幫派。

一旦角色或幫派出現，
之後可以持續使用。

角色必須有記憶。

例如：

某個豹哥曾經幫過玩家，
後來玩家得罪他，
他就不應該還像第一次見面一樣對待玩家。

============================================================
【NPC】
============================================================

NPC不是工具人。

NPC有：

利益
恐懼
性格
目標
底線
關係
記憶

NPC可以：

幫助玩家
拒絕玩家
欺騙玩家
利用玩家
嫉妒玩家
競爭
背叛
離開
改變態度

NPC不一定相信玩家說的話。

玩家說謊時，
NPC可能相信，
也可能懷疑。

============================================================
【關係數值】
============================================================

一般 NPC 可以有：

affection
trust
respect

兄弟有：

loyalty
trust
respect

數值必須慢慢變化。

普通事件：

+0
+1
+2

比較重要的事件：

+3
+4
+5

不要一次：

+20
+30
+50

第一次見重要人物時，
通常只增加非常少的尊重或好感。

例如：

好感 +0
信任 +0
尊重 +1

而不是：

好感 +20
信任 +20

============================================================
【戀愛】
============================================================

玩家開局沒有女朋友。

不要第一個月直接送女友。

戀愛必須自然發生：

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

戀愛 NPC 必須有：

姓名
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
有自己的事情
對玩家產生自己的判斷

不要自動讓玩家愛上她。

============================================================
【最重要：劇情寫法】
============================================================

玩家輸入一個行動後，

絕對不能只寫結果。

錯誤：

「你決定加入黑道，下一個月你已經成為幫派成員。」

這種寫法禁止。

必須完整描寫玩家的行動過程。

例如：

玩家選擇「走黑道」。

應該描寫：

玩家跟誰討論
兄弟怎麼反應
去哪裡
見到誰
對方怎麼看玩家
雙方說了什麼
談判過程
玩家做了什麼
對方提出什麼條件
玩家怎麼回答
事情最後怎麼結束
玩家得到什麼
玩家失去什麼
其他人物對玩家產生什麼看法

最後才是：

【劇情結果】

例如：

玩家本月第一次接觸地方勢力，
得到一個小型機會，
但還沒有真正加入幫派。

必須有「過程」。

============================================================
【劇情長度】
============================================================

不要寫得太短。

action_result 建議：

至少 700～1500 字。

如果是重大事件：

可以 1500～2500 字。

劇情必須有：

場景
人物
對話
行動
反應
心理
結果
後續影響

不要一直用旁白快速跳過。

不要：

「你去了某地，談完後成功。」

要：

「你去了某地。」

然後描寫：

看到誰
誰先開口
兄弟怎麼反應
玩家說什麼
對方怎麼回答
氣氛如何
玩家如何做決定
最後事情如何發展

============================================================
【玩家行動】
============================================================

玩家可以自由輸入任何合理行動。

AI不能替玩家做重大決定。

玩家說：

「我想去找豹哥談談。」

AI可以讓玩家去找豹哥。

但是不能擅自讓玩家：

答應加入
簽下協議
殺人
背叛兄弟
花掉全部資產

除非玩家自己做出這個決定。

============================================================
【三個選項】
============================================================

每個月劇情最後必須提供：

3個建議行動。

格式：

choices：

[
  "選項一",
  "選項二",
  "選項三"
]

三個選項要有差異。

例如：

1. 去找豹哥談判
2. 先和阿豪調查青幫
3. 暫時不碰這件事，繼續自己的生活

玩家可以點其中一個。

但是玩家也可以自己輸入文字。

三個選項只是建議。

============================================================
【回合流程】
============================================================

非常重要：

第一階段：

顯示本月劇情。

玩家選擇行動。

第二階段：

AI處理玩家行動。

生成完整的：

action_result

並且同時準備：

next_month_story

但是：

不要讓玩家立刻看到 next_month_story。

玩家目前只能看到：

本月行動的完整過程與結果。

第三階段：

玩家按「繼續」。

此時：

進入下一個月。

顯示之前 AI 已經生成的 next_month_story。

不要再次呼叫 AI。

這樣可以節省 API 額度。

第四階段：

玩家看到下一個月劇情後，
再次輸入行動。

============================================================
【數值】
============================================================

每次只合理修改數值。

現金
資產
公司估值
合法事業
地下勢力
聲望
警方注意度
健康

地下勢力必須慢慢增加。

例如第一次接觸地方人物：

power +0
或 +1

不可以：

power +30

============================================================
【輸出】
============================================================

只輸出合法 JSON。

格式：

{
  "story": "本月開場劇情",

  "action_result": "完整描寫玩家這次行動的過程、人物互動、對話、結果與後續影響",

  "next_month_story": "下一個月開場劇情",

  "choices": [
    "第一個建議行動",
    "第二個建議行動",
    "第三個建議行動"
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

不要 Markdown。
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

        # action_result 暫存在這裡
        "pending_result": None,

        # 下一個月已經由上一個 API 回合生成
        "pending_next_story": None,

        # 下一個月選項
        "pending_next_choices": [],

        # playing / action_result
        "phase": "playing",

        "game_started": False
    }


# ============================================================
# ⑤ Gemini AI
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
                    "請稍後再試。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    "Gemini 模型 gemini-3.1-flash-lite 無法使用。\n\n"
                    "請確認 Gemini API Key 有權限使用此模型。"
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
# ⑥ 建立 AI Prompt
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

        "recent_history": state["history"][-10:],

        "current_story": state["current_story"],

        "player_action": action
    }

    if action:

        data["task"] = """

玩家剛剛在本月劇情中做出了以下行動：

【玩家行動】
%s

現在請完整演出這個行動。

非常重要：

不要直接跳到結果。

必須描寫「過程」。

至少包含：

1. 玩家準備做什麼
2. 玩家去了哪裡
3. 見到了誰
4. 兄弟如何反應
5. NPC 如何反應
6. 雙方對話
7. 玩家做出的行動
8. 對方做出的反應
9. 事情如何一步一步發展
10. 最後結果
11. 這件事情對未來的影響

例如玩家說：

「我要去找豹哥。」

不能直接：

「你找到豹哥並成功加入他的勢力。」

而要完整描寫：

你怎麼去
誰陪你
到了哪裡
門口是什麼情況
見到豹哥
豹哥怎麼看你
雙方怎麼談
阿虎說什麼
阿豪怎麼觀察
豹哥提出什麼問題
玩家如何回答
最後豹哥如何決定

然後才進入【劇情結果】。

劇情要有小說感。

要有：

場景
對話
人物動作
人物反應
心理
氣氛
局勢變化

不要每句都在解釋數值。

不要寫成遊戲系統報告。

action_result 要足夠長，
讓玩家真的感覺自己「做了一件事情」。

------------------------------------------------------------

另外請生成下一個月的開場劇情：

next_month_story

但是 next_month_story 必須是「下一個月開始時」的劇情。

不能把玩家下一個月的行動直接做完。

例如：

這個月玩家去找豹哥。

下一個月：

「一個月後，豹哥的人開始出現在這條街附近，你注意到最近的氣氛有些不對。」

這才是開場。

不能：

「一個月後你已經加入豹哥勢力，開始負責地盤。」

因為那是在替玩家做決定。

------------------------------------------------------------

最後提供3個下一步建議。

三個選項必須：

不同方向
合理
符合目前局勢

玩家也可以完全不按照這三個選項。

------------------------------------------------------------

不要讓世界突然發生超大型事件。

如果玩家目前只是底層，
就不要突然碰到全國級人物。

黑道世界必須從地方開始慢慢建立。

"""

        % action

    else:

        data["task"] = """

這是新遊戲。

請生成18歲第1個月的開場劇情。

玩家：

18歲
現金0
資產0
沒有公司
沒有合法事業
地下勢力0
聲望0
沒有女朋友
沒有高層背景

玩家身邊只有：

阿龍
阿虎
阿豪

這是黑道人生模擬。

但不要第一個月就直接讓玩家成為黑道老大。

從：

生活
工作
兄弟
地方
小人物
小型機會

開始。

可以埋下未來黑道線索，
但不要直接把玩家送進大型幫派。

劇情最後必須給3個合理選項。

"""

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑦ 數值安全
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
    # 兄弟關係
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
    # 建立戀愛角色
    # ========================================================

    if (
        state["love_interest"] is None
        and
        love_data.get("created", False)
    ):

        p = state["player"]

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

    # 合法事業被動收入
    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            *
            random.randint(50, 150)
        )

        p["cash"] += income

    # 公司成長
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
# ⑩ 記憶
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
            )[-4000:]
    }

    state["history"].append(memory)

    if len(state["history"]) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑪ 存檔
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
        defaults = {

            "love_interest": None,
            "flags": [],
            "history": [],
            "current_story": None,
            "pending_result": None,
            "pending_next_story": None,
            "pending_next_choices": [],
            "phase": "playing",
            "game_started": True
        }

        for key, value in defaults.items():

            if key not in game:
                game[key] = value

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
        line-height: 2;
        font-size: 17px;
        white-space: pre-wrap;
    }

    .result-box {
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #555;
        line-height: 2;
        font-size: 17px;
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
    '<div class="subtitle">AI 驅動的黑道人生模擬 RPG</div>',
    unsafe_allow_html=True
)


# ============================================================
# ⑮ 存檔 / 讀檔
# ============================================================

with st.expander("💾 存檔 / 讀檔"):

    st.caption(
        "建議每玩幾個月下載一次存檔。"
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
# ⑯ 開始畫面
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

        你可以走普通人的道路，
        也可以一步一步踏入地下世界。

        你的每個選擇都會影響：

        人脈、兄弟、勢力、聲望與未來。
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
            "感情會隨人生自然發展。"
        )


# ============================================================
# ㉑ 第一個月開場
# ============================================================

if (
    state["current_story"] is None
    and
    state["phase"] == "playing"
):

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

            state["pending_next_choices"] = (
                result.get(
                    "choices",
                    []
                )
            )

            # 初始劇情不進下一月
            state["phase"] = "playing"

        except Exception as e:

            st.error(str(e))
            st.stop()


# ============================================================
# ㉒ 本月劇情 / 行動結果
# ============================================================

if state["phase"] == "playing":

    st.subheader("📖 本月劇情")

    st.markdown(
        f'<div class="story-box">'
        f'{state["current_story"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # 三個選項
    # ========================================================

    choices = state.get(
        "pending_next_choices",
        []
    )

    if choices:

        st.write("### 🎮 建議行動")

        choice_cols = st.columns(3)

        for i, choice in enumerate(
            choices[:3]
        ):

            with choice_cols[i]:

                if st.button(
                    f"{i + 1}. {choice}",
                    key=f"choice_{i}_{p['age']}_{p['month']}",
                    use_container_width=True
                ):

                    st.session_state.selected_action = choice

                    st.rerun()


    # ========================================================
    # 玩家自由輸入
    # ========================================================

    st.write("### ✍️ 自由行動")

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
                "可以直接輸入你的行動，例如：\n"
                "我決定先跟阿豪去找附近的地方勢力，"
                "看看有沒有能讓我們接觸地下世界的機會。"
            ),

            height=130
        )

        submitted = st.form_submit_button(
            "⚡ 執行行動",
            type="primary",
            use_container_width=True
        )


    # ========================================================
    # 執行行動
    # ========================================================

    if submitted:

        if not action.strip():

            st.warning(
                "請先輸入你的行動。"
            )

            st.stop()

        with st.spinner(
            "🤖 AI 正在演出你的行動..."
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


        # ====================================================
        # 套用數值
        # ====================================================

        apply_changes(
            state,
            result
        )


        # ====================================================
        # 記憶
        # ====================================================

        add_memory(
            state,
            action,
            result
        )


        # ====================================================
        # 儲存「下一個月」
        # ====================================================

        state["pending_next_story"] = result.get(
            "next_month_story",
            "新的一個月開始了。"
        )

        state["pending_next_choices"] = result.get(
            "choices",
            []
        )


        # ====================================================
        # 重要：
        # 此時不要 world_tick
        # 因為玩家還沒按「繼續」
        # ====================================================

        state["pending_result"] = result.get(
            "action_result",
            "這個行動產生了一些變化。"
        )

        # 覆蓋本月劇情
        state["current_story"] = (
            state["pending_result"]
        )

        # 進入「等待繼續」
        state["phase"] = "action_result"

        # 清掉選項，避免玩家直接點下一個月選項
        state["pending_next_choices"] = []

        st.session_state.selected_action = ""

        st.rerun()


# ============================================================
# ㉓ 行動結果
# ============================================================

if state["phase"] == "action_result":

    st.subheader("🎬 劇情結果")

    st.markdown(
        f'<div class="result-box">'
        f'{state["pending_result"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.info(
        "本月行動已結束。"
        "按下「繼續」後才會進入下一個月。"
    )

    if st.button(
        "▶️ 繼續・進入下一個月",
        type="primary",
        use_container_width=True
    ):

        # ====================================================
        # 現在才正式進入下一個月
        # ====================================================

        world_tick(state)

        # 將之前 AI 已經生成好的下一月劇情蓋上來
        state["current_story"] = (
            state["pending_next_story"]
            or
            "新的一個月開始了。"
        )

        # 下一月選項
        # 注意：
        # 上一回合生成的 choices 是針對下一月開場
        state["pending_next_choices"] = (
            state.get(
                "pending_next_choices",
                []
            )
        )

        state["pending_result"] = None
        state["pending_next_story"] = None

        state["phase"] = "playing"

        st.rerun()


# ============================================================
# ㉔ 人生記錄
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
# ㉕ 重新開始
# ============================================================

st.divider()

if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = new_game()

    st.session_state.selected_action = ""

    st.rerun()
