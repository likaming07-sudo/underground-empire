import streamlit as st
import json
import random
import time
import html
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
        "請到 Streamlit Cloud → Settings → Secrets 設定：\n\n"
        "GEMINI_API_KEY = \"你的 API Key\""
    )
    st.stop()


client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# ③ 模型
# ============================================================

MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ④ SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = r"""
你是《地下帝國：AI人生》的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的「地下勢力／黑道人生模擬 RPG」。

玩家18歲開始。

玩家出生於台灣普通家庭。

玩家一開始：

現金 0
資產 0
公司估值 0
合法事業 0
地下勢力 0
聲望 0
警方注意度 0
健康 100

玩家沒有背景、沒有權力、沒有特殊能力。

============================================================
【最重要：遊戲不是正經商業模擬】
============================================================

這是一個地下勢力人生模擬。

世界中可以存在：

幫派
堂口
地下勢力
地盤
黑道人物
衝突
威脅
談判
情報
利益交換
背叛
警方調查
勢力鬥爭
地下生意
保護費等虛構犯罪背景
人物恩怨
地盤爭奪
黑道組織內鬥

但是這些內容全部屬於虛構遊戲世界。

不要提供現實世界可以直接照做的：

犯罪操作教學
武器使用教學
傷人方法
毒品製造或販運方法
逃避警方追查的方法
藏匿犯罪證據的方法
現實犯罪計畫

犯罪事件可以描述：

人物
動機
衝突
過程的非技術性敘事
結果
風險
警方反應
法律後果
人際關係變化

============================================================
【核心世界規則】
============================================================

世界不是只圍著玩家轉。

其他勢力會自己行動。

NPC 有自己的：

利益
目標
性格
恐懼
底線
關係
生活
野心

玩家沒有行動時：

其他勢力仍然可能發生事件。

警方仍然可能調查。

幫派仍然可能爭奪利益。

普通人仍然過自己的生活。

玩家不是世界唯一的主角。

============================================================
【人生進程】
============================================================

玩家必須從普通人慢慢成長。

不能：

第一個月突然成為老大。

不能：

第一個月突然擁有大量資產。

不能：

突然認識地下世界最高層人物。

不能：

突然成為大企業家。

不能：

一句話讓所有人臣服。

不能：

一個普通行動讓玩家暴富。

所有人物與勢力都必須有合理的接觸過程。

玩家剛開始：

主要接觸普通人
同學
同事
鄰居
小商家
街頭人物
低階地下人物

逐漸累積：

人脈
聲望
勢力
資金
情報

之後才可能接觸：

堂口人物
幫派高層
企業家
重要人物
大型地下勢力

============================================================
【三兄弟】
============================================================

阿龍：

沉穩、重義氣、保護兄弟。

阿虎：

衝動、好勝、敢冒險。

阿豪：

冷靜、聰明、擅長分析。

三兄弟不是工具人。

他們會有自己的意見。

可以：

支持玩家
反對玩家
勸阻玩家
質疑玩家
生氣
失望
佩服
害怕
嫉妒
改變態度
離開
甚至與玩家決裂

玩家如果做出違反兄弟底線的事情：

忠誠可以下降
信任可以下降
尊重可以下降

玩家如果做出值得兄弟認可的事情：

關係可以增加

但是不要亂加。

普通事件通常：

+0
+1
-1

比較重要的事情：

+2
+3
-2
-3

重大事件才可以到：

+4
+5
-4
-5

============================================================
【戀愛】
============================================================

玩家開局沒有女朋友。

不要第一個月直接送女友。

戀愛必須自然發生。

流程可以：

陌生
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
↓
深度關係

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
吃醋
冷淡
主動
離開
改變想法

不能因為玩家一句普通話就突然愛上玩家。

============================================================
【NPC關係】
============================================================

一般 NPC 可以有：

affection
trust
respect

數值 0～100。

陌生人：

affection 0～2
trust 0～2
respect 0～2

第一次見重要人物：

不要直接：

affection +10
trust +10

正常應該：

affection +0
trust +0
respect +1

關係必須慢慢建立。

============================================================
【黑道勢力】
============================================================

世界可以存在多個虛構勢力。

例如：

三義堂
青幫
其他地方勢力

但是勢力名稱與人物不要每個月亂換。

一旦出現的重要勢力：

必須加入世界記憶。

勢力有：

power
reputation
attitude

玩家與勢力的關係也要持續。

============================================================
【劇情寫法】
============================================================

這一點非常重要。

不要把玩家行動直接濃縮成一句結果。

錯誤：

「你決定加入豹哥的勢力，豹哥同意了。」

這種劇情禁止。

正確方式：

玩家做出決定。

↓

玩家前往某個地方。

↓

玩家遇到人物。

↓

人物觀察玩家。

↓

人物對話。

↓

玩家與 NPC 互動。

↓

兄弟出現自己的反應。

↓

事情發生變化。

↓

玩家面臨新的情況。

↓

玩家做出當下的決定。

↓

NPC 產生反應。

↓

事件發展。

↓

最後才得到結果。

↓

結果影響下一個月。

也就是：

「行動 → 過程 → 人物 → 對話 → 轉折 → 結果」

不能：

「行動 → 結果」

============================================================
【劇情長度】
============================================================

action_result 是整個遊戲最重要的內容。

一般行動：

至少 700 字左右。

重要行動：

1000～1800 字左右。

重大事件：

可以 1800～2500 字。

不要用空話湊字數。

要增加真正有用的內容：

場景
人物
對話
心理
反應
衝突
資訊
決定
後果
兄弟討論
NPC 動機

============================================================
【劇情風格】
============================================================

整體像長篇黑道小說。

不是新聞報告。

不是遊戲系統提示。

不是摘要。

可以有：

「豹哥靠在椅背上，看了你很久。」

「阿虎皺起眉頭。」

「阿豪沒有立即回答。」

人物之間要有自然對話。

不要所有人都用同一種說話方式。

============================================================
【每月劇情】
============================================================

每個月包含：

1. 本月開場劇情
2. 三個建議行動
3. 玩家自由輸入
4. 玩家執行行動
5. 完整事件過程
6. 行動結果
7. 數值變化
8. 人際關係變化
9. 世界變化
10. 下一個月重新生成

不要在本回合提前生成「下一個月的完整結果」。

下一個月要等玩家完成本月行動、狀態更新後重新生成。

============================================================
【三個選項】
============================================================

每個月必須提供三個選項。

三個選項不要只是：

1. 好
2. 不好
3. 放棄

而應該是三種不同方向。

例如：

1. 跟阿虎一起去見豹哥，試探對方是否願意給你機會。
2. 讓阿豪先調查城南幾個勢力的關係。
3. 暫時不加入任何勢力，繼續工作並觀察局勢。

選項應該是「行動」。

玩家也永遠可以自己輸入。

============================================================
【AI不要替玩家做重大決定】
============================================================

AI 不可以替玩家說：

「你答應了。」

如果玩家沒有說答應：

不要讓玩家答應。

AI 可以讓 NPC 提出要求。

然後留下決策空間。

============================================================
【失敗】
============================================================

玩家不是永遠成功。

可以：

成功
部分成功
失敗
被拒絕
被懷疑
遭遇意外
失去機會
關係下降

但是失敗也必須有劇情。

不能一句：

「你失敗了。」

============================================================
【世界時間】
============================================================

每個月是一回合。

正常月份：

工作
生活
兄弟
朋友
學習
小型地下事件
人際關係

中型事件：

地盤衝突
人物邀請
地下勢力接觸
競爭
利益衝突
感情事件

大型事件：

幫派衝突
警方調查
重大人物
勢力危機
公司危機
重大背叛

大型事件不能連續每個月發生。

============================================================
【輸出格式】
============================================================

只能輸出合法 JSON。

不要 Markdown。

不要 ```json。

開場階段：

{
  "story": "...",
  "choices": [
    "...",
    "...",
    "..."
  ]
}

行動階段：

{
  "action_result": "...",
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
  "npcs_add": [],
  "factions_add": [],
  "flags_add": [],
  "flags_remove": [],
  "death": false,
  "arrested": false,
  "listed": false
}

不要輸出其他欄位。

============================================================
【重要】
============================================================

action_result 必須描述完整事件。

不要生成 next_month_story。

下一個月由程式重新呼叫 AI。

這是為了讓遊戲真正按照玩家上一回合的選擇發展。
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

        "love_interest": None,

        "npcs": {},

        "factions": {},

        "flags": [],

        "history": [],

        "current_story": None,

        "current_choices": [],

        "last_action_result": None,

        "game_started": False
    }


# ============================================================
# ⑥ AI JSON 解析
# ============================================================

def clean_json_text(text):

    if not text:
        raise RuntimeError("AI 沒有返回內容。")

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # 嘗試找 JSON 起點
    if not text.startswith("{"):
        start = text.find("{")

        if start >= 0:
            text = text[start:]

    # 嘗試找 JSON 結尾
    if not text.endswith("}"):
        end = text.rfind("}")

        if end >= 0:
            text = text[:end + 1]

    return text.strip()


def parse_ai_json(response):

    text = clean_json_text(
        response.text
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError as e:

        raise RuntimeError(
            "AI 回傳的內容不是合法 JSON。\n\n"
            f"錯誤位置：{e}"
        )


# ============================================================
# ⑦ AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config={
                    "system_instruction": SYSTEM_PROMPT,

                    "temperature": 0.9,

                    "max_output_tokens": 6000,

                    "response_mime_type": "application/json"
                }
            )

            return parse_ai_json(response)

        except Exception as e:

            error_text = str(e)

            if (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < retries - 1:

                    time.sleep(4)
                    continue

                raise RuntimeError(
                    "Gemini API 額度或速率限制。\n\n"
                    "請稍後再試。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    f"Gemini 模型 {MODEL} 無法使用。\n\n"
                    "目前程式設定：\n"
                    f'MODEL = "{MODEL}"'
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
# ⑧ 建立世界摘要
# ============================================================

def build_world_summary(state):

    npcs = state.get(
        "npcs",
        {}
    )

    factions = state.get(
        "factions",
        {}
    )

    npc_text = {}

    for name, npc in npcs.items():

        npc_text[name] = npc

    faction_text = {}

    for name, faction in factions.items():

        faction_text[name] = faction

    return {
        "npcs": npc_text,
        "factions": faction_text,
        "flags": state.get(
            "flags",
            []
        )
    }


# ============================================================
# ⑨ 建立 AI 回合資料
# ============================================================

def build_game_context(state):

    p = state["player"]

    return {
        "current_date": {
            "age": p["age"],
            "month": p["month"]
        },

        "player": p,

        "brothers": state["brothers"],

        "love_interest": state.get(
            "love_interest"
        ),

        "world": build_world_summary(
            state
        ),

        "recent_history": state[
            "history"
        ][-8:],

        "last_action_result": state.get(
            "last_action_result"
        ),

        "current_story": state.get(
            "current_story"
        )
    }


# ============================================================
# ⑩ 生成月份開場
# ============================================================

def generate_month_opening(state):

    context = build_game_context(
        state
    )

    prompt = f"""
