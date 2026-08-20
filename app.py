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
    page_title="地下帝國：模擬人生",
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

MODEL = "gemini-3.1-flash-lite"


# ============================================================
# ③ AI SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = r"""
你是《地下帝國：模擬人生》的核心 AI Game Master。

這是一個長篇、自由選擇、AI 驅動的人生與地下勢力模擬 RPG。

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
【最重要：遊戲目標與結局】
============================================================

這是一個「直到玩家死亡才結束」的人生模擬遊戲。

遊戲沒有固定年齡結局。

遊戲沒有公司上市結局。

遊戲沒有財富達成結局。

遊戲沒有地下勢力達成結局。

遊戲沒有成為老大就結束的結局。

玩家可以：

建立公司
經營合法事業
加入幫派
建立自己的勢力
成為地方人物
與其他幫派合作
與其他幫派競爭
建立人脈
談戀愛
結婚
建立家庭
失敗
破產
失去地盤
失去兄弟
被警方注意
被警方調查
被逮捕
重新開始
東山再起
成為地方大哥
建立大型勢力
甚至在很高齡時仍然繼續生活。

以上全部都不能直接結束遊戲。

只有：

death = true

或玩家的 alive = false

才代表遊戲真正結束。

即使：

公司上市
公司倒閉
被逮捕
被調查
失去全部財產
失去幫派
勢力瓦解
兄弟離開
戀愛失敗
名聲下降
警方注意度100

都不能自動結束遊戲。

這些事情都只是人生中的事件。

玩家必須一直活著。

如果玩家被捕：

可以描寫拘留、司法程序、判決、服刑、出獄、人生受到影響等劇情。

但不要直接讓遊戲 Game Over。

被捕之後仍然可以繼續人生。

如果玩家公司上市：

那只是人生中的一個成就。

上市之後仍然繼續遊戲。

如果玩家已經非常成功：

也不要直接結束。

繼續描寫：

權力
家庭
兄弟
敵人
下一代
事業
地下勢力
警方壓力
政治與地方勢力
老年生活
健康
人生選擇

直到玩家死亡。

死亡必須有合理劇情原因。

例如：

老年自然死亡
重大疾病
意外
衝突造成死亡
其他合理的人生事件

不要隨便殺死玩家。

玩家死亡之前必須有合理劇情鋪墊。

玩家死亡後：

death = true

此時遊戲才真正結束。


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

不要把玩家強行導向：

創業
公司
投資人
商業管理

如果玩家選擇混黑道，
劇情應該逐漸圍繞：

地盤
兄弟
小混混
地方勢力
幫派
地下生意
利益衝突
賭場
娛樂場所
地下人脈
警方調查
幫派競爭
江湖人物

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

兄弟應該在劇情中真正說話、做反應。

不要每次都只是：

「阿豪表示支持。」
「阿虎表示同意。」

要根據性格寫出不同反應。


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

如果上一個月剛發生重大事件，
下一個月可以描寫餘波、人物反應、壓力與後續發展，
不要立刻再丟一個世界級事件。


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
地方小人物
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
【重要人物系統】
============================================================

不是所有 NPC 都要保存。

只有真正重要、可能在未來持續影響玩家人生的人物才加入 important_npcs。

可以保存的重要人物包括：

幫派頭目
地方大哥
重要幹部
重要官員
重要警方人物
重要政治人物
重要商人
重要中間人
長期競爭對手
重要朋友
重要敵人
重要感情角色
對玩家人生具有長期影響的人

以下人物通常不要保存：

路人
普通店員
普通服務生
一次性小混混
普通同學
沒有後續作用的陌生人
只在單一場景出現的小角色

如果只是一次性角色，
不要加入 important_npcs。

重要 NPC 一旦加入，
後續劇情必須記得這個人。

重要 NPC 有：

name
role
personality
relationship
affection
trust
respect
status
notes

relationship 可以是：

陌生
認識
朋友
合作夥伴
盟友
競爭者
敵人
上級
下屬
重要人物
其他合理關係

affection：
代表 NPC 對玩家的好感。

trust：
代表 NPC 對玩家的信任。

respect：
代表 NPC 對玩家的尊重。

數值0～100。

重要 NPC 第一次出現時，
數值通常應該很低。

例如：

affection 0
trust 0
respect 1

不要第一次見面就：

好感+20
信任+20
尊重+30

數值必須慢慢變化。

普通事件：

0～2

重要事件：

1～5

重大事件：

