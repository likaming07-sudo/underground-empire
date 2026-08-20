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

# ============================================================
# 固定使用你指定的模型
# ============================================================

MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = r"""
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
地下生意
利益衝突
保護費
地下交易
賭場
娛樂場所勢力
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

兄弟要有自己的台詞與反應。

不要每次都讓三兄弟全部同意玩家。

============================================================
【世界運作】
============================================================

每個月是一個回合。

但是玩家不是世界中心。

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
【最重要：玩家行動的劇情寫法】
============================================================

這是整個遊戲最重要的規則。

玩家輸入行動後，
不能只寫結果。

絕對禁止：

「你決定走黑道，下一個月你成功加入幫派。」

這種跳躍式寫法禁止。

必須真正演出玩家的行動。

例如玩家選：

「我要去找豹哥談談。」

應該描寫：

你為什麼去。
誰陪你。
你怎麼到那裡。
門口看到什麼。
遇到什麼人。
對方怎麼看你。
豹哥是否願意見你。
你與豹哥怎麼談。
阿龍說什麼。
阿虎說什麼。
阿豪怎麼觀察。
豹哥提出什麼問題。
你如何回答。
對方如何反應。
氣氛如何改變。
中間發生什麼事情。
最後事情怎麼收尾。

最後才寫：

【劇情結果】

這個結果必須是「這次行動真正造成的結果」。

不要直接替玩家做下一步重大決定。

例如：

玩家說：
「我要試著加入豹哥。」

可以寫談判過程。

但是不能擅自寫：

「豹哥讓你成為他的副手。」

除非這個結果合理，而且玩家的行動真的足以造成這種結果。

============================================================
【劇情長度】
============================================================

action_result：

一般至少 900～1600 字。

重大事件：

1500～2500 字。

不要為了湊字數一直重複旁白。

要增加：

場景
人物
對話
動作
反應
心理
氣氛
衝突
選擇
結果
後續伏筆

劇情要有小說感。

例如：

不要：

「你到了棋牌社，豹哥同意了你的要求。」

要：

「你推開棋牌社的門時，裡面的麻將聲突然停了一瞬。阿虎下意識往裡看了一眼，阿豪卻伸手壓住他的肩膀。」

然後繼續演出。

============================================================
【玩家不能被AI控制】
============================================================

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
交往
離開某個勢力

除非玩家自己做出這個決定。

============================================================
【三個選項】
============================================================

每次行動結果結束後，
AI都必須準備下一個月的3個建議行動。

格式：

choices：

[
  "選項一",
  "選項二",
  "選項三"
]

三個選項必須有差異。

例如：

1. 去找豹哥談判
2. 先和阿豪調查青幫的動向
3. 暫時不碰這件事情，繼續自己的生活

玩家可以點選其中一個。

玩家也可以自己輸入文字。

三個選項只是建議，
不能限制玩家。

============================================================
【非常重要：回合流程】
============================================================

遊戲真正的流程：

第一階段：

顯示本月開場劇情。

玩家選擇一個行動。

第二階段：

AI只處理「玩家現在這個行動」。

生成：

action_result

同時偷偷準備：

next_month_story

以及：

next_month_choices

但是：

next_month_story 不可以顯示給玩家。

next_month_choices 也不能在 action_result 畫面顯示。

此時玩家只能看到：

【劇情結果】

也就是他剛剛做的事情。

第三階段：

玩家按：

「繼續・進入下一個月」

這時才：

月份 +1

顯示之前已經生成的：

next_month_story

並且顯示：

next_month_choices

不要再次呼叫 AI。

第四階段：

玩家看到下一個月的開場劇情後，
選擇下一個行動。

如此循環。

============================================================
【下一個月劇情】
============================================================

next_month_story 是「下一個月開始時」的開場。

不能直接替玩家完成下一個月的行動。

例如：

本月：

玩家去找豹哥。

next_month_story 可以：

「一個月後，你發現這條街最近多了幾張陌生面孔。阿豪坐在你旁邊，看著窗外的人影，低聲說：『他們應該不是來玩的。』」

這是正確的。

不能：

「一個月後，你已經正式加入豹哥的勢力，開始替他管理地盤。」

這是替玩家做決定，禁止。

============================================================
【劇情連貫】
============================================================

AI必須閱讀：

current_story
recent_history
flags
brothers
love_interest

並且記住：

曾經出現的人物
曾經出現的幫派
曾經發生的事情
玩家做過的選擇
兄弟對玩家的態度
NPC對玩家的態度
玩家與不同勢力的關係

不要每個月重新創造完全不同的世界。

如果之前出現：

豹哥
青幫
三義堂

後續劇情可以繼續使用。

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

第一次接觸地方人物：

power +0
或 +1

不可以：

power +30

兄弟：

普通事情：

-1 到 +2

重要事情：

-3 到 +5

戀愛：

普通互動：

-1 到 +2

重要事件：

-3 到 +5

============================================================
【死亡與逮捕】
============================================================

不要隨便讓玩家死亡。

不要隨便讓玩家被逮捕。

只有玩家的行動與累積局勢合理到達這種程度時，
才可以發生。

============================================================
【輸出】
============================================================

只輸出合法 JSON。

不要 Markdown。

不要 ```json。

格式：

{
  "story": "本月開場劇情",

  "action_result": "完整描寫玩家這次行動的過程、人物互動、對話、結果與後續影響",

  "next_month_story": "下一個月開始時的開場劇情",

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
"""


