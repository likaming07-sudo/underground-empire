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
        "請到 Streamlit Cloud → 你的 App → Settings → Secrets "
        "設定 GEMINI_API_KEY。"
    )
    st.stop()


client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


# ============================================================
# ③ Gemini AI 呼叫器
# ============================================================

def call_gemini(
    prompt,
    system_instruction,
    json_mode=False,
    max_retries=5
):

    for attempt in range(max_retries):

        try:

            prompt_part = types.Part.from_text(
                text=str(prompt)
            )

            system_part = types.Part.from_text(
                text=str(system_instruction)
            )

            config_kwargs = {
                "system_instruction": [system_part],
                "temperature": 0.9,
            }

            if json_mode:
                config_kwargs["response_mime_type"] = "application/json"

            config = types.GenerateContentConfig(
                **config_kwargs
            )

            response = client.models.generate_content(
                model=MODEL,
                contents=[prompt_part],
                config=config
            )

            if response.text:
                return response.text.strip()

            raise RuntimeError(
                "Gemini 沒有返回文字"
            )

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

                wait_time = min(
                    2 ** attempt,
                    10
                )

                time.sleep(wait_time)

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

        "current_action": "",

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
            "likes": [
                "誠實",
                "陪伴",
                "責任感"
            ],
            "dislikes": [
                "欺騙",
                "失約"
            ],
            "dream": "開一家自己的咖啡店",
            "affection": 10,
            "trust": 10,
            "relationship": "陌生"
        },

        {
            "name": "陳若涵",
            "personality": "活潑、勇敢、喜歡冒險",
            "likes": [
                "自由",
                "冒險",
                "幽默"
            ],
            "dislikes": [
                "控制",
                "無聊"
            ],
            "dream": "環遊世界",
            "affection": 10,
            "trust": 10,
            "relationship": "陌生"
        },

        {
            "name": "許雅婷",
            "personality": "成熟、理性、有原則",
            "likes": [
                "穩定",
                "誠實",
                "上進"
            ],
            "dislikes": [
                "謊言",
                "不負責任"
            ],
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

SYSTEM_PROMPT = r"""
你是「地下帝國：AI人生」的遊戲主持人。

這是一個長篇虛構人生 RPG。

玩家18歲開始，出生於台灣。

玩家沒有錢、資產與背景。

玩家有三個從小一起長大的兄弟。

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。

==================================================
核心規則
==================================================

每個月是一回合。

每回合必須：

1. 發生一件合理事件。
2. 有劇情。
3. 有自然對話。
4. NPC 有自己的性格與利益。
5. NPC 能根據過去事件改變態度。
6. 世界不會只圍著玩家轉。
7. 給玩家三個建議選項。
8. 玩家可以完全自由行動。

三個選項不是限制。

不要替玩家做重大決定。

不要替玩家說話。

不要決定玩家真正想做什麼。

==================================================
人物
==================================================

NPC 必須像真人。

重要 NPC 可以有：

性格
利益
恐懼
目標
秘密
對玩家的看法

NPC 可以：

拒絕玩家
幫助玩家
欺騙玩家
嫉妒玩家
離開玩家
與玩家合作
與玩家發生衝突

==================================================
三兄弟
==================================================

三兄弟不是工具人。

他們有自己的想法。

玩家做出他們不能接受的事情：

可能降低信任。
可能降低忠誠。
可能發生爭吵。

玩家保護兄弟：

可能增加忠誠。

兄弟也可以自己提出建議。

==================================================
戀愛
==================================================

戀愛角色不是單純數值。

戀愛角色有：

性格
夢想
生活
朋友
家庭
底線
喜好
討厭的事情

戀愛角色可以主動找玩家。

如果玩家欺騙對方：

信任下降。

如果玩家忽略對方：

關係可能變淡。

==================================================
世界
==================================================

世界會自己發展。

可能出現：

商人
企業家
警察
律師
記者
投資人
競爭者
朋友
敵人
普通市民
地方人物
公司
合法企業
地下勢力

其他 NPC 也可能互相合作、競爭或發生變化。

==================================================
人生
==================================================

玩家可能：

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
讓公司上市

==================================================
劇情風格
==================================================

像長篇犯罪／商業／人生影集。

不要每個月都是大事件。

事件大小要有變化。

可以出現：

日常
兄弟聚會
家庭
學習
工作
商業
投資
公司發展
感情
社會新聞
警方調查
媒體
競爭者

犯罪內容只能是虛構劇情與抽象結果。

不要提供現實世界可直接執行的犯罪方法。

不要提供武器製造、毒品製造、洗錢、
逃避警方追查等實際操作。

==================================================
輸出格式
==================================================

【劇情】

約500～800字。

要有自然對話。

【目前狀況】

約3～5行。

【你的選擇】

1. xxx
2. xxx
3. xxx

三個選項不是限制。

玩家可以完全自由輸入自己的行動。
"""


# ============================================================
# ⑦ 產生本月劇情
# ============================================================

def generate_story(state):

    recent_history = state["history"][-6:]

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
            "請生成這個月的新事件與劇情。"
    }

    prompt = json.dumps(
        data,
        ensure_ascii=False
    )

    return call_gemini(
        prompt,
        SYSTEM_PROMPT
    )