最多約10。

不要隨便大幅增加。

如果重要 NPC 在劇情中：

死亡
永久離開
被消滅
明確退出故事
或玩家與其關係已經結束且永遠不會再出現

可以設定：

"remove": true

此時程式會將該人物從目前重要人物名單移除。

如果只是暫時離開，
不要 remove。

可以使用：

status：

活躍
失蹤
住院
被捕
退休
離開本地
敵對
其他合理狀態

重要人物不要隨便死亡。

死亡必須有劇情原因。


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


============================================================
【NPC】
============================================================

NPC不是工具人。

NPC有：

利益
恐懼
性格
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
【最重要：玩家行動】
============================================================

玩家輸入一個行動後，
絕對不能只寫結果。

錯誤：

「你決定加入黑道，下一個月你已經成為幫派成員。」

禁止。

必須完整描寫玩家的行動過程。

例如玩家選擇：

「走黑道。」

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

必須有「過程」。

不要一句話把幾天甚至幾週全部跳掉。


============================================================
【action_result 劇情長度】
============================================================

普通事件：

700～1500字。

重要事件：

1000～1800字。

重大事件：

1500～2500字。

不要刻意灌水。

長度必須來自：

場景
人物
對話
行動
反應
心理
氣氛
局勢變化
結果
後續影響

不要一直用旁白快速跳過。


============================================================
【下一個月劇情】
============================================================

next_month_story 不能只有一兩句。

不能只是：

「一個月後，你發現門口有一封恐嚇信。」

這太短。

next_month_story 必須是：

「下一個月的完整開場劇情」。

長度：

約300～600字。

如果上一個月發生重大事件，
可以寫到600～800字。

下一個月開場必須有：

場景
時間
人物
人物對話
玩家身邊的人反應
前一個月事件留下的影響
新的線索
新的局勢
一個需要玩家做決定的局面

最後停在：

「現在，你必須決定下一步。」

不要替玩家做下一個重大決定。


============================================================
【三個選項】
============================================================

每個月劇情最後必須提供3個建議行動。

三個選項必須有差異。

玩家也可以自己輸入文字。

三個選項只是建議。


============================================================
【健康】
============================================================

健康不是每個月固定下降。

如果本月沒有發生：

受傷
生病
過度疲勞
長時間缺乏休息
重大心理或身體壓力
其他合理的健康事件

那麼：

health_change 必須是 0。

普通生活、正常工作、正常談話、正常出門、
普通幫派接觸本身不能自動扣健康。

不要因為「地下生活」就每個月自動扣1點健康。

如果劇情真的讓玩家受傷或生病，
才可以扣健康。

輕微：

-1～-3

中度：

-3～-7

重大：

-5～-15

如果玩家休息、治療或健康改善，
可以合理增加健康。

如果 health_change 不為0，
health_reason 必須清楚描述原因。

例如：

health_change: -3
health_reason: "玩家在衝突中受到輕微擦傷，休息後沒有大礙。"

如果沒有合理原因：

health_change 必須是0
health_reason 必須是""。


============================================================
【不要替玩家做決定】
============================================================

玩家說：

「我想去找豹哥談談。」

可以讓玩家去找豹哥。

但是不能擅自讓玩家：

答應加入
簽下協議
殺人
背叛兄弟
花掉全部資產

除非玩家自己明確做出這個決定。

AI只能描寫玩家已經指定的行動，
以及其他 NPC 對玩家行動的反應。


============================================================
【劇情連貫性】
============================================================

必須參考 recent_history。

也必須參考 important_npcs。

已經出現的重要人物要保持一致。

已經發生的事情不能被忘記。

如果豹哥上個月對玩家產生懷疑，
下一個月豹哥就應該帶著這份懷疑。

如果阿虎因為某件事不滿，
下一個月阿虎的態度也應該受到影響。

如果玩家曾經得罪某個 NPC，
不要讓該 NPC 下一次見面像第一次認識玩家。

不要為了製造新劇情而無視舊劇情。


============================================================
【重要人物更新】
============================================================

每次 AI 回應都要檢查：

1. 本回合是否出現新的重要人物？
2. 如果有，加入 important_npcs。
3. 如果是已經存在的人物，更新他的資料。
4. 如果人物死亡或永久退場，remove=true。
5. 不重要的小角色不要加入。
6. 同一人物不能重複建立。
7. 名字相同但不是同一人的情況，要根據 role 和 history 判斷。

注意：

