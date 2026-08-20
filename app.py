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

# 目前 Gemini API 官方低成本 3.1 Flash 型號
MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM
# ============================================================

SYSTEM_PROMPT = """
你是「地下帝國：AI人生」的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的黑道人生模擬 RPG。

玩家18歲開始，出生於台灣普通家庭。

玩家：
- 沒有錢
- 沒有資產
- 沒有背景
- 沒有人脈
- 沒有公司
- 沒有地下勢力

玩家必須從一個普通人開始，一步一步建立自己的人生與地下世界。

三個從小一起長大的兄弟：

阿龍：
沉穩、重義氣、保護兄弟。

阿虎：
衝動、好勝、敢冒險。

阿豪：
冷靜、聰明、擅長分析。

==================================================
【最重要：這不是正經商業人生模擬】
==================================================

遊戲核心是：

「普通人 → 接觸地下世界 → 建立關係 → 建立勢力 → 面對競爭 → 建立自己的地下帝國」

合法工作、學業、商業只是玩家可以選擇的人生路線之一。

玩家也可以選擇逐漸進入地下世界。

地下勢力、兄弟關係、敵人、競爭者、地盤、聲望、警方注意度、
地下人物關係，都可以成為長期遊戲內容。

但是：

不要提供現實世界可以直接執行的犯罪操作教學。

犯罪劇情可以描述：
- 發生了什麼
- 玩家遇到誰
- 人物怎麼談
- 人物怎麼反應
- 玩家做出的選擇
- 成功或失敗
- 關係變化
- 勢力變化
- 風險
- 法律後果

不要描述：
- 具體犯罪操作流程
- 如何躲避警方
- 如何製造或取得武器
- 如何販賣或取得毒品
- 如何實際執行暴力犯罪
- 如何竊盜、詐騙或洗錢的具體方法

==================================================
【世界規則】
==================================================

每個月是一回合。

世界必須有自己的運作。

世界不能永遠圍著玩家轉。

不要每個月都發生重大事件。

事件大小必須有變化。

普通月份可以是：
- 工作
- 學習
- 家庭
- 兄弟
- 朋友
- 小型地下人物接觸
- 普通人際關係
- 小型衝突
- 小型機會
- 日常生活

中型事件可以是：
- 地下人物介紹
- 小型勢力衝突
- 商業機會
- 人際衝突
- 競爭者
- 兄弟之間的意見不合
- 新人物加入
- 小型利益交換
- 玩家第一次接觸地下圈子

大型事件可以是：
- 建立勢力
- 地下勢力競爭
- 重大人物出現
- 公司成立
- 重大商業合作
- 重大危機
- 警方調查
- 媒體事件
- 重要人物死亡或離場
- 勢力重新洗牌

重大事件不能每個月連續發生。

==================================================
【劇情生成方式】
==================================================

這一點非常重要。

玩家做出行動後，不可以直接跳到結果。

例如玩家說：

「我決定開始接觸地下世界。」

錯誤：

「隔月你已經成為地下勢力的一員。」

正確：

必須描寫完整過程，例如：

1. 玩家先跟誰討論
2. 哪個兄弟知道這件事情
3. 玩家透過什麼合理的人際關係接觸到人物
4. 玩家去什麼類型的地方
5. 遇到誰
6. 對方如何看待玩家
7. 對方提出什麼條件或試探
8. 玩家如何回應
9. 兄弟如何反應
10. 最後發生什麼
11. 玩家獲得什麼
12. 玩家失去什麼
13. 關係如何變化
14. 地下勢力是否增加
15. 下一個月留下什麼伏筆

劇情要有「過程」。

不能只寫「你做了某件事，所以成功」。

==================================================
【每回合劇情長度】
==================================================

action_result 必須是完整劇情。

一般回合：

至少 500～900 個中文字。

重要事件：

可以 900～1500 個中文字。

不要為了湊字數重複。

劇情應該有：

場景
→ 人物
→ 對話
→ 行動
→ 反應
→ 發展
→ 結果

不要每次都使用完全相同的句型。

==================================================
【下一個月】
==================================================

這是另一個非常重要的規則。

next_month_story 只是：

「下一個月的開場場景」

不是下一個月的完整結果。

例如：

本月玩家選擇：
「跟阿虎一起去接觸地下人物。」

本月 action_result：

完整描寫玩家如何跟阿虎討論、
如何找到合理的人脈、
如何見面、
對方如何試探、
玩家如何回答、
最後建立什麼程度的關係。

然後 next_month_story：

「一個月後，阿虎突然告訴你，那個人又來找他了。
這次他沒有直接談事情，而是問你最近是不是有興趣接觸另一批人。
你們三兄弟坐在桌邊討論這件事……」

到這裡就停止。

不能直接寫：

「於是你加入了那個勢力。」

因為玩家下一回合還沒有做決定。

==================================================
【三個選項】
==================================================

每個回合都必須生成三個建議選項。

三個選項不能只是同義句。

應該有不同方向。

例如：

1.
「先跟阿豪討論這件事，調查對方背景。」

2.
「直接跟阿虎去見那個人。」

3.
「暫時不碰，先找一份工作累積現金。」

三個選項要有不同風險。

但：

玩家永遠可以不選三個選項。

玩家可以自由輸入任何合理行動。

==================================================
【玩家自由】
==================================================

不要替玩家說話。

不要替玩家做重大決定。

不要擅自讓玩家答應事情。

玩家輸入：

「我先觀察對方，不急著答應。」

AI 就必須按照這個行動發展。

玩家輸入：

「我跟阿龍討論這件事情。」

就按照阿龍的性格發展。

玩家輸入：

「我拒絕這個邀請。」

就必須允許拒絕。

不要強迫玩家走劇情。

==================================================
【玩家成長】
==================================================

開局：

現金0
資產0
公司估值0
合法事業0
地下勢力0
聲望0
警方注意度0
健康100

玩家不能突然暴富。

玩家不能因為一次普通行動突然成為大人物。

玩家不能突然認識總裁、部長、政治人物或地下世界最高層人物。

人物必須有合理接觸原因。

玩家剛開始：

主要接觸：
- 同學
- 同事
- 鄰居
- 小商家
- 普通朋友
- 小型地下人物

玩家建立地下關係後：

才逐漸接觸：
- 地方人物
- 地下勢力成員
- 競爭者
- 更高層人物

玩家建立勢力：

才可以逐漸接觸更高層的人。

==================================================
【地下勢力】
==================================================

power 代表玩家的地下勢力。

power 很低：

玩家只是普通人。

power 1～10：

開始認識地下圈子。

power 11～30：

開始有自己的小圈子。

power 31～60：

開始形成真正勢力。

power 61～100：

已經是重要地下人物。

不要一次增加太多。

一般事件：

power +0～2。

重大事件：

power +2～5。

非常重大且合理的事件：

才可以增加更多。

==================================================
【聲望】
==================================================

reputation 不是單純好感。

代表玩家在世界中的名聲。

玩家可以因為：
- 守信用
- 成功處理事情
- 幫助兄弟
- 建立事業
- 建立勢力
- 得罪人物
- 失敗
- 被警方注意

而改變。

==================================================
【警方注意度】
==================================================

police_attention：

0～10：
幾乎沒人注意。

11～30：
開始出現風險。

31～60：
警方可能開始注意玩家相關人物或事件。

61～80：
警方高度關注。

81～100：
重大危機。

不要因為玩家普通聊天就大幅增加。

==================================================
【三兄弟】
==================================================

三兄弟不是工具人。

每個人有自己的性格。

阿龍：
重視兄弟、安全、穩定。

阿虎：
喜歡冒險、衝突、刺激。

阿豪：
重視分析、利益、長期風險。

玩家不同選擇會讓兄弟產生不同看法。

忠誠 loyalty
信任 trust
尊重 respect

一次普通事件通常只變化 0～3。

重大事件才可能變化 3～5。

兄弟可以：

支持
反對
爭吵
失望
生氣
離開
改變立場

不要永遠支持玩家。

==================================================
【一般 NPC】
==================================================

NPC 必須有：

名字
性格
利益
目標
恐懼
底線
生活
與玩家的關係

NPC不是工具人。

NPC可以：

幫助
拒絕
欺騙
嫉妒
競爭
離開
改變態度

==================================================
【戀愛】
==================================================

玩家開局沒有女朋友。

不要第一個月直接生成女友。

戀愛必須自然發生。

可能經過：

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

戀愛 NPC 必須有自己的：

性格
家庭
工作或學業
夢想
價值觀
喜好
底線
生活

她不是玩家工具人。

她可以：

拒絕
生氣
失望
離開
主動做自己的事情

戀愛關係：

affection
trust
respect

一次普通互動只能小幅增加。

==================================================
【時間】
==================================================

每次玩家完成一個月行動後：

才進入下一個月。

AI 已經生成的 next_month_story 可以直接使用。

不要再額外呼叫一次 API。

==================================================
【AI任務】
==================================================

每次玩家完成一個行動：

1. 判斷玩家行動是否合理
2. 描寫行動過程
3. 描寫玩家接觸到的人
4. 描寫 NPC 對話與反應
5. 判斷成功、部分成功或失敗
6. 更新數值
7. 更新兄弟關係
8. 更新戀愛關係
9. 產生完整 action_result
10. 產生下一個月「開場」
11. 產生三個下一步選項
12. 保持世界連續性

不要永遠讓玩家成功。

==================================================
【輸出】
==================================================

只能輸出合法 JSON。

格式：

{
  "story": "本月開場劇情",

  "action_result": "玩家本月行動的完整過程與結果",

  "next_month_story": "下一個月的開場劇情，只能是開場與伏筆，不得提前替玩家做下一個月的決定",

  "options": [
    "選項一",
    "選項二",
    "選項三"
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
        "current_result": None,
        "current_options": [],

        "game_started": False
    }


# ============================================================
# ⑤ Gemini Schema
# ============================================================

RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {

        "story": {
            "type": "STRING"
        },

        "action_result": {
            "type": "STRING"
        },

        "next_month_story": {
            "type": "STRING"
        },

        "options": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        },

        "changes": {
            "type": "OBJECT",
            "properties": {

                "cash_change": {
                    "type": "NUMBER"
                },

                "assets_change": {
                    "type": "NUMBER"
                },

                "company_value_change": {
                    "type": "NUMBER"
                },

                "legal_business_change": {
                    "type": "NUMBER"
                },

                "power_change": {
                    "type": "NUMBER"
                },

                "reputation_change": {
                    "type": "NUMBER"
                },

                "police_attention_change": {
                    "type": "NUMBER"
                },

                "health_change": {
                    "type": "NUMBER"
                }
            },
            "required": [
                "cash_change",
                "assets_change",
                "company_value_change",
                "legal_business_change",
                "power_change",
                "reputation_change",
                "police_attention_change",
                "health_change"
            ]
        },

        "brothers": {
            "type": "OBJECT",
            "properties": {

                "阿龍": {
                    "type": "OBJECT",
                    "properties": {
                        "loyalty_change": {
                            "type": "NUMBER"
                        },
                        "trust_change": {
                            "type": "NUMBER"
                        },
                        "respect_change": {
                            "type": "NUMBER"
                        }
                    }
                },

                "阿虎": {
                    "type": "OBJECT",
                    "properties": {
                        "loyalty_change": {
                            "type": "NUMBER"
                        },
                        "trust_change": {
                            "type": "NUMBER"
                        },
                        "respect_change": {
                            "type": "NUMBER"
                        }
                    }
                },

                "阿豪": {
                    "type": "OBJECT",
                    "properties": {
                        "loyalty_change": {
                            "type": "NUMBER"
                        },
                        "trust_change": {
                            "type": "NUMBER"
                        },
                        "respect_change": {
                            "type": "NUMBER"
                        }
                    }
                }
            }
        },

        "love": {
            "type": "OBJECT",
            "properties": {

                "created": {
                    "type": "BOOLEAN"
                },

                "name": {
                    "type": "STRING"
                },

                "personality": {
                    "type": "STRING"
                },

                "affection_change": {
                    "type": "NUMBER"
                },

                "trust_change": {
                    "type": "NUMBER"
                },

                "respect_change": {
                    "type": "NUMBER"
                }
            }
        },

        "flags_add": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        },

        "flags_remove": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        },

        "death": {
            "type": "BOOLEAN"
        },

        "arrested": {
            "type": "BOOLEAN"
        },

        "listed": {
            "type": "BOOLEAN"
        }
    },

    "required": [
        "story",
        "action_result",
        "next_month_story",
        "options",
        "changes",
        "brothers",
        "love",
        "flags_add",
        "flags_remove",
        "death",
        "arrested",
        "listed"
    ]
}


# ============================================================
# ⑥ AI 呼叫
# ============================================================

def call_ai(prompt, retries=2):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(

                model=MODEL,

                contents=prompt,

                config={

                    "system_instruction":
                        SYSTEM_PROMPT,

                    "response_mime_type":
                        "application/json",

                    "response_schema":
                        RESPONSE_SCHEMA
                }
            )

            if not response.text:

                raise RuntimeError(
                    "AI 沒有返回內容"
                )

            text = response.text.strip()

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

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
                    "請等待 API 額度恢復。"
                )

            if "404" in error_text:

                raise RuntimeError(
                    "Gemini 模型無法使用。\n\n"
                    "目前設定的模型："
                    f"{MODEL}\n\n"
                    "請確認你的 Gemini API 專案可以使用 "
                    "gemini-3.1-flash-lite。"
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
# ⑦ 建立 AI 回合資料
# ============================================================

def build_turn_prompt(
    state,
    action=None
):

    p = state["player"]

    data = {

        "current_date": {

            "age":
                p["age"],

            "month":
                p["month"]
        },

        "player":
            p,

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

        "current_options":
            state.get(
                "current_options",
                []
            ),

        "player_action":
            action
    }

    if action:

        data["task"] = """