現在要生成《地下帝國：AI人生》的
「本月開場」。

這不是玩家行動結果。

玩家現在只是準備開始這個月。

請根據目前世界狀態、過去歷史、
NPC、勢力以及上一回合造成的影響，
生成自然銜接的本月劇情。

目前遊戲資料：

{json.dumps(
    context,
    ensure_ascii=False,
    indent=2
)}

==================================================
要求
==================================================

1. story 是本月開場。

2. 不要直接替玩家做決定。

3. 不要直接結束本月。

4. 必須讓玩家有事情可以做。

5. 劇情不能每月都是大事件。

6. 如果玩家上一個月剛接觸某個人物，
   這個月可以合理延續。

7. 已經認識的 NPC 不要重新介紹成陌生人。

8. 已經發生的事情必須記得。

9. 如果世界中已經存在幫派，
   他們要按照自己的利益活動。

10. story 建議 500～900 字。

11. 必須生成 3 個不同方向的行動。

12. 每個選項都要是玩家「可以做的事情」。

13. 三個選項不能只是換句話說。

14. 玩家仍然可以自由輸入其他行動。

只輸出 JSON。
"""

    result = call_ai(
        prompt
    )

    story = result.get(
        "story",
        "新的一個月開始了。"
    )

    choices = result.get(
        "choices",
        []
    )

    if not isinstance(
        choices,
        list
    ):

        choices = []

    choices = [
        str(x)
        for x in choices[:3]
        if str(x).strip()
    ]

    while len(choices) < 3:

        choices.append(
            "自由決定你接下來要做什麼。"
        )

    state["current_story"] = story

    state["current_choices"] = choices[:3]


# ============================================================
# ⑪ 建立玩家行動 Prompt
# ============================================================

def build_action_prompt(
    state,
    action
):

    context = build_game_context(
        state
    )

    prompt = f"""