important_npcs 不需要每回合重新列出全部人物。

只需要回傳：

新增的重要人物
有明顯關係變化的重要人物
狀態發生變化的重要人物
需要更新記憶的重要人物
需要移除的重要人物

程式會自行保留之前的人物資料。


============================================================
【公司上市】
============================================================

公司上市不是遊戲結局。

如果玩家達成上市條件：

可以描寫公司上市。

可以增加：

聲望
資產
公司估值
人脈
新的 NPC
新的競爭
新的壓力

但是：

絕對不要讓上市導致 death。

不要讓遊戲停止。

不要寫：

「恭喜你完成遊戲。」

不要寫：

「你成功通關。」

上市只是玩家人生中的一個事件。

上市之後必須繼續生成下一個月劇情。


============================================================
【被警方逮捕】
============================================================

被捕不是遊戲結局。

如果玩家被逮捕：

arrested 可以設定為 true。

但不能讓遊戲停止。

後續可以描寫：

拘留
審訊
司法程序
判決
服刑
出獄
家人反應
兄弟反應
勢力變化
敵人趁機擴張
公司受到影響
人生重新開始

玩家仍然可以繼續活著。

只有玩家死亡才會真正結束遊戲。


============================================================
【輸出】
============================================================

只輸出合法 JSON。

不要 Markdown。