# ============================================================
# ④ 新遊戲
# ============================================================

def new_game():

    return {
        "save_version": 3,

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

        # 當前畫面正在顯示的劇情
        "current_story": None,

        # 玩家行動產生的結果
        "pending_result": None,

        # AI 提前準備好的下一月劇情
        "pending_next_story": None,

        # AI 提前準備好的下一月選項
        "pending_next_choices": [],

        # playing / action_result
        "phase": "playing",

        "game_started": False
    }


# ============================================================
# ⑤ Gemini API
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
                raise RuntimeError("AI 沒有返回內容。")

            text = response.text.strip()

            # 防止模型偶爾還是包 Markdown
            if text.startswith("```json"):
                text = text[7:]

            elif text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            return result

        except json.JSONDecodeError as e:

            if attempt < retries - 1:
                time.sleep(2)
                continue

            raise RuntimeError(
                f"AI 回傳的內容不是有效 JSON：{e}"
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
                    "請稍後再試。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    "Gemini 模型 gemini-3.1-flash-lite 無法使用。\n\n"
                    "請確認 Gemini API Key 目前有權限使用此模型。"
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

        "recent_history": state["history"][-12:],

        "current_story": state["current_story"],

        "player_action": action
    }

    if action:

        task = """
玩家剛剛在本月劇情中做出了以下行動：

【玩家行動】

{action}

============================================================
現在請完整演出這個行動。
============================================================

這次輸出的 action_result 是整個回合最重要的內容。

不能直接跳結果。

必須把玩家「做這件事情的過程」演出來。

至少包含：

1. 玩家準備做什麼
2. 玩家與誰討論
3. 誰陪玩家
4. 玩家去了哪裡
5. 場景與環境
6. 見到誰
7. NPC 怎麼看玩家
8. 兄弟怎麼反應
9. 雙方實際對話
10. 玩家怎麼表態
11. 對方提出什麼
12. 玩家怎麼回應
13. 中間發生什麼變化
14. 其他 NPC 的反應
15. 氣氛如何改變
16. 最後結果
17. 對未來產生什麼影響

例如玩家選：

「去找豹哥談談。」

禁止寫：

「你找到豹哥，豹哥同意讓你加入。」

必須像小說一樣完整演出：

你先跟兄弟討論。

阿虎可能想直接進去。

阿豪可能提醒你注意。

阿龍可能提出不同看法。

接著你們前往棋牌社。

描述環境。

描述門口的人。

描述你們如何進去。

描述豹哥如何看待你。

描述雙方談話。

描述豹哥問你的問題。

描述你的回答。

描述阿豪觀察到的細節。

描述阿虎可能說出的話。

描述豹哥的態度。

最後才得到結果。

============================================================
【非常重要：不要替玩家做重大決定】
============================================================

玩家做出的事情只能依照玩家的指令。

例如玩家說：

「我想去找豹哥談談。」

你可以演出：

去找豹哥
談判
詢問
觀察
試探

但不要擅自讓玩家：

答應加入
背叛兄弟
殺人
簽約
花掉所有錢
成為幫派頭目
與 NPC 交往

除非玩家自己的指令已經明確做出這個決定。

============================================================
【劇情風格】
============================================================

劇情不要像遊戲系統報告。

不要一直說：

「你的聲望+1。」

這些數值由 changes 處理。

小說正文應該主要描寫：

人物
場景
對話
行動
反應
心理
氣氛
局勢

要有真正的故事感。

action_result 一般至少 900～1600 字。

重大事件可以 1500～2500 字。

不要用大量空泛旁白湊字數。

============================================================
【玩家目前的階段】
============================================================

玩家目前仍然是：

{age}歲
第{month}個月

玩家不是大哥。

如果玩家目前地下勢力很低，
不要讓所有地下大人物突然認識玩家。

人物必須逐步認識。

如果玩家第一次遇到某個豹哥，
不要直接讓豹哥把玩家當自己人。

============================================================
【世界記憶】
============================================================

請仔細閱讀：

current_story
recent_history
flags
brothers
love_interest

之前出現的人物必須有記憶。

之前出現的幫派可以延續。

之前的行動會影響現在的人際關係。

============================================================
【下一個月】
============================================================

除了 action_result 之外，
還必須生成：

next_month_story

這只是下一個月的「開場」。

不能替玩家完成下一個月的行動。

例如本月：

玩家去找豹哥。

正確：

「一個月後，阿豪告訴你，最近這條街多了幾個陌生面孔。你站在巷口，看著遠處棋牌社亮著的燈，開始意識到那次談話可能已經產生影響。」

錯誤：

「一個月後，你正式加入豹哥勢力，開始管理這條街。」

因為後者替玩家做了下一個月的決定。

============================================================
【下一個月選項】
============================================================

choices 必須是下一個月開始後，
玩家可以採取的三個不同方向。

例如：

[
  "去找豹哥問清楚最近的情況",
  "跟阿豪先觀察街上的陌生人",
  "暫時不碰地下勢力，先處理自己的生活"
]

三個選項必須有明顯差異。

玩家也可以自由輸入。

============================================================
【數值】
============================================================

數值只能合理變化。

不要暴增。

普通事件：

0～2

重要事件：

3～5

地下勢力不能因為一次行動直接暴增。

兄弟關係也必須慢慢變。

============================================================
最後
============================================================

只輸出合法 JSON。

不要 Markdown。

不要 ```。

不要解釋 JSON。

"""

        data["task"] = task.format(
            action=action,
            age=p["age"],
            month=p["month"]
        )

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
警方注意度0
健康100