玩家現在完成了本月行動。

這一次 AI 必須把玩家的行動「真正演出來」。

不是摘要。

不是一句結果。

不是：

「你去找豹哥，豹哥答應了。」

而是完整描寫事件。

==================================================
目前遊戲資料
==================================================

{json.dumps(
    context,
    ensure_ascii=False,
    indent=2
)}

==================================================
玩家本月行動
==================================================

{action}

==================================================
寫作要求
==================================================

請把這個行動寫成完整黑道人生 RPG 劇情。

必須包含：

1. 玩家實際做了什麼。

2. 玩家去了哪裡。

3. 見到了誰。

4. NPC 對玩家的第一反應。

5. NPC 與玩家的對話。

6. 三兄弟如果在場，
   必須按照各自性格做出反應。

7. 事件中間必須發生事情。

8. NPC 不可以無條件配合玩家。

9. 玩家可能被拒絕、懷疑、試探、
   利用、欺騙或遇到意外。

10. 玩家沒有說出口的事情，
    不要替玩家說。

11. 玩家沒有同意的事情，
    不要替玩家同意。

12. 玩家做出的決定要真正影響事件。

13. 最後才寫出本次行動結果。

14. 結果必須能影響後續世界。

==================================================
【重要】
==================================================

不要寫 next_month_story。

