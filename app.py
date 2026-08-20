import streamlit as st
import json
import random
import time
from google import genai

st.set_page_config(page_title='地下帝國：AI人生', page_icon='👑', layout='wide')

try:
    API_KEY = st.secrets['GEMINI_API_KEY']
except Exception:
    API_KEY = None

if not API_KEY:
    st.error('找不到 GEMINI_API_KEY')
    st.info('請到 Streamlit Cloud → Settings → Secrets 設定 GEMINI_API_KEY。')
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL = 'gemini-3.1-flash-lite'

SYSTEM_PROMPT = r'''
你是《地下帝國：AI人生》的核心 AI Game Master。
這是一個長篇、自由選擇、AI 驅動的黑道人生模擬 RPG。
玩家18歲開始，普通家庭，沒有背景、人脈或特殊能力。核心不是正經商業模擬，而是黑道、地下勢力、幫派、地盤、兄弟、利益、人情、衝突、背叛、權力、地下人物與警方壓力。
合法工作與正當生意可以存在，但不能把玩家強行導向創業。
可以描寫虛構事件、人物、衝突、結果、風險、心理、警方反應、勢力變化與人物關係，但不要提供現實世界可直接執行的犯罪操作、逃避警方方法、武器製作、毒品製造或具體犯罪技巧。

三兄弟：
阿龍：沉穩、重義氣、保護兄弟、遇事穩、不喜歡無意義冒險。
阿虎：衝動、好勝、敢冒險、容易被挑釁、喜歡直接解決問題。
阿豪：冷靜、聰明、擅長分析、觀察局勢、不喜歡沒把握的行動。
三人有自己的性格、底線、利益、情緒、忠誠、信任與尊重，可以反對玩家、失望、提升或降低關係。

世界會自行運作。其他幫派會擴張、競爭、談判、發生衝突、換老大、招募新人、失去地盤或內鬥。普通月份不要硬塞大型事件；大型事件不能連續發生。人物與幫派一旦出現，要有記憶與持續性。

成長必須慢：普通人→地方小人物→小頭目→地方勢力→區域勢力→大型幫派。不可突然成為大哥、控制城市或認識最高層人物。

NPC有利益、恐懼、性格、目標、底線、關係與記憶，不是工具人。他們可以幫助、拒絕、懷疑、利用、嫉妒、競爭、背叛或離開。

關係數值慢慢變化。普通事件約0~2，重要事件約3~5，禁止一次暴增20以上。

戀愛必須自然：陌生→認識→朋友→熟悉→曖昧→交往。戀愛NPC有自己的生活、家庭、學業或工作、夢想、價值觀與底線，不可第一個月硬塞女友。

最重要：玩家輸入行動後，絕對不能只寫結果。必須完整演出過程。要寫玩家如何準備、去哪裡、見到誰、兄弟如何反應、NPC如何反應、雙方對話、玩家做了什麼、對方如何回應、事情如何一步一步發展、最後結果與後續影響。

action_result 建議 900~1800 字；重大事件可1500~2500字。必須有場景、人物、對話、動作、反應、心理、氣氛、結果與後續影響。不要用幾句旁白直接跨過一整個月。

玩家沒有做出的重大決定不能由AI代替。例如玩家說去找豹哥，只能演出見面與談判，不能擅自讓玩家答應加入、背叛、殺人或花掉全部資產。

每次行動後都要生成下一個月的「開場」，但不能替玩家做下一個月的行動。下一月開場應該像小說場景，例如：上一月事件造成的餘波、人物傳話、環境變化、新人物出現、兄弟討論等；不要只寫「一個月後……」一句話。next_month_story 建議 500~900 字，要讓玩家能感覺事情正在發展，而且結尾要留下可以行動的局面。

每次都提供3個有差異的建議行動。選項要針對「下一月看到的開場局勢」，不是重複上一月行動。

每個月一回合。按下執行行動後，只顯示本月行動結果；不要立刻顯示next_month_story。玩家按「繼續」後，才把next_month_story覆蓋到畫面，並進入下一月。不要再次呼叫AI生成該next_month_story。

只輸出合法 JSON，不要Markdown。
'''


def new_game():
    return {
        'save_version': 3,
        'player': {'name':'你','age':18,'month':1,'cash':0,'assets':0,'company_value':0,'legal_business':0,'power':0,'reputation':0,'police_attention':0,'health':100,'alive':True,'arrested':False,'listed':False},
        'brothers': {
            '阿龍': {'age':18,'loyalty':88,'trust':80,'respect':80,'ability':65,'personality':'沉穩、重義氣、保護兄弟'},
            '阿虎': {'age':18,'loyalty':78,'trust':70,'respect':72,'ability':75,'personality':'衝動、好勝、敢冒險'},
            '阿豪': {'age':18,'loyalty':92,'trust':85,'respect':86,'ability':58,'personality':'冷靜、聰明、擅長分析'}},
        'love_interest':None,'flags':[],'history':[],'current_story':None,'pending_result':None,'pending_next_story':None,'pending_next_choices':[],'phase':'playing','game_started':False
    }