玩家已經完成本月行動。

請注意：

這不是單純判定成功或失敗。

你必須先描寫「過程」。

請按照以下節奏：

第一段：
玩家開始執行行動。

第二段：
玩家接觸到誰、在哪裡、為什麼會接觸到這個人。

第三段：
NPC如何說話與反應。

第四段：
玩家如何做出自己的行動。

第五段：
事情如何發展。

第六段：
兄弟或其他 NPC 如何反應。

第七段：
最後才判定本月結果。

第八段：
說明數值與關係為什麼發生變化。

action_result 必須讓玩家有「真的玩了一個月」的感覺。

不能只有：

「你做了X，所以成功。」

必須讓玩家看到：

「我做了什麼 → 遇到誰 → 發生什麼 → 我怎麼處理 → 對方怎麼反應 → 最後結果。」

重要：

next_month_story 只能是「下一個月的開場」。

不能提前替玩家完成下一個月的行動。

不要寫：

「下一個月你成功加入某勢力。」

應該寫：

「下一個月，某個人物出現在你的生活中，提出一個新的可能。」

然後停止。

options 必須提供三個不同方向的下一步選擇。

三個選項要有不同風險。

例如：

1. 保守
2. 中等
3. 冒險

但不要固定使用這三種名稱。

"""

    else:

        data["task"] = """

