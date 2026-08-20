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
        "請到 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY。"
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

# 使用較省額度的模型
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """
你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的黑道人生 RPG。

玩家18歲開始，出生於台灣普通家庭。

玩家開局：
現金0
資產0
公司估值0
合法事業0
地下勢力0
聲望0
警方注意度0

玩家不是天選之子。

玩家必須從一個普通人慢慢成長。

遊戲的核心不是正經商業模擬器。

「地下勢力、幫派、地盤、兄弟、黑道勢力、人際關係、利益衝突、權力鬥爭」
是遊戲的重要核心。

可以存在虛構黑道與犯罪劇情。

但不要提供現實世界可以直接執行的犯罪操作、犯罪教學、藏匿證據方法、規避警方技巧或具體暴力操作方法。

犯罪內容應該著重：
事件
人物
衝突
選擇
風險
後果
關係
權力
法律後果。


==================================================
【三兄弟】
==================================================

阿龍：

沉穩、重義氣、保護兄弟。

阿虎：

衝動、好勝、敢冒險。

阿豪：

冷靜、聰明、擅長分析。

三個兄弟不是工具人。

他們有自己的想法。

他們會根據玩家行為改變：
忠誠
信任
尊重

如果玩家做出兄弟無法接受的事情：

忠誠可以下降
信任可以下降
尊重可以下降

如果玩家長期照顧兄弟：

關係可以增加。

不要每次都增加。

要符合事件。


==================================================
【世界規則】
==================================================

每個月是一回合。

但是：

玩家行動結果
與
下一個月劇情

必須完全分開。

這是非常重要的規則。

玩家輸入行動後：

你只能處理「玩家現在這個行動」。

不能直接跳到下一個月。

必須完整描述：

玩家去了哪裡
遇見誰
說了什麼
NPC怎麼回答
兄弟怎麼反應
事情怎麼發展
玩家做出的選擇產生什麼結果
事情最後停在哪裡

然後提供三個合理的下一步選項。

只有玩家按下「繼續下一個月」後，
系統才會進入下一個月。

下一個月的劇情必須重新生成。


==================================================
【劇情風格】
==================================================

劇情不能像新聞摘要。

不要寫：

「你加入了某勢力。」
「事情順利完成。」
「下一個月青幫開始行動。」

這種內容太乾。

必須像小說一樣描述事件過程。

例如：

玩家決定去找某個黑道人物。

應該描述：

玩家怎麼過去
當時環境
門口看到什麼
誰把玩家帶進去
對方正在做什麼
對方怎麼看玩家
雙方談話
玩家說了什麼
對方怎麼回答
兄弟在旁邊的反應
局勢怎麼變化
玩家最後取得什麼結果

人物對話應該自然。

例如：

「青幫的人最近在打聽這條街。」

豹哥沒有馬上回答。

他把手上的菸放到桌邊，抬頭看了你一眼。

「你從哪裡聽來的？」

這類對話可以大量使用。

劇情應該有：

環境
動作
對話
心理
人物反應
事件發展
局勢變化

但是不要每段都寫得過度文青。

要像黑道人生 RPG。


==================================================
【世界不能只圍著玩家轉】
==================================================

世界有自己的運作。

不要每個月都發生大事件。

普通月份：

工作
學習
家庭
朋友
兄弟
日常
小型衝突
小型機會

中型事件：

小型地盤衝突
黑道人物接觸
競爭者
利益衝突
工作機會
商業機會
感情
兄弟矛盾

大型事件：

幫派衝突
地盤爭奪
重要人物
警方調查
重大商業事件
企業危機
地下勢力洗牌
重大人物死亡或離開
媒體事件

大型事件不能連續每個月發生。

玩家弱小時，
不能突然接觸最高層人物。

玩家必須一步一步建立關係。


==================================================
【人物接觸規則】
==================================================

玩家18歲開始只是普通人。

玩家早期主要接觸：

同學
同事
鄰居
小商家
普通朋友
地方人物
小混混
基層幫派成員

玩家逐漸建立勢力後：

小頭目
地方勢力
中層人物
更高層人物

玩家聲望、勢力、人脈提高後，
才可以接觸真正重要的人物。

不能突然認識：

大企業家
高官
政治人物
大型幫派最高領袖
地下世界大人物

如果沒有合理理由。


==================================================
【黑道成長】
==================================================

玩家可以選擇：

正常生活
工作
創業
加入地方勢力
接觸黑道
建立自己的勢力
與其他勢力合作
與其他勢力競爭
建立地盤
處理兄弟關係
處理警方壓力

但成長必須合理。

玩家不能因為一句：

「我決定當老大。」

下一回合就變成老大。

玩家必須經過：

認識
接觸
建立關係
取得信任
完成事情
建立名聲
累積勢力

才能逐步成長。


==================================================
【戀愛】
==================================================

玩家開局沒有女朋友。

不要第一個月直接送女友。

戀愛必須自然發生。

可能：

陌生人
↓
認識
↓
熟悉
↓
朋友
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

拒絕
生氣
失望
離開
主動聯絡
有自己的事情

不要讓戀愛 NPC 永遠圍著玩家。


==================================================
【關係數值】
==================================================

一般 NPC 可以有：

affection
trust
respect
relationship

數值變化必須小。

普通互動：

+0
+1
-1
偶爾 +2

不要一次：

+10
+20

尤其重要人物。

第一次見面通常：

好感 +0
信任 +0
尊重 +1

只有重大事件才能有比較明顯的變化。


==================================================
【玩家自由】
==================================================

玩家可以自由輸入任何合理行動。

不能只限制三個選項。

但是每次行動結果結束後，
必須提供三個建議選項。

玩家仍然可以自己輸入其他行動。

不要替玩家說話。

不要替玩家做重大決定。

不要擅自讓玩家答應事情。

不要擅自讓玩家做出玩家沒有輸入的重大行動。


==================================================
【最重要：行動與下個月分離】
==================================================

玩家輸入：

「我去找豹哥。」

AI必須只生成：

這次去找豹哥的完整過程。

不能生成下一個月。

例如：

玩家到達棋牌社
↓
門口的人攔住
↓
阿龍說話
↓
玩家進去
↓
見到豹哥
↓
雙方對話
↓
豹哥提出問題
↓
玩家回答
↓
豹哥做出決定
↓
玩家離開
↓
事件結果

然後停止。

最後提供：

選項一
選項二
選項三

這三個選項代表「接下來玩家可以做什麼」。

不要執行選項。

不要替玩家選。


==================================================
【下一個月】
==================================================

只有玩家按下「繼續下一個月」後，
才進入下一個月。

下一個月 AI 必須讀取：

上一個月玩家行動
上一個月完整結果
NPC關係變化
兄弟關係
戀愛關係
玩家資產
地下勢力
聲望
警方注意度
flags
歷史記錄

然後生成新的月份開場。

新的月份必須承接上一個月。

例如上一個月：

玩家得罪青幫。

下一個月：

可以出現青幫的人開始打聽玩家。

但不能直接：

「你已經和青幫開戰。」

除非上一個月真的發生了開戰。

世界必須有因果。


==================================================
【AI輸出】
==================================================

第一階段：

只輸出合法 JSON。

格式：

{
  "action_result": "完整劇情",
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
  "listed": false,

  "options": [
    "選項一",
    "選項二",
    "選項三"
  ]
}

第二階段：

只輸出：

{
  "story": "下一個月開場劇情",
  "options": [
    "選項一",
    "選項二",
    "選項三"
  ]
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
        "current_options": [],

        "pending_result": None,

        "game_started": False
    }


# ============================================================
# ⑤ AI 基礎呼叫
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
                    "AI 沒有返回內容。"
                )

            text = response.text.strip()

            if text.startswith("```json"):
                text = text[7:]

            if text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            return json.loads(text)

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
                    f"Gemini 模型 {MODEL} 無法使用。\n\n"
                    "請確認 Gemini API Key 可以使用此模型。"
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
# ⑥ 建立「玩家行動」Prompt
# ============================================================

def build_action_prompt(state, action):

    p = state["player"]

    data = {

        "phase": "ACTION_RESULT",

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

        "player_action": action,

        "task": """