def clean_json(text):
    text = (text or '').strip()
    if text.startswith('```json'): text = text[7:]
    elif text.startswith('```'): text = text[3:]
    if text.endswith('```'): text = text[:-3]
    return text.strip()


def call_ai(prompt, retries=2):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={'system_instruction':SYSTEM_PROMPT,'response_mime_type':'application/json'}
            )
            if not response.text: raise RuntimeError('AI 沒有返回內容')
            return json.loads(clean_json(response.text))
        except Exception as e:
            msg = str(e)
            if '429' in msg or 'RESOURCE_EXHAUSTED' in msg:
                if attempt < retries-1: time.sleep(3); continue
                raise RuntimeError('Gemini 免費額度已達上限，請稍後再試。')
            if '404' in msg:
                raise RuntimeError(f'Gemini 模型 {MODEL} 無法使用，請確認 API Key 可使用此模型。')
            if '401' in msg or '403' in msg:
                raise RuntimeError('Gemini API Key 無效或沒有 API 權限。')
            if attempt < retries-1: time.sleep(2); continue
            raise RuntimeError(f'AI 發生錯誤：{msg}')
    raise RuntimeError('AI 暫時無法使用。')


def build_turn_prompt(state, action=None):
    p = state['player']
    data = {
        'current_date': {'age':p['age'],'month':p['month']},
        'player':p,'brothers':state['brothers'],'love_interest':state['love_interest'],
        'flags':state['flags'],'recent_history':state['history'][-10:],
        'current_story':state['current_story'],'player_action':action
    }
    if action:
        data['task'] = '''
玩家剛剛做出這個行動：
【玩家行動】
%s

請把這個行動寫成完整小說式事件，不要跳結果。
至少依序呈現：準備→前往→見人→兄弟反應→NPC反應→多輪對話→玩家實際行動→對方反應→局勢發展→結果→後續影響。
不要把玩家沒有說的重大決定自動做掉。

【長度要求】
action_result 至少900字；若事件本身較大可1500~2500字。不要用一句「談完後」或「一個月後」跳過過程。對話要具體，人物要有各自語氣，兄弟不能只當旁白。

【下一月開場】
另外生成 next_month_story，500~900字左右。它必須是下一個月「剛開始」時發生的場景與局勢，不是下一月完整結果。要承接本月事件的餘波，寫出人物、環境、對話或新訊息，最後留下玩家可以處理的局面。不要替玩家做下一月行動。

【選項】
提供3個針對下一月開場的不同方向，每個選項是玩家下一步可以做的事。
''' % action
    else:
        data['task'] = '''
這是新遊戲，生成18歲第1個月的開場劇情。
story 500~900字，讓玩家真正看到自己的生活、三兄弟、地方環境與可以發展的線索。不要第一個月直接成為黑道成員或大哥。最後提供3個不同方向的建議行動。
'''
    # 關鍵修正：不再用 f-string 塞 JSON/大括號，因此不會出現 Invalid format specifier。
    return json.dumps(data, ensure_ascii=False, indent=2)


def safe_number(v): return v if isinstance(v,(int,float)) and not isinstance(v,bool) else 0


def apply_changes(state,result):
    p=state['player']; changes=result.get('changes',{})
    fields=['cash','assets','company_value','legal_business','power','reputation','police_attention','health']
    for field in fields:
        v=safe_number(changes.get(field+'_change',0))
        v=max(-100000,min(100000,v)) if field in ['cash','assets','company_value'] else max(-10,min(10,v))
        p[field]+=v
    p['cash']=max(0,p['cash']); p['assets']=max(0,p['assets']); p['company_value']=max(0,p['company_value'])
    p['legal_business']=max(0,min(100,p['legal_business'])); p['power']=max(0,p['power']); p['reputation']=max(0,p['reputation']); p['police_attention']=max(0,min(100,p['police_attention'])); p['health']=max(0,min(100,p['health']))
    for name,d in result.get('brothers',{}).items():
        if name not in state['brothers']: continue
        for f in ['loyalty','trust','respect']:
            v=max(-5,min(5,safe_number(d.get(f+'_change',0))))
            state['brothers'][name][f]=max(0,min(100,state['brothers'][name][f]+v))
    love=result.get('love',{})
    if state['love_interest']:
        l=state['love_interest']
        for f in ['affection','trust','respect']:
            l[f]=max(0,min(100,l[f]+max(-5,min(5,safe_number(love.get(f+'_change',0))))))
        a=l['affection']; l['relationship']='陌生' if a<20 else '認識' if a<40 else '朋友' if a<60 else '曖昧' if a<75 else '交往' if a<90 else '深度交往'
    elif love.get('created') and (p['age']>18 or p['month']>2) and love.get('name'):
        state['love_interest']={'name':love['name'],'personality':love.get('personality','個性獨立'),'affection':1,'trust':1,'respect':1,'relationship':'認識'}
    for f in result.get('flags_add',[]):
        if f not in state['flags']: state['flags'].append(f)
    for f in result.get('flags_remove',[]):
        if f in state['flags']: state['flags'].remove(f)
    if result.get('death'): p['alive']=False
    if result.get('arrested'): p['arrested']=True
    if result.get('listed'): p['listed']=True


