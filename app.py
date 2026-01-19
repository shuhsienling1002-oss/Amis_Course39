import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 39: O Faloco'", page_icon="❤️", layout="centered")

# --- CSS 美化 (溫暖粉紅與深紅) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #F8BBD0; color: #880E4F; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FCE4EC 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #C2185B;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #AD1457; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FCE4EC;
        border-left: 5px solid #F48FB1;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #F8BBD0; color: #880E4F; border: 2px solid #C2185B; padding: 12px;
    }
    .stButton>button:hover { background-color: #F48FB1; border-color: #AD1457; }
    .stProgress > div > div > div > div { background-color: #C2185B; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 39: 19個單字 - User Fix) ---
vocab_data = [
    {"amis": "Faloco'", "chi": "心 / 心意 (詞根)", "icon": "❤️", "source": "Row 429", "morph": "Root"},
    {"amis": "Lipahak", "chi": "快樂 (詞根)", "icon": "😄", "source": "Row 4640", "morph": "Root"},
    {"amis": "Malipahak", "chi": "感到快樂", "icon": "🥳", "source": "Row 4640", "morph": "Ma-Lipahak"},
    {"amis": "Rarom", "chi": "難過 / 憂傷 (詞根)", "icon": "😢", "source": "Standard", "morph": "Root"},
    {"amis": "Mararom", "chi": "感到難過", "icon": "😭", "source": "Standard", "morph": "Ma-Rarom"},
    {"amis": "Olah", "chi": "愛 / 喜歡 (詞根)", "icon": "🤟", "source": "Standard", "morph": "Root"},
    {"amis": "Maolah", "chi": "去愛 / 喜歡", "icon": "😍", "source": "Standard", "morph": "Ma-Olah"},
    {"amis": "Limela", "chi": "珍惜 (詞根)", "icon": "💎", "source": "Row 490", "morph": "Root"},
    {"amis": "Misalimela", "chi": "愛惜 / 珍惜 (主動)", "icon": "🤲", "source": "User Fix", "morph": "Misa-Limela"}, # 修正
    {"amis": "Tangic", "chi": "哭 (詞根)", "icon": "💧", "source": "Row 238", "morph": "Root"},
    {"amis": "Tomangic", "chi": "哭泣 (動作)", "icon": "😿", "source": "User Fix", "morph": "T-om-angic"},
    {"amis": "Tawa", "chi": "笑 (詞根)", "icon": "😆", "source": "Standard", "morph": "Root"},
    {"amis": "Matawa", "chi": "笑 / 發笑", "icon": "🤣", "source": "Standard", "morph": "Ma-Tawa"},
    {"amis": "Roray", "chi": "累 / 困難 (詞根)", "icon": "😫", "source": "Row 465", "morph": "Root"},
    {"amis": "Maroray", "chi": "感到累 / 辛苦", "icon": "🥱", "source": "Row 465", "morph": "Ma-Roray"},
    {"amis": "Rihaday", "chi": "平安 / 安詳", "icon": "🕊️", "source": "User Fix", "morph": "State"}, # 修正
    {"amis": "Cirihaday", "chi": "平靜 / 安逸", "icon": "🙏", "source": "User Fix", "morph": "Cirihaday"}, # 新增
    {"amis": "Adada", "chi": "痛 (詞根 / 狀態)", "icon": "💔", "source": "Row 470", "morph": "Root"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Talacowacowa misa'icel ciira, marorayho.", "chi": "無論他如何努力，還是很辛苦(累)。", "icon": "😫", "source": "User Fix"},
    {"amis": "Malipahak kako anini a romi'ad.", "chi": "我今天很快樂。", "icon": "🥳", "source": "Standard Pattern"},
    {"amis": "Mararom ko faloco' no mako.", "chi": "我的心很難過。", "icon": "💔", "source": "Standard Pattern"},
    {"amis": "Maolah ci ina to wawa.", "chi": "媽媽愛孩子。", "icon": "🤱", "source": "Standard Pattern"},
    {"amis": "Matengil ko soni no tangic.", "chi": "聽見了哭聲。", "icon": "🔊", "source": "Row 238"},
    {"amis": "Matawa ci ama.", "chi": "爸爸在笑。", "icon": "😆", "source": "Standard Pattern"},
    {"amis": "Rihaday ko niyaro' no mita.", "chi": "我們的部落很平安。", "icon": "🕊️", "source": "Standard Pattern"},
    {"amis": "Adada ko faloco' ako.", "chi": "我的心很痛(心痛)。", "icon": "❤️‍🩹", "source": "Row 470 Context"},
    {"amis": "Misalimela to ko maomahay to kolong.", "chi": "農夫很珍惜牛。", "icon": "🐂", "source": "User Fix"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Talacowacowa misa'icel ciira, marorayho.",
        "audio": "Talacowacowa misa'icel ciira, marorayho",
        "options": ["無論他如何努力，還是很累", "無論他去哪裡，都很開心", "無論他做什麼，都不累"],
        "ans": "無論他如何努力，還是很累",
        "hint": "Talacowacowa (無論如何/去哪), Maroray (累)"
    },
    {
        "q": "單字測驗：Misalimela",
        "audio": "Misalimela",
        "options": ["愛惜/珍惜", "討厭", "丟棄"],
        "ans": "愛惜/珍惜",
        "hint": "User Fix: Misalimela"
    },
    {
        "q": "單字測驗：Cirihaday",
        "audio": "Cirihaday",
        "options": ["平靜/安逸", "打架", "睡覺"],
        "ans": "平靜/安逸",
        "hint": "User Fix: Palarihaday"
    },
    {
        "q": "Mararom ko faloco' no mako.",
        "audio": "Mararom ko faloco' no mako",
        "options": ["我的心很難過", "我的心很快樂", "我的心很痛"],
        "ans": "我的心很難過",
        "hint": "Mararom (難過) (Standard)"
    },
    {
        "q": "單字測驗：Malipahak",
        "audio": "Malipahak",
        "options": ["感到快樂", "感到生氣", "感到難過"],
        "ans": "感到快樂",
        "hint": "Ma- (感到) + Lipahak (快樂)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #AD1457;'>Unit 39: O Faloco'</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>心情與感受 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #AD1457;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #F8BBD0; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #880E4F;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會心情與感受的說法了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()