玩家剛剛輸入了一個行動。

你現在只能處理這個行動。

絕對不要生成下一個月。

絕對不要直接跳時間。

必須把玩家這次行動完整演出來。

劇情至少應該包含：

1. 玩家怎麼開始行動
2. 去了哪裡
3. 遇見誰
4. 現場環境
5. 人物對話
6. NPC反應
7. 兄弟反應
8. 事件如何發展
9. 玩家行動造成的結果
10. 最後留下什麼局勢

劇情要有小說感。

不要寫成摘要。

不要只寫三四句。

要有完整過程。

玩家沒有輸入的重大決定，
不要替玩家做。

例如玩家說：

「我要去找豹哥。」

不要直接寫：

「你成功加入豹哥。」

而應該描述：

你怎麼去
誰攔你
你怎麼進去
豹哥問什麼
你如何表達
豹哥如何反應
兄弟怎麼看
最後得到什麼結果

事件結果必須合理。

不要讓玩家永遠成功。

不要讓普通人突然擁有巨大勢力。

不要讓玩家突然暴富。

不要突然認識最高層人物。

如果玩家做的是普通事情，
就產生普通但有內容的劇情。

如果玩家做的是黑道相關行動，
可以發生幫派、地盤、人物、利益與權力衝突。

但是不要提供現實犯罪操作教學。

