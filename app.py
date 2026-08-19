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
    st.info("請到 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY。")
    st.stop()


client = genai.Client(api_key=API_KEY)

# 你目前測試成功的模型
MODEL = "gemini-3.6-flash"


# ============================================================
# ③ Gemini 呼叫器
# ============================================================

def call_gemini(
    prompt,
    system_instruction,
    json_mode=False,
    max_retries=2
):

    last_error = None

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
                raise RuntimeError("AI 沒有返回內容")

            return response.text.strip()

        except Exception as e:

            last_error = e

            error_text = str(e)

            temporary_error = (
                "503" in error_text
                or "429" in error_text
                or "500" in error_text
                or "UNAVAILABLE" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
                or "TIMEOUT" in error_text.upper()
            )

            if not temporary_error:
                raise

            if attempt < max_retries - 1:
                time.sleep(1)

    raise RuntimeError(
        f"Gemini 暫時無法使用：{last_error}"
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

        "flags": [],

        "history": [],

        "current_story": None,

        "choices": [],

        "game_started": False
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

    state["love_interest"] = random.choice(candidates)


# ============================================================
# ⑥ 主劇情 Prompt
# ============================================================

SYSTEM_PROMPT = r"""
你是「地下帝國：AI人生」的遊戲主持人。

這是一個長篇虛構人生 RPG。

玩家18歲開始，出生於台灣。

玩家沒有錢、資產與背景。

玩家有三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。

世界不是遊戲任務清單。

這是一個會自己運轉的人生世界。

NPC 有自己的：

性格
利益
恐懼
目標
家庭
朋友
人際關係

NPC 可以：

幫助玩家
拒絕玩家
欺騙玩家
嫉妒玩家
離開玩家
與玩家產生衝突

三兄弟不是工具人。

玩家如果做出兄弟不能接受的事情，
忠誠與信任可以下降。

戀愛角色也不是數值機器。

她們有：

自己的生活
工作
夢想
家庭
朋友
底線

世界不會只圍著玩家轉。

可能出現：

工作
學習
家庭
朋友
商業
投資
公司
合法事業
競爭者
警方
律師
記者
投資人
地下勢力
戀愛
失戀
結婚
社會事件

人生可能：

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
公司上市

劇情節奏：

不要每個月都是大事件。

有些月份只是普通生活。

有些月份會出現小機會。

有些月份才會出現重大事件。

重大事件不能連續發生。

劇情要有長期伏筆。

角色要記得以前發生過的事情。

玩家的選擇會影響未來。

犯罪內容只能是虛構劇情與抽象結果。

不要提供現實世界可以直接執行的犯罪方法。

【輸出格式】

請只輸出以下 JSON：

{
    "story": "本月劇情，約250～400字，有自然對話",
    "choices": [
        "選項一",
        "選項二",
        "選項三"
    ]
}

不要輸出 Markdown。

不要輸出 ```。

不要在 JSON 外面加其他文字。

不要替玩家做重大決定。

不要替玩家說話。
"""


# ============================================================
# ⑦ 生成劇情
# ============================================================

def generate_story(state):

    recent_history = state["history"][-5:]

    data = {

        "player": state["player"],

        "brothers": state["brothers"],

        "love_interest":
            state["love_interest"],

        "flags":
            state["flags"],

        "recent_history":
            recent_history,

        "task":
            "請生成下一個月的人生事件。"
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    text = call_gemini(
        prompt,
        SYSTEM_PROMPT,
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

        data = json.loads(text)

        story = data.get(
            "story",
            "這個月沒有發生特別重大的事情。"
        )

        choices = data.get(
            "choices",
            [
                "觀察情況",
                "和兄弟商量",
                "尋找新的機會"
            ]
        )

        if not isinstance(choices, list):
            choices = [
                "觀察情況",
                "和兄弟商量",
                "尋找新的機會"
            ]

        choices = choices[:3]

        while len(choices) < 3:
            choices.append("自由行動")

        return story, choices

    except Exception:

        return (
            text,
            [
                "先觀察情況",
                "和兄弟商量",
                "尋找新的機會"
            ]
        )


# ============================================================
# ⑧ 行動結果 Prompt
# ============================================================

RESULT_PROMPT = r"""
你是「地下帝國：AI人生」的劇情裁判。

玩家剛剛做了一個行動。

根據：

玩家目前狀態
三兄弟狀態
戀愛狀態
最近歷史
本月劇情
玩家行動

判斷合理結果。

玩家不一定成功。

可能：

成功
部分成功
失敗
遇到意外
改變 NPC 關係
產生未來伏筆

不要讓玩家自動成功。

不要突然讓玩家變成世界首富。

不要替玩家做下一個重大決定。

結果控制在約150～300字。

犯罪內容只能停留在虛構與抽象層次。

只輸出劇情文字。
"""


# ============================================================
# ⑨ 行動判定
# ============================================================

def resolve_action(
    state,
    action
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

        "recent_history":
            state["history"][-5:],

        "current_story":
            state["current_story"],

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
# ⑩ 數值判定
# ============================================================

STATE_PROMPT = r"""
你是 RPG 數值判定器。

根據玩家行動與劇情結果，
判斷合理的數值變化。

只輸出 JSON。

格式：

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

普通事件的變化通常控制在 -10 到 +10。

不要因為玩家一次普通行動就得到巨大財富。

只有重大事件才可以產生重大變化。

不要讓數值無理由暴增。
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
# ⑪ 套用數值
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


    # --------------------------------------------------------
    # 兄弟
    # --------------------------------------------------------

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
            min(100, b["loyalty"])
        )

        b["trust"] = max(
            0,
            min(100, b["trust"])
        )


    # --------------------------------------------------------
    # 戀愛
    # --------------------------------------------------------

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
            min(100, love["affection"])
        )

        love["trust"] = max(
            0,
            min(100, love["trust"])
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


    # --------------------------------------------------------
    # 世界旗標
    # --------------------------------------------------------

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
# ⑫ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業收入
    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            * random.randint(100, 300)
        )

        p["cash"] += income


    # 公司自然成長
    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            * random.randint(100, 500)
        )

        p["company_value"] += growth


    # 直接進下一個月
    p["month"] += 1


    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for b in state["brothers"].values():
            b["age"] += 1


# ============================================================
# ⑬ 記憶
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


    # 保留最近20回合
    if len(state["history"]) > 20:

        state["history"] = (
            state["history"][-20:]
        )


# ============================================================
# ⑭ CSS
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
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #444;
        line-height: 1.8;
        font-size: 17px;
        margin-bottom: 15px;
    }

    .choice-button {
        margin-top: 5px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ⑮ Session 初始化
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


if "last_result" not in st.session_state:

    st.session_state.last_result = None


if "input_key" not in st.session_state:

    st.session_state.input_key = 0


state = st.session_state.game

p = state["player"]


# ============================================================
# ⑯ 標題
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
# ⑰ 開始遊戲
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

        **你不想永遠只是個普通人。**
        """
    )


    if st.button(
        "🎮 開始人生",
        type="primary",
        use_container_width=True
    ):

        state["game_started"] = True

        try:

            with st.spinner(
                "🤖 正在建立你的人生..."
            ):

                create_love_interest(state)

                story, choices = generate_story(
                    state
                )

                state["current_story"] = story
                state["choices"] = choices

            st.rerun()

        except Exception as e:

            st.error(
                "AI 暫時沒有回應。"
            )

            with st.expander("查看錯誤資訊"):

                st.code(
                    str(e)
                )

            if st.button(
                "🔄 重試"
            ):

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
        "重新開始"
    ):

        st.session_state.game = new_game()

        st.session_state.last_result = None

        st.rerun()

    st.stop()


if p["arrested"]:

    st.error(
        "🚔 你被警方逮捕。"
    )

    st.write(
        "你的故事在這裡結束。"
    )

    if st.button(
        "重新開始"
    ):

        st.session_state.game = new_game()

        st.session_state.last_result = None

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

        st.session_state.last_result = None

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
            f"性格：{love['personality']}"
        )

        st.write(
            f"夢想：{love['dream']}"
        )


# ============================================================
# ㉒ 劇情
# ============================================================

if state["current_story"] is None:

    with st.spinner(
        "🤖 正在生成劇情..."
    ):

        try:

            if state["love_interest"] is None:
                create_love_interest(state)

            story, choices = generate_story(
                state
            )

            state["current_story"] = story
            state["choices"] = choices

        except Exception as e:

            st.error(
                "AI 暫時沒有回應。"
            )

            with st.expander(
                "查看錯誤資訊"
            ):

                st.code(
                    str(e)
                )

            if st.button(
                "🔄 重試劇情"
            ):

                st.rerun()

            st.stop()


# ============================================================
# ㉓ 顯示本月劇情
# ============================================================

st.subheader("📖 本月劇情")

st.markdown(
    f"""
    <div class="story-box">
        {state["current_story"]}
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ㉔ 快速選項
# ============================================================

st.subheader("🎮 你的行動")


choices = state.get(
    "choices",
    []
)


if choices:

    st.caption(
        "快速選擇"
    )

    choice_cols = st.columns(
        len(choices)
    )


    for i, choice in enumerate(choices):

        with choice_cols[i]:

            if st.button(
                choice,
                key=f"choice_{p['age']}_{p['month']}_{i}",
                use_container_width=True
            ):

                st.session_state.pending_action = choice

                st.rerun()


# ============================================================
# ㉕ 自由輸入
# ============================================================

current_input_key = (
    f"action_{st.session_state.input_key}"
)


action = st.text_area(
    "或者自己輸入行動",
    placeholder="例如：我先和阿豪討論，再決定要不要接受這個機會。",
    height=100,
    key=current_input_key
)


# ============================================================
# ㉖ 決定實際行動
# ============================================================

pending_action = st.session_state.get(
    "pending_action",
    None
)


if pending_action:

    action = pending_action


# ============================================================
# ㉗ 執行行動
# ============================================================

execute = st.button(
    "⚡ 執行行動",
    type="primary",
    use_container_width=True
)


if execute or pending_action:

    if not action or not action.strip():

        st.warning(
            "請先輸入你的行動。"
        )

        st.stop()


    # 防止同一個 pending_action 重複執行
    st.session_state.pending_action = None


    try:

        # ----------------------------------------------------
        # 1. AI 判定玩家行動
        # ----------------------------------------------------

        with st.spinner(
            "🤖 AI 正在判定你的行動..."
        ):

            result = resolve_action(
                state,
                action
            )


        # ----------------------------------------------------
        # 2. AI 更新數值
        # ----------------------------------------------------

        with st.spinner(
            "🎲 正在更新世界..."
        ):

            changes = calculate_changes(
                state,
                action,
                result
            )

            apply_changes(
                state,
                changes
            )


        # ----------------------------------------------------
        # 3. 保存記憶
        # ----------------------------------------------------

        add_memory(
            state,
            action,
            result
        )


        # ----------------------------------------------------
        # 4. 直接進下一個月
        # ----------------------------------------------------

        world_tick(
            state
        )


        # ----------------------------------------------------
        # 5. 清除上一個月內容
        # ----------------------------------------------------

        state["current_story"] = None
        state["choices"] = []

        st.session_state.last_result = result


        # ----------------------------------------------------
        # 6. 產生下一個月
        # ----------------------------------------------------

        with st.spinner(
            f"📅 {p['age']}歲・第{p['month']}個月..."
        ):

            story, choices = generate_story(
                state
            )

            state["current_story"] = story
            state["choices"] = choices


        # ----------------------------------------------------
        # 7. 清空輸入框
        # ----------------------------------------------------

        st.session_state.input_key += 1


        # ----------------------------------------------------
        # 8. 直接重新整理
        # ----------------------------------------------------

        st.rerun()


    except Exception as e:

        st.error(
            "這次行動處理失敗，遊戲狀態沒有被重置。"
        )

        with st.expander(
            "查看錯誤資訊"
        ):

            st.code(
                str(e)
            )


        if st.button(
            "🔄 重試這次行動"
        ):

            st.session_state.pending_action = action

            st.rerun()


# ============================================================
# ㉘ 上一回合結果
# ============================================================

if st.session_state.last_result:

    with st.expander(
        "📜 上一回合結果"
    ):

        st.write(
            st.session_state.last_result
        )


# ============================================================
# ㉙ 重新開始
# ============================================================

st.divider()


if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = new_game()

    st.session_state.last_result = None

    st.session_state.pending_action = None

    st.session_state.input_key += 1

    st.rerun()
