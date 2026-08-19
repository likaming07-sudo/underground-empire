````python
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

    # 防止 API Key 前後有空白或換行
    API_KEY = str(API_KEY).strip()

except Exception:
    API_KEY = None


if not API_KEY:
    st.error("找不到 GEMINI_API_KEY")
    st.info(
        "請到 Streamlit Cloud → Settings → Secrets "
        "設定 GEMINI_API_KEY。"
    )
    st.stop()


client = genai.Client(
    api_key=API_KEY
)

MODEL = "gemini-3.6-flash"


# ============================================================
# ③ Gemini 呼叫器
# ============================================================

def call_gemini(
    prompt,
    system_instruction,
    json_mode=False,
    max_retries=3
):

    for attempt in range(max_retries):

        try:

            config = {
                "system_instruction": system_instruction,
                "temperature": 0.8,
            }

            if json_mode:
                config["response_mime_type"] = "application/json"

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config
            )

            if not response.text:
                raise RuntimeError(
                    "Gemini 沒有返回文字"
                )

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

            if attempt < max_retries - 1:

                time.sleep(
                    1 + attempt
                )

    raise RuntimeError(
        "Gemini 目前無法使用，請稍後再試。"
    )


# ============================================================
# ④ 新遊戲
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
                    "沉穩、重義氣、保護兄弟"
            },

            "阿虎": {

                "age": 18,
                "loyalty": 78,
                "trust": 70,
                "ability": 75,

                "alive": True,

                "personality":
                    "衝動、好勝、敢冒險"
            },

            "阿豪": {

                "age": 18,
                "loyalty": 92,
                "trust": 85,
                "ability": 58,

                "alive": True,

                "personality":
                    "冷靜、聰明、擅長分析"
            }
        },

        "love_interest": None,

        "flags": [],

        "history": [],

        "current_story": None,

        "game_started": False,

        "last_result": None
    }


# ============================================================
# ⑤ 戀愛 NPC
# ============================================================

def create_love_interest(state):

    if state["love_interest"]:
        return

    candidates = [

        {
            "name": "林雨晴",
            "personality": "聰明、溫柔、獨立",
            "likes": ["誠實", "陪伴", "責任感"],
            "dislikes": ["欺騙", "失約"],
            "dream": "開一家自己的咖啡店",
            "affection": 10,
            "trust": 10,
            "relationship": "陌生"
        },

        {
            "name": "陳若涵",
            "personality": "活潑、勇敢、喜歡冒險",
            "likes": ["自由", "冒險", "幽默"],
            "dislikes": ["控制", "無聊"],
            "dream": "環遊世界",
            "affection": 10,
            "trust": 10,
            "relationship": "陌生"
        },

        {
            "name": "許雅婷",
            "personality": "成熟、理性、有原則",
            "likes": ["穩定", "誠實", "上進"],
            "dislikes": ["謊言", "不負責任"],
            "dream": "建立自己的事業",
            "affection": 10,
            "trust": 10,
            "relationship": "陌生"
        }
    ]

    state["love_interest"] = random.choice(
        candidates
    )


# ============================================================
# ⑥ 主劇情 Prompt
# ============================================================

SYSTEM_PROMPT = """
你是「地下帝國：AI人生」的遊戲主持人。

這是一個長篇虛構人生 RPG。

玩家18歲開始，出生於台灣，沒有錢、資產或背景。

三個兄弟：

阿龍：沉穩、重義氣、保護兄弟。
阿虎：衝動、好勝、敢冒險。
阿豪：冷靜、聰明、擅長分析。

每個月是一回合。

NPC 有自己的性格、利益、恐懼、目標。
NPC 可以幫助、拒絕、欺騙或離開玩家。

世界不會只圍著玩家轉。

事件可以包含：
日常、工作、學習、商業、公司、投資、家庭、
感情、警方、媒體、競爭者、朋友、敵人。

事件大小要有變化。
不要每個月都是大事件。

玩家可能成功，也可能失敗。

犯罪內容只能是虛構與抽象結果，
不要提供現實世界可執行的犯罪方法。

請直接輸出：

【劇情】

約300～500字。
必須有自然對話。

【目前狀況】

3～5行。

【你的選擇】

1. 選項
2. 選項
3. 選項

玩家可以自由輸入行動。

不要替玩家說話。
不要替玩家做重大決定。
"""