下一個月由下一次 AI 呼叫生成。

不要提前替玩家決定下一個月做什麼。

==================================================
【篇幅】
==================================================

一般行動：

700～1200 字。

重要行動：

1000～1800 字。

重大事件：

1800～2500 字。

內容要有實質劇情。

可以大量使用人物對話。

==================================================
【風格】
==================================================

像長篇黑道小說。

要有：

場景
氣氛
人物
對話
心理
利益
衝突
轉折
結果

例如可以使用：

「豹哥沒有立刻回答。」

「阿豪看了你一眼。」

「阿虎把手插進口袋，顯然已經有些不耐煩。」

不要寫成遊戲說明書。

==================================================
【數值】
==================================================

根據實際劇情更新數值。

不要亂加。

普通事情通常 0～1。

重要事情通常 1～3。

重大事情最多 5 左右。

現金也必須合理。

玩家不能靠一句話突然暴富。

==================================================
【人際】
==================================================

兄弟：

loyalty
trust
respect

依照實際事件調整。

戀愛：

affection
trust
respect

依照實際互動調整。

不要因為普通對話突然大幅增加。

==================================================
【NPC】
==================================================

如果這次劇情產生新的重要 NPC，
可以加入 npcs_add。

格式：

{{
  "name": "人物姓名",
  "description": "人物描述",
  "faction": "所屬勢力",
  "attitude": "對玩家目前態度"
}}

==================================================
【勢力】
==================================================

如果產生新的重要勢力，
可以加入 factions_add。

格式：

{{
  "name": "勢力名稱",
  "power": 20,
  "reputation": 20,
  "attitude": "中立"
}}