最後一定要提供三個合理的下一步選項。

這三個選項只代表玩家接下來可以做什麼。

不要替玩家選。

不要執行選項。

重要：

「action_result」只能描述這次行動。

不能包含下一個月劇情。
"""
    }

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑦ 建立「下一個月」Prompt
# ============================================================

def build_next_month_prompt(state):

    p = state["player"]

    data = {

        "phase": "NEXT_MONTH",

        "current_date": {
            "age": p["age"],
            "month": p["month"]
        },

        "player": p,

        "brothers": state["brothers"],

        "love_interest": state["love_interest"],

        "flags": state["flags"],

        "recent_history": state["history"][-12:],

        "previous_action_result": (
            state["pending_result"]
            if state["pending_result"]
            else None
        ),

        "task": """
現在玩家已經按下「繼續下一個月」。

請正式進入下一個月。

你現在才可以推進時間。

請根據上一個月真正發生的事情，
生成新的月份開場劇情。

必須有因果。

如果上一個月玩家只是找工作，
下一個月就不要突然爆發幫派大戰。

如果上一個月玩家開始接觸地方勢力，
下一個月可以慢慢出現新的接觸。

如果上一個月發生衝突，
下一個月可以出現後續影響。

世界要自然運作。

不要每個月都重大事件。

劇情要像小說。

至少包含：

環境
人物
對話
事件
NPC反應
局勢

不要直接總結成：

「你成功了。」

要讓玩家真正看到事情怎麼開始。

最後提供三個玩家可以選擇的行動。

不要執行這三個選項。

不要替玩家做決定。
"""
    }

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑧ 安全數值
# ============================================================

def safe_number(value):

    if isinstance(value, (int, float)):
        return value

    return 0


# ============================================================
# ⑨ 套用數值
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

            key = field + "_change"

            value = safe_number(
                love_data.get(key, 0)
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
# ⑩ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

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

    p["month"] += 1

    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for b in state["brothers"].values():
            b["age"] += 1


# ============================================================
# ⑪ 人生記憶
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

    state["history"].append(
        memory
    )

    if len(state["history"]) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑫ 存檔
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

        if "current_options" not in game:
            game["current_options"] = []

        if "pending_result" not in game:
            game["pending_result"] = None

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
# ⑬ CSS
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
# ⑭ Session
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()

state = st.session_state.game

p = state["player"]


# ============================================================
# ⑮ 標題
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
# ⑯ 存檔 / 讀檔
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

                    st.error(
                        str(e)
                    )


# ============================================================
# ⑰ 開始遊戲
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

        你可以過普通人的生活。

        也可以一步一步踏入地下世界。

        你的每個選擇都可能改變未來。
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
# ⑱ 結局
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
# ⑲ 狀態
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
# ⑳ 三兄弟
# ============================================================

with st.expander("👊 三兄弟"):

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
# ㉑ 戀愛
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
# ㉒ 第一個月開場
# ============================================================

if state["current_story"] is None:

    with st.spinner(
        "🤖 AI 正在建立你的世界..."
    ):

        try:

            prompt = json.dumps({

                "phase": "NEW_GAME",

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

                "task": """
生成18歲第1個月開場劇情。

玩家只是普通人。

沒有錢。
沒有勢力。
沒有背景。

不要直接認識大人物。

可以從：

工作
朋友
兄弟
家庭
地方生活
小型事件

開始。

如果有黑道元素，
必須從很小的接觸開始。

劇情要有完整場景與人物對話。

不要只寫摘要。

最後提供三個玩家行動選項。

只生成開場。