# ============================================================
# ⑦ 生成劇情
# ============================================================

def generate_story(state):

    recent_history = state["history"][-4:]

    data = {

        "player": state["player"],

        "brothers": state["brothers"],

        "love_interest":
            state["love_interest"],

        "flags": state["flags"],

        "recent_history":
            recent_history,

        "task":
            "生成下一個月的新事件。"
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    return call_gemini(
        prompt,
        SYSTEM_PROMPT,
        max_retries=2
    )


# ============================================================
# ⑧ 行動結果
# ============================================================

RESULT_PROMPT = """
你是「地下帝國：AI人生」的劇情裁判。

根據玩家目前狀態、本月劇情與玩家行動，
判斷合理結果。

玩家不一定成功。

結果可以是：
成功、部分成功、失敗、意外、
NPC關係改變、產生未來伏筆。

不要讓玩家自動成功。
不要突然讓玩家成為世界首富。

犯罪內容只能是虛構與抽象結果。

輸出約200～400字。
不要替玩家做下一個重大決定。
"""


def resolve_action(
    state,
    action,
    current_story
):

    data = {

        "player":
            state["player"],

        "brothers":
            state["brothers"],

        "love_interest":
            state["love_interest"],

        "flags":
            state["flags"],

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
        RESULT_PROMPT,
        max_retries=2
    )


# ============================================================
# ⑨ 數值判定
# ============================================================

STATE_PROMPT = """
你是 RPG 數值判定器。

根據玩家行動與劇情結果，
判斷合理數值變化。

只輸出 JSON：

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

一般事件數值變化控制在 -10 到 +10。

不要突然增加大量金錢或勢力。
"""


def calculate_changes(
    state,
    action,
    story
):

    data = {

        "player":
            state["player"],

        "brothers":
            state["brothers"],

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
        json_mode=True,
        max_retries=2
    )

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:

        return json.loads(text)

    except Exception:

        return {}


# ============================================================
# ⑩ 套用數值
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


    # -------------------------
    # 兄弟
    # -------------------------

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


    # -------------------------
    # 戀愛
    # -------------------------

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


    # -------------------------
    # Flag
    # -------------------------

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

            state["flags"].remove(
                flag
            )


    # -------------------------
    # 結局
    # -------------------------

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
# ⑪ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業自然收入
    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            * random.randint(
                80,
                180
            )
        )

        p["cash"] += income


    # 公司成長
    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            * random.randint(
                100,
                300
            )
        )

        p["company_value"] += growth


    # 下一個月
    p["month"] += 1


    # 跨年
    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for b in state["brothers"].values():

            b["age"] += 1


# ============================================================
# ⑫ 記憶
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
            story[-1800:]
    }

    state["history"].append(
        memory
    )


    if len(
        state["history"]
    ) > 20:

        state["history"] = (
            state["history"][-20:]
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
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 25px;
    }

    .story-box {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #444;
        line-height: 1.8;
        font-size: 17px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ⑭ Session 初始化
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
    '<div class="subtitle">AI 驅動的人生模擬 RPG</div>',
    unsafe_allow_html=True
)


# ============================================================
# ⑯ 開始遊戲
# ============================================================