==================================================
只輸出合法 JSON。
不要 Markdown。
"""

    return prompt


# ============================================================
# ⑫ 安全數值
# ============================================================

def safe_number(value):

    if isinstance(
        value,
        (int, float)
    ):
        return value

    return 0


# ============================================================
# ⑬ 套用玩家數值
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


# ============================================================
# ⑭ 套用兄弟關係
# ============================================================

def apply_brother_changes(
    state,
    result
):

    brothers = result.get(
        "brothers",
        {}
    )

    for name, data in brothers.items():

        if name not in state["brothers"]:
            continue

        if not isinstance(
            data,
            dict
        ):
            continue

        brother = state[
            "brothers"
        ][name]

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

            brother[field] += value

            brother[field] = max(
                0,
                min(100, brother[field])
            )


# ============================================================
# ⑮ 套用戀愛關係
# ============================================================

def apply_love_changes(
    state,
    result
):

    love_data = result.get(
        "love",
        {}
    )

    if not isinstance(
        love_data,
        dict
    ):
        return

    # 新戀愛角色
    if (
        state["love_interest"] is None
        and
        love_data.get(
            "created",
            False
        )
    ):

        p = state["player"]

        # 不允許開局直接送戀愛角色
        if (
            p["age"] > 18
            or
            p["month"] > 2
        ):

            name = str(
                love_data.get(
                    "name",
                    ""
                )
            ).strip()

            if name:

                state[
                    "love_interest"
                ] = {

                    "name": name,

                    "personality":
                        love_data.get(
                            "personality",
                            "個性獨立"
                        ),

                    "affection": 1,

                    "trust": 1,

                    "respect": 1,

                    "relationship":
                        "認識"
                }

    # 已有戀愛角色
    if state["love_interest"]:

        love = state[
            "love_interest"
        ]

        for field in [
            "affection",
            "trust",
            "respect"
        ]:

            key = field + "_change"

            value = safe_number(
                love_data.get(
                    key,
                    0
                )
            )

            value = max(
                -5,
                min(5, value)
            )

            love[field] += value

            love[field] = max(
                0,
                min(100, love[field])
            )

        affection = love[
            "affection"
        ]

        if affection < 20:

            love[
                "relationship"
            ] = "陌生"

        elif affection < 40:

            love[
                "relationship"
            ] = "認識"

        elif affection < 60:

            love[
                "relationship"
            ] = "朋友"

        elif affection < 75:

            love[
                "relationship"
            ] = "曖昧"

        elif affection < 90:

            love[
                "relationship"
            ] = "交往"

        else:

            love[
                "relationship"
            ] = "深度交往"


# ============================================================
# ⑯ NPC
# ============================================================

def apply_npcs(
    state,
    result
):

    additions = result.get(
        "npcs_add",
        []
    )

    if not isinstance(
        additions,
        list
    ):
        return

    for npc in additions:

        if not isinstance(
            npc,
            dict
        ):
            continue

        name = str(
            npc.get(
                "name",
                ""
            )
        ).strip()

        if not name:
            continue

        if name not in state[
            "npcs"
        ]:

            state[
                "npcs"
            ][name] = {

                "name": name,

                "description":
                    npc.get(
                        "description",
                        ""
                    ),

                "faction":
                    npc.get(
                        "faction",
                        ""
                    ),

                "attitude":
                    npc.get(
                        "attitude",
                        "中立"
                    )
            }


# ============================================================
# ⑰ 勢力
# ============================================================

def apply_factions(
    state,
    result
):

    additions = result.get(
        "factions_add",
        []
    )

    if not isinstance(
        additions,
        list
    ):
        return

    for faction in additions:

        if not isinstance(
            faction,
            dict
        ):
            continue

        name = str(
            faction.get(
                "name",
                ""
            )
        ).strip()

        if not name:
            continue

        if name not in state[
            "factions"
        ]:

            state[
                "factions"
            ][name] = {

                "power":
                    max(
                        0,
                        min(
                            100,
                            int(
                                safe_number(
                                    faction.get(
                                        "power",
                                        10
                                    )
                                )
                            )
                        )
                    ),

                "reputation":
                    max(
                        0,
                        min(
                            100,
                            int(
                                safe_number(
                                    faction.get(
                                        "reputation",
                                        10
                                    )
                                )
                            )
                        )
                    ),

                "attitude":
                    faction.get(
                        "attitude",
                        "中立"
                    )
            }


# ============================================================
# ⑱ Flags
# ============================================================

def apply_flags(
    state,
    result
):

    for flag in result.get(
        "flags_add",
        []
    ):

        if flag not in state[
            "flags"
        ]:

            state[
                "flags"
            ].append(flag)


    for flag in result.get(
        "flags_remove",
        []
    ):

        if flag in state[
            "flags"
        ]:

            state[
                "flags"
            ].remove(flag)


# ============================================================
# ⑲ 結局狀態
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
# ⑳ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業被動產生一些收入
    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            *
            random.randint(
                30,
                100
            )
        )

        p["cash"] += income


    # 已經建立的事業產生少量估值變化
    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            *
            random.randint(
                30,
                100
            )
        )

        p["company_value"] += growth


    # 月份推進
    p["month"] += 1


    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for brother in state[
            "brothers"
        ].values():

            brother["age"] += 1


# ============================================================
# ㉑ 人生記憶
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
            )[-4000:]
    }

    state[
        "history"
    ].append(memory)

    # 保留最近40回合
    if len(
        state["history"]
    ) > 40:

        state[
            "history"
        ] = state[
            "history"
        ][-40:]


# ============================================================
# ㉒ 完整套用 AI 結果
# ============================================================

def apply_result(
    state,
    result,
    action
):

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

    apply_npcs(
        state,
        result
    )

    apply_factions(
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

    add_memory(
        state,
        action,
        result
    )

    state[
        "last_action_result"
    ] = result.get(
        "action_result",
        ""
    )


# ============================================================
# ㉓ 存檔
# ============================================================

def create_save_data(
    state
):

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


def save_game_file(
    state
):

    return json.dumps(
        create_save_data(
            state
        ),
        ensure_ascii=False,
        indent=2
    )


# ============================================================
# ㉔ 讀檔
# ============================================================

def load_game_file(
    uploaded_file
):

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


        # 相容舊存檔

        defaults = {

            "love_interest":
                None,

            "npcs":
                {},

            "factions":
                {},

            "flags":
                [],

            "history":
                [],

            "current_story":
                None,

            "current_choices":
                [],

            "last_action_result":
                None,

            "game_started":
                True
        }


        for key, value in defaults.items():

            if key not in game:

                game[key] = value


        # 玩家欄位補齊

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
# ㉕ CSS
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
        padding: 26px;
        border-radius: 12px;
        border: 1px solid #444;
        line-height: 2;
        font-size: 17px;
        white-space: pre-wrap;
    }

    .result-box {
        padding: 26px;
        border-radius: 12px;
        border: 1px solid #555;
        line-height: 2;
        font-size: 17px;
        white-space: pre-wrap;
    }

    .choice-box {
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 8px;
        border: 1px solid #444;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ㉖ Session
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


state = st.session_state.game

p = state["player"]


# ============================================================
# ㉗ 標題
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
# ㉘ 存檔 / 讀檔
# ============================================================

with st.expander(
    "💾 存檔 / 讀檔"
):

    st.caption(
        "建議每玩幾個月下載一次存檔。"
        "存檔為 JSON，可以重新上傳繼續。"
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
                        "存檔讀取成功。"
                    )

                    time.sleep(0.5)

                    st.rerun()

                except Exception as e:

                    st.error(
                        str(e)
                    )


# ============================================================
# ㉙ 開始遊戲
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

        這不是一條預設好的道路。

        你可以過普通人的生活。

        也可以一步一步接觸地下世界。

        你做出的每個決定，
        都會影響之後的人生。
        """
    )


    if st.button(
        "🎮 開始人生",
        type="primary",
        use_container_width=True
    ):

        state[
            "game_started"
        ] = True

        st.rerun()


    st.stop()