這是新遊戲。

請生成18歲第1個月的開場劇情。

玩家目前：

沒有女友
沒有錢
沒有資產
沒有公司
沒有合法事業
沒有地下勢力
沒有聲望
沒有背景

這是一個黑道人生模擬。

不要一開局直接讓玩家成為黑道老大。

但是可以埋下地下世界的伏筆。

例如：

兄弟知道某個人物
玩家在生活中偶然接觸到某個人
某個小人物提供機會
玩家聽到附近發生的事情
阿虎提出一個冒險想法

玩家還沒有真正做選擇。

story 要像遊戲開場。

最後提供三個不同方向的選項。

戀愛角色不要直接送到玩家面前。

"""

    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑧ 安全數值
# ============================================================

def safe_number(value):

    if isinstance(
        value,
        (int, float)
    ):

        return value

    return 0


# ============================================================
# ⑨ 套用數值
# ============================================================

def apply_changes(
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
                data.get(
                    key,
                    0
                )
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
        love_data.get(
            "created",
            False
        )
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
            )[-3000:]
    }

    state["history"].append(
        memory
    )

    if len(
        state["history"]
    ) > 40:

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

        這不是一個固定劇本。

        你可以選擇普通人生，
        也可以逐漸踏入地下世界。

        每一個選擇都會影響之後的人生。
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

            prompt = build_turn_prompt(
                state
            )

            result = call_ai(
                prompt
            )

            state["current_story"] = result.get(
                "story",
                "你的故事即將開始。"
            )

            state["current_options"] = (
                result.get(
                    "options",
                    []
                )[:3]
            )

            state["current_result"] = None

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉓ 劇情
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
# ㉔ 三個選項
# ============================================================

st.subheader(
    "🎮 你要怎麼做？"
)

options = state.get(
    "current_options",
    []
)

selected_option = None

if options:

    for i, option in enumerate(options):

        if st.button(
            f"{i + 1}. {option}",
            key=f"option_{i}",
            use_container_width=True
        ):

            selected_option = option


# ============================================================
# ㉕ 自由行動
# ============================================================

with st.form(
    "action_form",
    clear_on_submit=True
):

    action = st.text_area(

        "或者自己輸入行動",

        placeholder=(
            "你可以完全自由行動，例如：\n"
            "我先跟阿豪討論這個人到底值不值得接觸，"
            "不要急著答應。"
        ),

        height=120
    )

    submitted = st.form_submit_button(

        "⚡ 執行自由行動",

        type="primary",

        use_container_width=True
    )


# ============================================================
# ㉖ 判斷玩家選擇
# ============================================================

final_action = None

if selected_option:

    final_action = selected_option

elif submitted:

    if not action.strip():

        st.warning(
            "請先輸入你的行動。"
        )

        st.stop()

    final_action = action.strip()


# ============================================================
# ㉗ 執行一回合
# ============================================================

if final_action:

    with st.spinner(
        "🤖 AI 正在判定你的選擇並推進劇情..."
    ):

        try:

            prompt = build_turn_prompt(
                state,
                final_action
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
    # 顯示本月完整結果
    # ========================================================

    result_text = result.get(
        "action_result",
        "這個行動產生了一些變化。"
    )

    st.subheader(
        "🎬 本月行動結果"
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
    # 人生記憶
    # ========================================================

    add_memory(
        state,
        final_action,
        result
    )


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
    # 下一個月三選項
    # ========================================================

    next_options = result.get(
        "options",
        []
    )

    if isinstance(next_options, list):

        state["current_options"] = [
            str(x)
            for x in next_options[:3]
            if str(x).strip()
        ]

    else:

        state["current_options"] = []


    state["current_result"] = None


    # ========================================================
    # 重新整理
    # ========================================================

    st.rerun()


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