玩家身邊只有：

阿龍
阿虎
阿豪

這是黑道人生模擬。

但是不要第一個月直接讓玩家加入大型幫派。

從：

生活
工作
兄弟
地方
小人物
小型機會
偶然事件

開始。

可以埋下地下世界的伏筆。

例如：

某間棋牌社
地方上的小混混
某個陌生人物
附近的地盤問題
兄弟聽到的傳聞

但不要直接把玩家變成黑道大哥。

story 應該是一個有場景、有角色、有對話的開場。

最後給3個玩家可以採取的方向。

只輸出合法 JSON。
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
# ⑧ 套用 AI 變化
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
    # 兄弟關係
    # ========================================================

    brothers = result.get(
        "brothers",
        {}
    )

    for name, data in brothers.items():

        if name not in state["brothers"]:
            continue

        brother = state["brothers"][name]

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

            brother[field] += value

            brother[field] = max(
                0,
                min(100, brother[field])
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
            love["relationship"] = "熟悉"

        elif affection < 90:
            love["relationship"] = "曖昧"

        else:
            love["relationship"] = "交往"

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
    # 結局狀態
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

    # 下一個月
    p["month"] += 1

    if p["month"] > 12:

        p["month"] = 1

        p["age"] += 1

        for brother in state["brothers"].values():

            brother["age"] += 1


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
            )[-5000:]
    }

    state["history"].append(
        memory
    )

    if len(state["history"]) > 50:

        state["history"] = (
            state["history"][-50:]
        )