不要執行任何選項。
"""
            }, ensure_ascii=False)

            result = call_ai(prompt)

            state["current_story"] = result.get(
                "story",
                "你的故事即將開始。"
            )

            state["current_options"] = result.get(
                "options",
                []
            )

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉓ 本月劇情
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
# ㉔ AI 建議選項
# ============================================================

if state["current_options"]:

    st.subheader(
        "🎮 你可以選擇"
    )

    for i, option in enumerate(
        state["current_options"][:3],
        start=1
    ):

        st.markdown(
            f"""
            <div class="option-box">
            <b>{i}.</b> {option}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ㉕ 玩家行動
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
            "可以自由輸入。\n\n"
            "例如：\n"
            "我決定先去附近打聽青幫的消息，"
            "再和阿豪討論這件事情。"
        ),

        height=140
    )

    submitted = st.form_submit_button(

        "⚡ 執行行動",

        type="primary",

        use_container_width=True
    )


# ============================================================
# ㉖ 執行玩家行動
# ============================================================

if submitted:

    if not action.strip():

        st.warning(
            "請先輸入你的行動。"
        )

        st.stop()

    with st.spinner(
        "🤖 AI 正在演算你的行動..."
    ):

        try:

            prompt = build_action_prompt(
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
    # 儲存結果
    # ========================================================

    state["pending_result"] = result


    # ========================================================
    # 套用數值
    # ========================================================

    apply_changes(
        state,
        result
    )


    # ========================================================
    # 人生記憶
    # ========================================================

    add_memory(
        state,
        action,
        result
    )


    # ========================================================
    # 清除舊選項
    # ========================================================

    state["current_options"] = []

    st.rerun()


# ============================================================
# ㉗ 顯示行動結果
# ============================================================

if state["pending_result"]:

    result = state["pending_result"]

    st.divider()

    st.subheader(
        "🎬 劇情結果"
    )

    result_text = result.get(
        "action_result",
        "這個行動產生了一些變化。"
    )

    st.markdown(

        f'<div class="result-box">'
        f'{result_text}'
        f'</div>',

        unsafe_allow_html=True
    )


    # ========================================================
    # 關係變化
    # ========================================================

    changes = result.get(
        "changes",
        {}
    )

    relationship_changes = []

    for field, label in [

        ("cash_change", "現金"),

        ("assets_change", "資產"),

        ("company_value_change", "公司估值"),

        ("legal_business_change", "合法事業"),

        ("power_change", "地下勢力"),

        ("reputation_change", "聲望"),

        ("police_attention_change", "警方注意度"),

        ("health_change", "健康")

    ]:

        value = safe_number(
            changes.get(field, 0)
        )

        if value != 0:

            relationship_changes.append(
                f"{label}: "
                f"{'+' if value > 0 else ''}{value}"
            )


    brothers_result = result.get(
        "brothers",
        {}
    )

    for name in [
        "阿龍",
        "阿虎",
        "阿豪"
    ]:

        data = brothers_result.get(
            name,
            {}
        )

        for field, label in [

            ("loyalty_change", "忠誠"),

            ("trust_change", "信任"),

            ("respect_change", "尊重")

        ]:

            value = safe_number(
                data.get(field, 0)
            )

            if value != 0:

                relationship_changes.append(
                    f"{name} {label}: "
                    f"{'+' if value > 0 else ''}{value}"
                )


    if relationship_changes:

        st.subheader(
            "📊 本次變化"
        )

        for item in relationship_changes:

            st.write(
                item
            )


    # ========================================================
    # 三個下一步選項
    # ========================================================

    options = result.get(
        "options",
        []
    )

    if options:

        st.subheader(
            "🔀 下一步"
        )

        for i, option in enumerate(
            options[:3],
            start=1
        ):

            st.write(
                f"**{i}.** {option}"
            )

    st.divider()

    st.info(
        "本次行動已經結束。"
        "選項只是建議，不會自動替你選擇。"
    )

    # ========================================================
    # 繼續下一個月
    # ========================================================

    if st.button(
        "▶️ 繼續下一個月",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🤖 世界正在進入下一個月..."
        ):

            try:

                # 先推進時間
                world_tick(state)

                # 生成真正的下一個月
                prompt = build_next_month_prompt(
                    state
                )

                next_result = call_ai(
                    prompt
                )

                state["current_story"] = next_result.get(
                    "story",
                    "新的一個月開始了。"
                )

                state["current_options"] = next_result.get(
                    "options",
                    []
                )

                # 清掉上一回合結果
                state["pending_result"] = None

                st.rerun()

            except Exception as e:

                st.error(
                    str(e)
                )

                st.stop()


# ============================================================
# ㉘ 人生記錄
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
# ㉙ 重新開始
# ============================================================

st.divider()

if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = new_game()

    st.rerun()