# ============================================================
# ㉚ 結局
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

        st.rerun()


    st.stop()


# ============================================================
# ㉛ 狀態
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
# ㉜ 三兄弟
# ============================================================

with st.expander(
    "👊 三兄弟"
):

    for name, brother in state[
        "brothers"
    ].items():

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
# ㉝ 勢力
# ============================================================

with st.expander(
    "👑 地下勢力"
):

    if not state["factions"]:

        st.caption(
            "目前還沒有正式接觸的地下勢力。"
        )

    else:

        for name, faction in state[
            "factions"
        ].items():

            st.write(
                f"### {name}"
            )

            st.write(
                f"勢力：{faction.get('power', 0)}　"
                f"聲望：{faction.get('reputation', 0)}"
            )

            st.caption(
                f"目前態度："
                f"{faction.get('attitude', '未知')}"
            )


# ============================================================
# ㉞ NPC
# ============================================================

with st.expander(
    "👥 已認識人物"
):

    if not state["npcs"]:

        st.caption(
            "目前還沒有重要人物資料。"
        )

    else:

        for name, npc in state[
            "npcs"
        ].items():

            st.write(
                f"### {name}"
            )

            if npc.get(
                "description"
            ):

                st.write(
                    npc["description"]
                )

            if npc.get(
                "faction"
            ):

                st.caption(
                    f"勢力：{npc['faction']}"
                )

            st.caption(
                f"對玩家態度："
                f"{npc.get('attitude', '未知')}"
            )