# ============================================================
# ⑪ 存檔
# ============================================================

def create_save_data(state):

    return {

        "game_name":
            "地下帝國：AI人生",

        "save_version":
            3,

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
# ⑬ Session State
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


if "action_text" not in st.session_state:

    st.session_state.action_text = ""


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

    save_data = save_game_file(
        state
    )

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

                    st.session_state.game = (
                        loaded_game
                    )

                    st.session_state.action_text = ""

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

        st.session_state.action_text = ""

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

        st.session_state.action_text = ""

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

        st.session_state.action_text = ""

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

            state["pending_next_choices"] = (
                result.get(
                    "choices",
                    []
                )[:3]
            )

            state["phase"] = "playing"

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉒ PLAYING：本月開場
# ============================================================

if state["phase"] == "playing":

    st.subheader(
        "📖 本月劇情"
    )

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

        st.write(
            "### 🎮 建議行動"
        )

        choice_cols = st.columns(3)

        for i, choice in enumerate(
            choices[:3]
        ):

            with choice_cols[i]:

                if st.button(
                    f"{i + 1}. {choice}",
                    key=(
                        f"choice_"
                        f"{i}_"
                        f"{p['age']}_"
                        f"{p['month']}"
                    ),
                    use_container_width=True
                ):

                    st.session_state.action_text = (
                        choice
                    )

                    st.rerun()

    # ========================================================
    # 玩家自由輸入
    # ========================================================

    st.write(
        "### ✍️ 自由行動"
    )

    with st.form(
        "action_form",
        clear_on_submit=False
    ):

        action = st.text_area(
            "你想做什麼？",
            key="action_text",
            placeholder=(
                "可以自由輸入，例如：\n"
                "我決定先跟阿豪去附近看看，"
                "找機會接觸地方上的地下勢力。"
            ),
            height=150
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
                    action.strip()
                )

                result = call_ai(
                    prompt
                )

            except Exception as e:

                st.error(
                    str(e)
                )

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
            action.strip(),
            result
        )

        # ====================================================
        # 儲存下一個月
        # ====================================================

        state["pending_next_story"] = (
            result.get(
                "next_month_story",
                "新的一個月開始了。"
            )
        )

        # 這裡非常重要：
        # 不要清掉！
        # 這就是按「繼續」後下一個月的3選項
        state["pending_next_choices"] = (
            result.get(
                "choices",
                []
            )[:3]
        )

        # ====================================================
        # 儲存這次行動結果
        # ====================================================

        state["pending_result"] = (
            result.get(
                "action_result",
                "這個行動產生了一些變化。"
            )
        )

        # ====================================================
        # 重要：
        # 直接覆蓋目前畫面
        #
        # 不會：
        #
        # 本月劇情
        # ↓
        # 行動結果
        #
        # 一直往下堆
        #
        # 而是：
        #
        # 本月劇情
        # ↓
        # 執行
        # ↓
        # 畫面直接變成行動結果
        # ====================================================

        state["current_story"] = (
            state["pending_result"]
        )

        # 進入等待繼續
        state["phase"] = "action_result"

        # 清除文字框
        st.session_state.action_text = ""

        st.rerun()


# ============================================================
# ㉓ ACTION RESULT：只顯示這次行動
# ============================================================

if state["phase"] == "action_result":

    st.subheader(
        "🎬 劇情結果"
    )

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
        # 現在才推進世界時間
        # ====================================================

        world_tick(
            state
        )

        # ====================================================
        # 把之前 AI 已經生成好的下一月劇情蓋上來
        # ====================================================

        next_story = (
            state.get(
                "pending_next_story",
                None
            )
            or
            "新的一個月開始了。"
        )

        state["current_story"] = (
            next_story
        )

        # ====================================================
        # pending_next_choices
        #
        # 這裡不要清掉。
        #
        # 它就是上一回合 AI 已經準備好的
        # 「下一個月三個選項」
        # ====================================================

        state["pending_result"] = None

        state["pending_next_story"] = None

        state["phase"] = "playing"

        st.session_state.action_text = ""

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

    st.session_state.action_text = ""

    st.rerun()