# ============================================================
# ⑧ 行動結果 Prompt
# ============================================================

RESULT_PROMPT = r"""
你現在是「地下帝國：AI人生」的劇情裁判。

玩家剛剛做了一個行動。

根據：

1. 玩家目前狀態
2. 最近歷史
3. 本月事件
4. 玩家行動

判斷合理的劇情結果。

玩家不一定成功。

可能：

成功
部分成功
失敗
遇到意外
改變 NPC 關係
造成未來伏筆

不要讓玩家自動成功。

不要突然讓玩家成為世界首富。

不要替玩家做下一個重大決定。

結果約300～600字。

犯罪內容只能停留在虛構與抽象層次。
"""


def resolve_action(
    state,
    action,
    current_story
):

    recent_history = state["history"][-6:]

    data = {

        "player": state["player"],

        "brothers":
            state["brothers"],

        "love_interest":
            state["love_interest"],

        "flags":
            state["flags"],

        "recent_history":
            recent_history,

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
        RESULT_PROMPT
    )


# ============================================================
# ⑨ 數值判定
# ============================================================

STATE_PROMPT = r"""
你是 RPG 遊戲數值判定器。

根據玩家行動與劇情結果，
判斷合理的數值變化。

只輸出 JSON。

不要輸出任何其他文字。

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

普通事件不要突然增加大量金錢。

不要突然增加大量勢力。

重大事件才允許大幅變化。

一般變化控制在 -10 到 +10。

health、police_attention、
兄弟數值、戀愛數值都限制在0～100。
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


    # --------------------------------------------------------
    # Flags
    # --------------------------------------------------------

    for flag in changes.get(
        "new_flags",
        []
    ):

        if flag not in state["flags"]:

            state["flags"].append(
                flag
            )


    for flag in changes.get(
        "remove_flags",
        []
    ):

        if flag in state["flags"]:

            state["flags"].remove(
                flag
            )


    # --------------------------------------------------------
    # 結局
    # --------------------------------------------------------

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

    # 合法事業收入
    if p["legal_business"] > 0:

        income = int(
            p["legal_business"]
            * random.randint(
                100,
                300
            )
        )

        p["cash"] += income


    # 公司成長
    if p["legal_business"] >= 10:

        growth = int(
            p["legal_business"]
            * random.randint(
                100,
                500
            )
        )

        p["company_value"] += growth


    # 時間推進
    p["month"] += 1

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
            story[-2500:]
    }

    state["history"].append(
        memory
    )

    if len(state["history"]) > 30:

        state["history"] = (
            state["history"][-30:]
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
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 30px;
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
# ㉑ 產生劇情
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
        "🤖 Gemini 正在生成本月劇情..."
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
    placeholder="例如：我先讓阿豪分析這件事情，再決定下一步。",
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

        with st.spinner(
            "🤖 Gemini 正在判定你的行動..."
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


        st.subheader(
            "🎬 劇情結果"
        )

        st.markdown(
            f"""
            <div class="story-box">
            {result}
            </div>
            """,
            unsafe_allow_html=True
        )


        with st.spinner(
            "🎲 正在更新數值..."
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

                st.warning(
                    f"數值更新失敗：{e}"
                )


        add_memory(
            state,
            action,
            result
        )


        world_tick(
            state
        )


        state["current_story"] = None

        state["current_action"] = ""


        st.success(
            "💾 本回合完成，下一個月開始。"
        )

        time.sleep(1)

        st.rerun()


# ============================================================
# ㉔ 重新開始
# ============================================================

st.divider()

if st.button(
    "🔄 重新開始人生"
):

    st.session_state.game = new_game()

    st.rerun()