def world_tick(state):
    p=state['player']
    if p['legal_business']>0: p['cash']+=int(p['legal_business']*random.randint(50,150))
    if p['legal_business']>=10: p['company_value']+=int(p['legal_business']*random.randint(50,200))
    p['month']+=1
    if p['month']>12:
        p['month']=1; p['age']+=1
        for b in state['brothers'].values(): b['age']+=1


def add_memory(state,action,result):
    state['history'].append({'age':state['player']['age'],'month':state['player']['month'],'action':action,'result':result.get('action_result','')[-4000:]})
    state['history']=state['history'][-40:]


def save_game(state):
    return json.dumps({'game_name':'地下帝國：AI人生','save_version':3,'saved_at':time.strftime('%Y-%m-%d %H:%M:%S'),'game':state},ensure_ascii=False,indent=2)


def load_game(f):
    data=json.load(f)
    if 'game' not in data: raise ValueError('這不是有效的地下帝國存檔。')
    g=data['game']
    defaults={'love_interest':None,'flags':[],'history':[],'current_story':None,'pending_result':None,'pending_next_story':None,'pending_next_choices':[],'phase':'playing','game_started':True}
    for k,v in defaults.items(): g.setdefault(k,v)
    return g

st.markdown('''<style>.main-title{text-align:center;font-size:42px;font-weight:bold}.subtitle{text-align:center;color:#888;margin-bottom:25px}.story-box,.result-box{padding:24px;border-radius:12px;border:1px solid #555;line-height:2;font-size:17px;white-space:pre-wrap}</style>''',unsafe_allow_html=True)

if 'game' not in st.session_state: st.session_state.game=new_game()
state=st.session_state.game; p=state['player']