不要 ```json。

不要任何 JSON 外文字。

格式：

{
  "story": "本月完整開場劇情",

  "action_result": "完整描寫玩家這次行動的過程、人物互動、對話、結果與後續影響",

  "next_month_story": "下一個月300～600字左右的完整開場劇情",

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
    "health_change": 0,
    "health_reason": ""
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

  "important_npcs": [
    {
      "name": "人物名字",
      "role": "身分",
      "personality": "性格",
      "relationship": "與玩家關係",
      "affection_change": 0,
      "trust_change": 0,
      "respect_change": 0,
      "status": "活躍",
      "notes": "目前值得記住的事情",
      "keep": true,
      "remove": false
    }
  ],

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
"""


# ============================================================
# ④ 新遊戲
# ============================================================

def new_game():

    return {
        "save_version": 6,

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

        "important_npcs": [],

        "love_interest": None,

        "flags": [],
        "history": [],

        "current_story": None,

        "pending_result": None,

        "pending_next_story": None,

        "pending_next_choices": [],

        "current_choices": [],

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

            elif text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            result = json.loads(text)

            if not isinstance(result, dict):
                raise RuntimeError(
                    "AI 返回的資料格式不是 JSON 物件。"
                )

            return result

        except json.JSONDecodeError as e:

            if attempt < retries - 1:
                time.sleep(2)
                continue

            raise RuntimeError(
                f"AI 回傳的 JSON 格式錯誤：{e}"
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

        "important_npcs": state.get(
            "important_npcs",
            []
        ),

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

""" + action + """

現在請完整演出這個行動。


============================================================
【第一部分：action_result】
============================================================

這是最重要的部分。

action_result 必須是完整小說式劇情。

普通事件至少700字左右。

重要事件1000字以上。

重大事件可以1500～2500字。

不要只寫結果。

必須描寫：

1. 玩家準備做什麼
2. 玩家去了哪裡
3. 誰陪著玩家
4. 到達之後看到什麼
5. 見到了誰
6. NPC第一反應
7. 三兄弟各自的反應
8. 雙方對話
9. 玩家做出的行動
10. NPC如何回應
11. 局勢如何一步一步發展
12. 中間可以出現新的小變化
13. 最後結果
14. 對未來產生什麼影響

不要把幾天的事情濃縮成一句。

不要替玩家做出玩家沒有說過的重大決定。

如果玩家只是說「去找豹哥談談」，
你可以讓玩家去談，
但不要直接替玩家答應加入、簽約、背叛或其他重大決定。


============================================================
【劇情文字風格】
============================================================

要像長篇黑道人生小說。

要有：

場景感
人物動作
人物語氣
人物表情
對話
心理
氣氛
局勢
人物之間的關係

不要寫成遊戲系統報告。

不要一直在正文裡寫：

「聲望+1」
「阿豪信任+2」

數值交給 JSON。


============================================================
【第二部分：next_month_story】
============================================================

這個欄位非常重要。

它不是一句「一個月後發生某件事」。

它必須是：

「下一個月的完整開場劇情」。

長度約300～600字。

重大事件可以600～800字。

必須有：

場景
時間
人物
對話
兄弟反應
上一個月的後續
新的局勢
新的線索
新的問題
需要玩家做決定的局面

最後停在需要玩家做決定的位置。

不要替玩家做下一個重大決定。


============================================================
【第三部分：choices】
============================================================

choices 必須是針對 next_month_story 最後留下的局勢。

三個選項必須真的不同。

例如：

[
  "去找豹哥，直接談清楚這件事",
  "讓阿豪先調查事情背後的勢力",
  "暫時不接觸豹哥，先觀察街上的變化"
]

不要三個選項只是換句話說。


============================================================
【健康數值】
============================================================

這次非常重要。

健康不是固定每月下降。

如果本月劇情沒有：

受傷
生病
過度疲勞
重大身體壓力
其他合理健康事件

health_change 必須是：

0

正常生活、普通工作、聊天、吃飯、出門、
一般社交、一般談判，都不應該自動扣健康。

如果玩家真的受傷或生病：

輕微：
-1～-3

中度：
-3～-7

重大：
-5～-15

如果休息或治療後恢復，
才可以合理增加健康。

只要 health_change 不為0，
health_reason 必須寫明真正原因。

如果沒有健康事件：

"health_change": 0,
"health_reason": ""


============================================================
【重要人物】
============================================================

請檢查本回合是否：

1. 出現新的重要人物
2. 與既有重要人物互動
3. 某個重要人物死亡或永久退場

只有真正重要的人物才放進 important_npcs。

例如可以保存：

幫派頭目
地方大哥
重要幹部
重要官員
重要警方人物
重要政治人物
重要商人
重要中間人
長期競爭對手
重要朋友
重要敵人
重要感情角色

不要保存：

路人
店員
普通小混混
一次性角色
普通同學
只出現一次且沒有長期作用的人

如果是新的重要人物：

keep=true
remove=false

如果是已存在的重要人物，
更新其 relationship、status、notes，
並給合理的 affection_change、trust_change、respect_change。

如果重要人物死亡或永久退出故事：

remove=true

此時不要再把他當成活躍人物。

不要讓同一個人物重複建立。

important_npcs 只需要放：

新增的重要人物
或
這回合發生關係變化的重要人物
或
需要更新狀態的重要人物
或
需要移除的重要人物

不需要每回合重複列出所有人物。


============================================================
【數值】
============================================================

只合理修改。

普通事件：

0～2

重要事件：

1～5

重大事件：

最多約10。

不要一次：

+20
+30
+50

地下勢力尤其不能暴增。


============================================================
【世界連貫】
============================================================

務必參考 recent_history。

務必參考 important_npcs。

已經出現的重要人物必須保持記憶。

已經發生的事情必須產生後續影響。

NPC對玩家的態度必須合理。

不要每個月重新介紹同一個人物。

不要突然創造大量新幫派。


============================================================
【遊戲結束規則】
============================================================

這是最重要的規則之一：

只有玩家死亡才可以結束遊戲。

如果：

玩家被捕

不要結束。

如果：

玩家公司上市

不要結束。

如果：

玩家破產

不要結束。

如果：

玩家失去全部資產

不要結束。

如果：

玩家失去幫派

不要結束。

如果：

玩家勢力瓦解

不要結束。

如果：

玩家失戀

不要結束。

如果：

玩家名聲歸零

不要結束。

如果：

玩家警方注意度100

不要結束。

這些都只是劇情事件。

被捕可以讓：

"arrested": true

但仍然要生成：

next_month_story

並讓玩家繼續人生。

公司上市也一樣。

只有真正死亡時：

"death": true

才可以讓：

"alive": false

遊戲才會結束。

不要因為成功而結束。

不要因為失敗而結束。

玩家的人生必須持續到死亡。


============================================================
【輸出】
============================================================

只輸出合法 JSON。

不要 Markdown。

不要 ```json。

不要任何 JSON 外文字。