if not state["game_started"]:

    st.markdown(
        """
        ## 你的故事開始了

        你出生於台灣。

        沒有富裕家庭。
        沒有資產。
        沒有背景。

        18歲這一年，你身上只有：

        ### 💰 $0

        但你有三個從小一起長大的兄弟：

        - **阿龍**：沉穩、重義氣
        - **阿虎**：衝動、敢冒險
        - **阿豪**：冷靜、擅長分析

        沒有人知道未來會發生什麼。

        你只知道一件事情：

        **你不想永遠只是個普通人。**
        """
    )


    if st.button(
        "🎮 開始人生",
        type="primary"
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
        "重新開始"
    ):

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


if p["arrested"]:

    st.error(
        "🚔 你被警方逮捕。"
    )

    st.write(
        "你的地下帝國迎來終點。"
    )

    if st.button(
        "重新開始"
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
        "重新開始"
    ):

        st.session_state.game = new_game()

        st.rerun()

    st.stop()


# ============================================================
# ⑱ 狀態欄
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

with st.expander(
    "👊 三兄弟"
):

    for name, b in state["brothers"].items():

        st.write(
            f"**{name}**"
        )

        st.write(
            f"忠誠：{b['loyalty']}　"
            f"信任：{b['trust']}　"
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
            f"性格：{love['personality']}"
        )

        st.write(
            f"夢想：{love['dream']}"
        )


# ============================================================
# ㉑ 生成本月劇情
# ============================================================

if state["current_story"] is None:

    if (
        state["love_interest"] is None
        and random.random() < 0.25
    ):

        create_love_interest(
            state
        )


    with st.spinner(
        "🤖 AI 正在生成本月劇情..."
    ):

        try:

            state["current_story"] = (
                generate_story(state)
            )

        except Exception as e:

            st.error(
                f"Gemini 發生錯誤：{e}"
            )

            st.stop()


# ============================================================
# ㉒ 顯示劇情
# ============================================================

st.subheader(
    "📖 本月劇情"
)

st.markdown(
    f"""
    <div class="story-box">
    {state["current_story"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ㉓ 玩家行動
# ============================================================

st.subheader(
    "🎮 你的行動"
)


action = st.text_area(
    "你想做什麼？",
    placeholder=
        "例如：我先和阿豪討論這件事情，再決定下一步。",
    height=120
)


if st.button(
    "⚡ 執行行動",
    type="primary"
):

    if not action.strip():

        st.warning(
            "請輸入你的行動。"
        )

    else:

        # ====================================================
        # A. 判定行動
        # ====================================================

        with st.spinner(
            "🤖 AI 正在判定你的行動..."
        ):

            try:

                result = resolve_action(
                    state,
                    action,
                    state["current_story"]
                )

            except Exception as e:

                st.error(
                    f"Gemini 發生錯誤：{e}"
                )

                st.stop()


        # ====================================================
        # B. 更新數值
        # ====================================================

        with st.spinner(
            "🎲 正在更新世界..."
        ):

            try:

                changes = calculate_changes(
                    state,
                    action,
                    result
                )

                apply_changes(
                    state,
                    changes
                )

            except Exception as e:

                st.error(
                    f"數值更新失敗：{e}"
                )

                st.stop()


        # ====================================================
        # C. 儲存記憶
        # ====================================================

        add_memory(
            state,
            action,
            result
        )


        # ====================================================
        # D. 直接進入下一個月
        # ====================================================

        world_tick(
            state
        )


        # 保存這次結果
        state["last_result"] = result

        # 清掉舊劇情
        state["current_story"] = None

        # 清掉輸入
        state["current_action"] = ""


        # ====================================================
        # E. 直接重新整理
        # ====================================================

        st.rerun()


# ============================================================
# ㉔ 顯示上一回合結果
# ============================================================

if state.get(
    "last_result"
):

    st.divider()

    st.subheader(
        "🎬 上個月發生的事"
    )

    st.markdown(
        f"""
        <div class="story-box">
        {state["last_result"]}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ㉕ 重新開始
# ============================================================

st.divider()


if st.button(
    "🔄 重新開始人生"
):

    st.session_state.game = new_game()

    st.rerun()
````