st.markdown('<div class="main-title">👑 地下帝國：AI人生</div>',unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI 驅動的黑道人生模擬 RPG</div>',unsafe_allow_html=True)

with st.expander('💾 存檔 / 讀檔'):
    c1,c2=st.columns(2)
    with c1:
        st.download_button('💾 下載目前存檔',save_game(state),file_name=f"地下帝國_{p['age']}歲_第{p['month']}個月.json",mime='application/json',use_container_width=True)
    with c2:
        up=st.file_uploader('📂 選擇存檔',type=['json'],key='save_uploader')
        if up and st.button('▶️ 載入這個存檔',use_container_width=True):
            try: st.session_state.game=load_game(up); st.rerun()
            except Exception as e: st.error(f'讀取存檔失敗：{e}')

if not state['game_started']:
    st.markdown('''## 你的故事開始了\n\n18歲。你出生於普通家庭，沒有資產、背景、人脈。\n\n但你有三個從小一起長大的兄弟：\n\n**阿龍** 沉穩、重義氣。\n\n**阿虎** 衝動、敢冒險。\n\n**阿豪** 冷靜、擅長分析。''')
    if st.button('🎮 開始人生',type='primary',use_container_width=True): state['game_started']=True; st.rerun()
    st.stop()

if not p['alive']:
    st.error('☠️ 你的人生結束了。'); st.write(f"你享年 {p['age']} 歲。")
    if st.button('重新開始'): st.session_state.game=new_game(); st.rerun()
    st.stop()
if p['arrested']:
    st.error('🚔 你被警方逮捕。'); st.write('你的人生迎來重大轉折。')
    if st.button('重新開始'): st.session_state.game=new_game(); st.rerun()
    st.stop()
if p['listed']:
    st.success('🏆 公司成功上市！')
    if st.button('重新開始'): st.session_state.game=new_game(); st.rerun()
    st.stop()

st.subheader(f"📅 {p['age']}歲・第{p['month']}個月")
cols=st.columns(4)
for c,label,val in zip(cols,['💰 現金','🏠 資產','🏢 公司估值','❤️ 健康'],[f"${int(p['cash']):,}",f"${int(p['assets']):,}",f"${int(p['company_value']):,}",f"{int(p['health'])}/100"]): c.metric(label,val)
cols=st.columns(4)
for c,label,val in zip(cols,['🏦 合法事業','👑 地下勢力','⭐ 聲望','👮 警方注意度'],[f"{int(p['legal_business'])}/100",int(p['power']),int(p['reputation']),f"{int(p['police_attention'])}/100"]): c.metric(label,val)

with st.expander('👊 三兄弟'):
    for n,b in state['brothers'].items(): st.write(f"### {n}"); st.write(f"忠誠：{b['loyalty']}　信任：{b['trust']}　尊重：{b['respect']}　能力：{b['ability']}"); st.caption(b['personality'])
if state['love_interest']:
    l=state['love_interest']
    with st.expander(f"❤️ {l['name']}"): st.write(f"關係：{l['relationship']}　好感：{l['affection']}/100　信任：{l['trust']}/100　尊重：{l['respect']}/100"); st.write(f"性格：{l['personality']}")
else:
    with st.expander('❤️ 感情'): st.write('目前沒有戀愛對象。')

if state['current_story'] is None and state['phase']=='playing':
    with st.spinner('🤖 AI 正在建立你的世界...'):
        try:
            r=call_ai(build_turn_prompt(state)); state['current_story']=r.get('story','你的故事即將開始。'); state['pending_next_choices']=r.get('choices',[])[:3]
        except Exception as e: st.error(str(e)); st.stop()

if state['phase']=='playing':
    st.subheader('📖 本月劇情'); st.markdown(f'<div class="story-box">{state["current_story"]}</div>',unsafe_allow_html=True)
    choices=state.get('pending_next_choices',[])
    if choices:
        st.write('### 🎮 建議行動'); cc=st.columns(3)
        for i,ch in enumerate(choices[:3]):
            with cc[i]:
                if st.button(f'{i+1}. {ch}',key=f"choice_{p['age']}_{p['month']}_{i}",use_container_width=True):
                    st.session_state.action_text=ch
                    st.rerun()
    selected=st.session_state.get('action_text','')
    # 不在 widget 建立後直接改 widget 對應的 session_state；按鈕只把選項存到另一個鍵。
    with st.form('action_form',clear_on_submit=True):
        action=st.text_area('你想做什麼？',value=selected,placeholder='例如：我跟阿豪去找附近的地方人物，先了解這條街的情況。',height=150)
        submitted=st.form_submit_button('⚡ 執行行動',type='primary',use_container_width=True)
    if submitted:
        if not action.strip(): st.warning('請先輸入你的行動。'); st.stop()
        with st.spinner('🤖 AI 正在演出你的行動...'):
            try: result=call_ai(build_turn_prompt(state,action.strip()))
            except Exception as e: st.error(str(e)); st.stop()
        apply_changes(state,result); add_memory(state,action.strip(),result)
        state['pending_result']=result.get('action_result','這個行動產生了一些變化。')
        state['pending_next_story']=result.get('next_month_story','新的一個月開始了。')
        state['pending_next_choices']=result.get('choices',[])[:3]
        state['current_story']=state['pending_result']; state['phase']='action_result'
        st.session_state.pop('action_text',None)
        st.rerun()

if state['phase']=='action_result':
    st.subheader('🎬 劇情結果'); st.markdown(f'<div class="result-box">{state["pending_result"]}</div>',unsafe_allow_html=True); st.divider(); st.info('本月行動已結束。按下「繼續」後才會進入下一個月。')
    if st.button('▶️ 繼續・進入下一個月',type='primary',use_container_width=True):
        world_tick(state)
        state['current_story']=state.get('pending_next_story') or '新的一個月開始了。'
        state['pending_result']=None; state['pending_next_story']=None; state['phase']='playing'
        # pending_next_choices 已經是「下一月」選項，不要清掉。
        st.session_state.pop('action_text',None)
        st.rerun()

with st.expander('📜 人生記錄'):
    if not state['history']: st.caption('目前還沒有歷史記錄。')
    for m in reversed(state['history'][-10:]):
        st.markdown(f"**{m['age']}歲・第{m['month']}個月**"); st.write(f"你的行動：{m['action']}"); st.write(m['result']); st.divider()

st.divider()
if st.button('🔄 重新開始人生',use_container_width=True): st.session_state.game=new_game(); st.session_state.pop('action_text',None); st.rerun()