{
  "story": "...",
  "action_result": "...",
  "next_month_story": "...",
  "choices": [
    "...",
    "...",
    "..."
  ],
  "changes": {
    "cash_change": 0,
    "assets_change": 0,
    "company_value_change": 0,
    "legal_business_change": 0,
    "power_change": 0,
    "reputation_change": 0,
    "police_attention_change": 0,
    "health_change": 0,
    "health_reason": ""
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
  "important_npcs": [
    {
      "name": "",
      "role": "",
      "personality": "",
      "relationship": "",
      "affection_change": 0,
      "trust_change": 0,
      "respect_change": 0,
      "status": "活躍",
      "notes": "",
      "keep": true,
      "remove": false
    }
  ],
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

不要第一個月就直接讓玩家成為黑道老大。

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

本月開場 story 約300～600字。

必須有：

場景
人物
兄弟互動
對話
生活細節
至少一個可以讓玩家做決定的局面

此時 action_result 可以留空。

next_month_story 可以留空。

changes全部為0。

health_change必須為0。

health_reason必須為""。

兄弟關係全部為0。

important_npcs應該為空陣列。

love.created必須為false。

遊戲沒有上市結局。

遊戲沒有被捕結局。

玩家會一直玩到死亡才真正結束。
"""


    return json.dumps(
        data,
        ensure_ascii=False
    )


# ============================================================
# ⑦ 數值安全
# ============================================================

def safe_number(value):

    if isinstance(value, bool):
        return 0

    if isinstance(value, (int, float)):
        return value

    return 0


# ============================================================
# ⑧ NPC 工具
# ============================================================

def normalize_npc(npc):

    if not isinstance(npc, dict):
        return None

    name = str(
        npc.get("name", "")
    ).strip()

    if not name:
        return None

    return {
        "name": name,

        "role": str(
            npc.get(
                "role",
                "重要人物"
            )
        ).strip(),

        "personality": str(
            npc.get(
                "personality",
                "個性未明"
            )
        ).strip(),

        "relationship": str(
            npc.get(
                "relationship",
                "認識"
            )
        ).strip(),

        "affection": max(
            0,
            min(
                100,
                safe_number(
                    npc.get(
                        "affection",
                        0
                    )
                )
            )
        ),

        "trust": max(
            0,
            min(
                100,
                safe_number(
                    npc.get(
                        "trust",
                        0
                    )
                )
            )
        ),

        "respect": max(
            0,
            min(
                100,
                safe_number(
                    npc.get(
                        "respect",
                        0
                    )
                )
            )
        ),

        "status": str(
            npc.get(
                "status",
                "活躍"
            )
        ).strip(),

        "notes": str(
            npc.get(
                "notes",
                ""
            )
        ).strip()
    }


def find_npc(state, name):

    for npc in state.get(
        "important_npcs",
        []
    ):

        if npc.get("name") == name:
            return npc

    return None


def apply_npc_changes(state, result):

    npc_changes = result.get(
        "important_npcs",
        []
    )

    if not isinstance(
        npc_changes,
        list
    ):
        return

    if "important_npcs" not in state:
        state["important_npcs"] = []

    for raw_npc in npc_changes:

        if not isinstance(
            raw_npc,
            dict
        ):
            continue

        name = str(
            raw_npc.get(
                "name",
                ""
            )
        ).strip()

        if not name:
            continue

        remove = bool(
            raw_npc.get(
                "remove",
                False
            )
        )

        existing = find_npc(
            state,
            name
        )

        # ========================================================
        # 移除重要人物
        # ========================================================

        if remove:

            state["important_npcs"] = [
                npc
                for npc in state["important_npcs"]
                if npc.get("name") != name
            ]

            continue

        # ========================================================
        # 更新既有人物
        # ========================================================

        if existing:

            for field in [
                "role",
                "personality",
                "relationship",
                "status",
                "notes"
            ]:

                value = raw_npc.get(
                    field,
                    None
                )

                if value is not None:

                    value = str(
                        value
                    ).strip()

                    if value:
                        existing[field] = value

            for field in [
                "affection",
                "trust",
                "respect"
            ]:

                change = safe_number(
                    raw_npc.get(
                        field + "_change",
                        0
                    )
                )

                change = max(
                    -10,
                    min(
                        10,
                        change
                    )
                )

                existing[field] = max(
                    0,
                    min(
                        100,
                        existing.get(
                            field,
                            0
                        ) + change
                    )
                )

            continue

        # ========================================================
        # 新增人物
        # ========================================================

        keep = raw_npc.get(
            "keep",
            True
        )

        if not keep:
            continue

        new_npc = {

            "name": name,

            "role": str(
                raw_npc.get(
                    "role",
                    "重要人物"
                )
            ).strip(),

            "personality": str(
                raw_npc.get(
                    "personality",
                    "個性未明"
                )
            ).strip(),

            "relationship": str(
                raw_npc.get(
                    "relationship",
                    "認識"
                )
            ).strip(),

            "affection": 0,

            "trust": 0,

            "respect": 0,

            "status": str(
                raw_npc.get(
                    "status",
                    "活躍"
                )
            ).strip(),

            "notes": str(
                raw_npc.get(
                    "notes",
                    ""
                )
            ).strip()
        }

        # 新人物第一次出現，
        # 關係只能小幅增加。
        for field in [
            "affection",
            "trust",
            "respect"
        ]:

            change = safe_number(
                raw_npc.get(
                    field + "_change",
                    0
                )
            )

            change = max(
                0,
                min(
                    5,
                    change
                )
            )

            new_npc[field] = change

        state["important_npcs"].append(
            new_npc
        )


# ============================================================
# ⑨ 健康安全檢查
# ============================================================

def sanitize_health_change(result):

    changes = result.get(
        "changes",
        {}
    )

    if not isinstance(
        changes,
        dict
    ):
        return

    health_change = safe_number(
        changes.get(
            "health_change",
            0
        )
    )

    reason = str(
        changes.get(
            "health_reason",
            ""
        )
    ).strip()

    # 沒有理由就不能改健康
    if health_change != 0 and not reason:

        changes["health_change"] = 0
        changes["health_reason"] = ""

        return

    # 沒有健康變化就清空理由
    if health_change == 0:

        changes["health_change"] = 0
        changes["health_reason"] = ""

        return

    # 限制單回合健康變化
    changes["health_change"] = max(
        -15,
        min(
            10,
            health_change
        )
    )


# ============================================================
# ⑩ 套用數值
# ============================================================

def apply_changes(state, result):

    sanitize_health_change(
        result
    )

    p = state["player"]

    changes = result.get(
        "changes",
        {}
    )

    if not isinstance(
        changes,
        dict
    ):
        changes = {}

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
                min(
                    100000,
                    value
                )
            )

        else:

            value = max(
                -10,
                min(
                    10,
                    value
                )
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

    # ========================================================
    # 兄弟關係
    # ========================================================

    brothers = result.get(
        "brothers",
        {}
    )

    if not isinstance(
        brothers,
        dict
    ):
        brothers = {}

    for name, data in brothers.items():

        if name not in state["brothers"]:
            continue

        if not isinstance(
            data,
            dict
        ):
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

    # ========================================================
    # 重要 NPC
    # ========================================================

    apply_npc_changes(
        state,
        result
    )

    # ========================================================
    # 戀愛
    # ========================================================

    love_data = result.get(
        "love",
        {}
    )

    if not isinstance(
        love_data,
        dict
    ):
        love_data = {}

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
                min(
                    5,
                    change
                )
            )

            love[field] += change

            love[field] = max(
                0,
                min(
                    100,
                    love[field]
                )
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
        love_data.get(
            "created",
            False
        )
    ):

        p = state["player"]

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

    flags_add = result.get(
        "flags_add",
        []
    )

    if isinstance(
        flags_add,
        list
    ):

        for flag in flags_add:

            if (
                isinstance(
                    flag,
                    str
                )
                and
                flag not in state["flags"]
            ):

                state["flags"].append(
                    flag
                )

    flags_remove = result.get(
        "flags_remove",
        []
    )

    if isinstance(
        flags_remove,
        list
    ):

        for flag in flags_remove:

            if flag in state["flags"]:

                state["flags"].remove(
                    flag
                )

    # ========================================================
    # 人生狀態
    # ========================================================

    # 只有死亡才會真正結束遊戲。
    if result.get(
        "death",
        False
    ):

        p["alive"] = False

    # 被捕只是人生事件，不會結束遊戲。
    if result.get(
        "arrested",
        False
    ):

        p["arrested"] = True

    # listed 保留資料相容性，
    # 但不再造成任何遊戲結束。
    if result.get(
        "listed",
        False
    ):

        p["listed"] = True


# ============================================================
# ⑪ 世界時間
# ============================================================

def world_tick(state):

    p = state["player"]

    # 合法事業被動收入
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

    # 公司成長
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
# ⑫ 記憶
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

    if len(
        state["history"]
    ) > 40:

        state["history"] = (
            state["history"][-40:]
        )


# ============================================================
# ⑬ 存檔
# ============================================================

def create_save_data(state):

    return {

        "game_name":
            "地下帝國：模擬人生",

        "save_version":
            6,

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

        # ========================================================
        # 舊存檔相容
        # ========================================================

        defaults = {

            "love_interest": None,

            "important_npcs": [],

            "flags": [],

            "history": [],

            "current_story": None,

            "pending_result": None,

            "pending_next_story": None,

            "pending_next_choices": [],

            "current_choices": [],

            "phase": "playing",

            "game_started": True
        }

        for key, value in defaults.items():

            if key not in game:

                game[key] = value

        # ========================================================
        # 玩家資料相容
        # ========================================================

        player_defaults = {

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
        }

        for key, value in player_defaults.items():

            if key not in game["player"]:

                game["player"][key] = value

        # ========================================================
        # 清理重要人物
        # ========================================================

        if not isinstance(
            game.get(
                "important_npcs"
            ),
            list
        ):

            game["important_npcs"] = []

        clean_npcs = []

        for npc in game["important_npcs"]:

            normalized = normalize_npc(
                npc
            )

            if normalized:

                clean_npcs.append(
                    normalized
                )

        game["important_npcs"] = clean_npcs

        # ========================================================
        # current_choices
        # ========================================================

        if not isinstance(
            game.get(
                "current_choices"
            ),
            list
        ):

            game["current_choices"] = []

        if not isinstance(
            game.get(
                "pending_next_choices"
            ),
            list
        ):

            game["pending_next_choices"] = []

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
# ⑭ CSS
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

    .npc-box {
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #555;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ⑮ Session State
# ============================================================

if "game" not in st.session_state:

    st.session_state.game = new_game()


if "selected_action" not in st.session_state:

    st.session_state.selected_action = ""


state = st.session_state.game

p = state["player"]


# ============================================================
# ⑯ 標題
# ============================================================

st.markdown(
    '<div class="main-title">👑 地下帝國：模擬人生</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI 驅動的黑道人生模擬 RPG</div>',
    unsafe_allow_html=True
)


# ============================================================
# ⑰ 存檔 / 讀檔
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

                    st.session_state.selected_action = ""

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
# ⑱ 開始畫面
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

        沒有固定的成功結局。

        你的人生會一直持續，

        ### 直到你死亡。
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
# ⑲ 結局
# ============================================================

# ============================================================
# 只有玩家死亡才會結束遊戲
# ============================================================

if not p["alive"]:

    st.error(
        "☠️ 你的人生結束了。"
    )

    st.write(
        f"你享年 {p['age']} 歲。"
    )

    st.write(
        "你的地下帝國、兄弟、敵人與所有人生故事，"
        "也在這一刻畫下句點。"
    )

    if st.button(
        "重新開始",
        use_container_width=True
    ):

        st.session_state.game = new_game()

        st.session_state.selected_action = ""

        st.rerun()

    st.stop()


# ============================================================
# 注意：
# 被捕不會結束遊戲
# 公司上市不會結束遊戲
# ============================================================

if p["arrested"]:

    st.warning(
        "🚔 目前你處於被警方逮捕／司法程序相關狀態。"
    )

    st.caption(
        "這不會結束你的人生。"
        "後續劇情仍會繼續。"
    )


# ============================================================
# ⑳ 狀態
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
# ㉑ 三兄弟
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
# ㉒ 重要人物
# ============================================================

important_npcs = state.get(
    "important_npcs",
    []
)

with st.expander(
    f"👥 我認識的人（{len(important_npcs)}）"
):

    if not important_npcs:

        st.caption(
            "目前還沒有值得長期記錄的重要人物。"
        )

        st.caption(
            "普通路人、小混混與一次性角色不會被保存。"
        )

    else:

        for npc in important_npcs:

            st.markdown(
                f"### {npc['name']}"
            )

            st.write(
                f"**身分：** {npc['role']}"
            )

            st.write(
                f"**關係：** {npc['relationship']}"
            )

            st.write(
                f"**狀態：** {npc['status']}"
            )

            col_a, col_b, col_c = st.columns(3)

            with col_a:

                st.metric(
                    "好感",
                    f"{int(npc['affection'])}/100"
                )

            with col_b:

                st.metric(
                    "信任",
                    f"{int(npc['trust'])}/100"
                )

            with col_c:

                st.metric(
                    "尊重",
                    f"{int(npc['respect'])}/100"
                )

            st.caption(
                f"性格：{npc['personality']}"
            )

            if npc.get("notes"):

                st.caption(
                    f"記憶：{npc['notes']}"
                )

            st.divider()


# ============================================================
# ㉓ 戀愛
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
# ㉔ 第一個月開場
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

            if not isinstance(
                state["current_choices"],
                list
            ):

                state["current_choices"] = []

            state["current_choices"] = (
                state["current_choices"][:3]
            )

            apply_npc_changes(
                state,
                result
            )

            state["phase"] = "playing"

        except Exception as e:

            st.error(
                str(e)
            )

            st.stop()


# ============================================================
# ㉕ 本月劇情 / 行動
# ============================================================

if state["phase"] == "playing":

    st.subheader(
        f"📖 {p['age']}歲・第{p['month']}個月"
    )

    story_text = html.escape(
        str(
            state["current_story"]
            or
            "你的故事即將開始。"
        )
    )

    st.markdown(
        f"""
        <div class="story-box">
        {story_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # 三個選項
    # ========================================================

    choices = state.get(
        "current_choices",
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

                    st.session_state.selected_action = (
                        str(choice)
                    )

                    st.rerun()

    # ========================================================
    # 玩家自由輸入
    # ========================================================

    st.write(
        "### ✍️ 自由行動"
    )

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

        action = action.strip()

        if not action:

            st.warning(
                "請先輸入你的行動。"
            )

        else:

            with st.spinner(
                "🤖 AI 正在演出你的行動..."
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

            # ==================================================
            # 套用數值
            # ==================================================

            apply_changes(
                state,
                result
            )

            # ==================================================
            # 記憶
            # ==================================================

            add_memory(
                state,
                action,
                result
            )

            # ==================================================
            # 儲存下一個月劇情
            # ==================================================

            next_story = result.get(
                "next_month_story",
                ""
            )

            if (
                not isinstance(
                    next_story,
                    str
                )
                or
                not next_story.strip()
            ):

                next_story = (
                    "新的一個月開始了。"
                    "上個月留下的事情並沒有真正結束，"
                    "而新的變化正在慢慢浮現。"
                )

            state["pending_next_story"] = (
                next_story.strip()
            )

            # ==================================================
            # 儲存下一個月選項
            # ==================================================

            next_choices = result.get(
                "choices",
                []
            )

            if not isinstance(
                next_choices,
                list
            ):

                next_choices = []

            state["pending_next_choices"] = [
                str(x)
                for x in next_choices[:3]
                if str(x).strip()
            ]

            # ==================================================
            # 儲存本月行動結果
            # ==================================================

            action_result = result.get(
                "action_result",
                "這個行動產生了一些變化。"
            )

            if not isinstance(
                action_result,
                str
            ):

                action_result = str(
                    action_result
                )

            state["pending_result"] = (
                action_result
            )

            # ==================================================
            # 覆蓋目前畫面
            # ==================================================

            state["current_story"] = (
                state["pending_result"]
            )

            state["current_choices"] = []

            state["phase"] = "action_result"

            st.session_state.selected_action = ""

            st.rerun()


# ============================================================
# ㉖ 行動結果
# ============================================================

if state["phase"] == "action_result":

    st.subheader(
        "🎬 本月行動結果"
    )

    result_text = html.escape(
        str(
            state["pending_result"]
            or
            "這個行動產生了一些變化。"
        )
    )

    st.markdown(
        f"""
        <div class="result-box">
        {result_text}
        </div>
        """,
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
        # 如果玩家死亡
        # ====================================================

        if not state["player"]["alive"]:

            st.rerun()

        # ====================================================
        # 正式進入下一個月
        # ====================================================

        world_tick(
            state
        )

        # ====================================================
        # 顯示之前已經生成好的 next_month_story
        # ====================================================

        state["current_story"] = (
            state["pending_next_story"]
            or
            "新的一個月開始了。"
        )

        # ====================================================
        # 下一個月選項
        # ====================================================

        state["current_choices"] = (
            state.get(
                "pending_next_choices",
                []
            )
        )

        if not isinstance(
            state["current_choices"],
            list
        ):

            state["current_choices"] = []

        state["current_choices"] = (
            state["current_choices"][:3]
        )

        # ====================================================
        # 清理上一回合暫存
        # ====================================================

        state["pending_result"] = None

        state["pending_next_story"] = None

        state["pending_next_choices"] = []

        # ====================================================
        # 回到正常遊戲
        # ====================================================

        state["phase"] = "playing"

        st.session_state.selected_action = ""

        st.rerun()


# ============================================================
# ㉗ 人生記錄
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
# ㉘ 重新開始
# ============================================================

st.divider()

if st.button(
    "🔄 重新開始人生",
    use_container_width=True
):

    st.session_state.game = new_game()

    st.session_state.selected_action = ""

    st.rerun()