# ============================================================
# ㉟ 戀愛
# ============================================================

if state["love_interest"]:

    love = state[
        "love_interest"
    ]

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
            "感情會隨著人生自然發展。"
        )


# ============================================================
# ㊱ 生成本月開場
# ============================================================

if state["current_story"] is None:

    with st.spinner(
        "🤖 AI 正在建立這個月的世界..."
    ):

        try:

            generate_month_opening(
                state
            )

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㊲ 本月劇情
# ============================================================

st.subheader(
    "📖 本月劇情"
)

safe_story = html.escape(
    state["current_story"]
)

st.markdown(
    f"""
    <div class="story-box">
    {safe_story}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ㊳ 三個選項
# ============================================================

st.subheader(
    "🎮 你要怎麼做？"
)


choices = state.get(
    "current_choices",
    []
)


for index, choice in enumerate(
    choices,
    start=1
):

    if st.button(
        f"{index}. {choice}",
        key=f"choice_{p['age']}_{p['month']}_{index}",
        use_container_width=True
    ):

        st.session_state.pending_action = (
            choice
        )

        st.rerun()


# ============================================================
# ㊴ 自由行動
# ============================================================

st.markdown(
    "### 或自己輸入行動"
)


with st.form(
    "action_form",
    clear_on_submit=True
):

    custom_action = st.text_area(

        "你想做什麼？",

        placeholder=(
            "例如：\n"
            "我決定先跟阿豪去了解城南的勢力，"
            "不急著加入任何人。"
        ),

        height=130
    )


    submitted = st.form_submit_button(

        "⚡ 執行自由行動",

        type="primary",

        use_container_width=True
    )


# ============================================================
# ㊵ 判定玩家行動
# ============================================================

pending_action = st.session_state.get(
    "pending_action"
)


selected_action = None


if pending_action:

    selected_action = pending_action

    del st.session_state[
        "pending_action"
    ]


elif submitted:

    if custom_action.strip():

        selected_action = (
            custom_action.strip()
        )


# ============================================================
# ㊶ 執行玩家行動
# ============================================================

if selected_action:

    with st.spinner(
        "🤖 AI 正在演算這次行動..."
    ):

        try:

            prompt = build_action_prompt(
                state,
                selected_action
            )

            result = call_ai(
                prompt
            )

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


    result_text = result.get(
        "action_result",
        "這個行動產生了一些變化。"
    )


    # --------------------------------------------------------
    # 先顯示完整結果
    # --------------------------------------------------------

    st.subheader(
        "🎬 劇情結果"
    )

    safe_result = html.escape(
        result_text
    )

    st.markdown(
        f"""
        <div class="result-box">
        {safe_result}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # 套用結果
    # --------------------------------------------------------

    apply_result(
        state,
        result,
        selected_action
    )


    # --------------------------------------------------------
    # 世界時間推進
    # --------------------------------------------------------

    world_tick(
        state
    )


    # --------------------------------------------------------
    # 清除舊劇情
    #
    # 注意：
    # 不使用 next_month_story。
    #
    # 下一個月會重新呼叫 AI。
    # --------------------------------------------------------

    state["current_story"] = None

    state["current_choices"] = []

    state["last_action_result"] = (
        result_text
    )


    # --------------------------------------------------------
    # 重新整理
    # --------------------------------------------------------

    st.rerun()


# ============================================================
# ㊷ Flags
# ============================================================

with st.expander(
    "🚩 世界事件"
):

    if not state["flags"]:

        st.caption(
            "目前沒有特殊事件旗標。"
        )

    else:

        for flag in state[
            "flags"
        ]:

            st.write(
                f"• {flag}"
            )


# ============================================================
# ㊸ 人生記錄
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
                f"你的行動："
                f"{memory['action']}"
            )

            st.write(
                memory["result"]
            )

            st.divider()


# ============================================================
# ㊹ 重新開始
# ============================================================

st.divider()


if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = (
        new_game()
    )

    st.rerun()
