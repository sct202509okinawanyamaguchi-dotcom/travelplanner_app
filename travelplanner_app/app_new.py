import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

st.set_page_config(page_title="たび Planner", layout="centered")

# --- フォントやデザインのカスタマイズ（CSS） ---
st.markdown("""
    <style>
    /* 背景色 */
    [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: #E6D8E2 !important;
    }

    /* メインタイトル */
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2E86C1;
        font-size: 35px !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 画像を中央に */
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    [data-testid="stImage"] > img {
        margin-left: auto !important;
        margin-right: auto !important;
    }

    /* ラベル（入力欄の上の文字など）を黒く太く */
    label p {
        color: black !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* タブの文字を黒く */
    button[data-baseweb="tab"] p {
        color: black !important;
        font-size: 18px !important;
    }

    /* 修正1改: 旅行タイトル入力ボックスを白背景・黒文字・黒カーソルに統一 */
    input[id="text_input_1"],
    input[aria-label="My Trip Plan is..."] {
        background-color: white !important;
        color: black !important;
        caret-color: black !important;
    }
    
    /* 旅行タイトル入力ボックスの親要素も白背景に */
    input[id="text_input_1"] ~ div,
    div[data-baseweb="input"]:has(input[id="text_input_1"]),
    div[data-baseweb="base-input"]:has(input[id="text_input_1"]) {
        background-color: white !important;
    }
    
    /* エキスパンダー内の入力欄は黒文字・黒カーソルに */
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] textarea {
        color: black !important;
        caret-color: black !important;
    }
    
    /* プレースホルダーも白に */
    input::placeholder {
        color: white !important;
        opacity: 1 !important;
    }
    textarea::placeholder {
        color: black !important;
        opacity: 1 !important;
    }

    /* 修正2: エキスパンダー（新しい予定を追加）のボタン部分を黒背景に */
    div[data-testid="stExpander"] details summary {
        background-color: black !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* 修正2: エキスパンダーボタンの文字を白に */
    div[data-testid="stExpander"] details summary p {
        color: white !important;
    }

    /* 修正3: エキスパンダー内の入力ボックスを白ベタ黒ふちに */
    div[data-testid="stExpander"] div[data-baseweb="input"],
    div[data-testid="stExpander"] div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }

    /* 修正3: エキスパンダー内の入力フィールドとテキストを黒に */
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] textarea,
    div[data-testid="stExpander"] div[data-baseweb="select"] div {
        color: black !important;
        background-color: white !important;
    }

    /* 修正3: エキスパンダー内のテキストエリアを白ベタ黒ふちに */
    div[data-testid="stExpander"] textarea {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }

    /* その他の一般的な入力ボックス（旅行期間など） */
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }

    /* 日付入力ボックス内の文字を黒に */
    div[data-baseweb="input"] input {
        color: black !important;
    }

    /* セレクトボックス内の文字を黒に */
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div {
        color: black !important;
    }

    /* 修正4: スケジュールボックス内の文字を黒に */
    .st-emotion-cache-yfw52f p,
    .st-emotion-cache-yfw52f h3,
    .st-emotion-cache-1fq9onn p,
    .st-emotion-cache-yfw52f strong {
        color: black !important;
    }
    
    /* 修正4: 予定が表示される各スケジュールボックス（container）を白ベタ黒ふちに */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }

    /* 修正5: ダイアログ内のラベル文字（予定の名前、場所、時間、メモ）を白に */
    .st-emotion-cache-10yj5h9 p {
        color: white !important;
    }
    
    div[class*="st-emotion-cache-1n6tfoc"] label p {
        color: white !important;
    }
    
    /* 修正5: ダイアログ内のセレクトボックスの時間表示（00:00など）を白に */
    div[class*="st-emotion-cache-1n6tfoc"] div[value] {
        color: white !important;
    }
    
    div[class*="st-emotion-cache-1n6tfoc"] .st-e5 {
        color: white !important;
    }
    
    /* 修正5: ダイアログ内の入力ボックスを白背景・黒枠に */
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="input"],
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"],
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="textarea"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    
    /* 修正5: セレクトボックスの内側も白背景に */
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    
    /* 修正5: ダイアログ内の入力フィールドの文字とカーソルを黒に - より強力なセレクタ */
    div[class*="st-emotion-cache-1n6tfoc"] input,
    div[class*="st-emotion-cache-1n6tfoc"] textarea,
    .st-emotion-cache-10yj5h9 ~ div input,
    .st-emotion-cache-10yj5h9 ~ div textarea {
        color: black !important;
        caret-color: black !important;
        background-color: white !important;
    }
    
    /* 修正5: ダイアログ内のセレクトボックスの表示テキストを黒に */
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"] div,
    div[class*="st-emotion-cache-1n6tfoc"] div[value] {
        color: black !important;
    }
    
    /* カーソルを全ての入力欄で表示（デフォルトは黒） */
    input, textarea {
        caret-color: black !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# --- データの保存場所 ---
if "plans" not in st.session_state:
    st.session_state.plans = []

# --- 編集用ポップアップ（ダイアログ） ---
@st.dialog("予定を編集")
def edit_plan_dialog(plan_index):
    plan = st.session_state.plans[plan_index]
    
    new_title = st.text_input("予定の名前", value=plan["title"])
    new_place = st.text_input("場所", value=plan["place"])
    new_time = st.selectbox("時間", [f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)], 
                            index=([f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)]).index(plan["time"]))
    new_memo = st.text_area("メモ・住所", value=plan["memo"])
    
    if st.button("更新を保存"):
        st.session_state.plans[plan_index].update({
            "title": new_title,
            "place": new_place,
            "time": new_time,
            "memo": new_memo
        })
        st.rerun()

# --- メイン画面 ---

# --- アプリの最上部に画像を入れる ---
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    try:
        st.image("my_header.png", width=300) 
    except:
        st.markdown('<h1 style="text-align: center;">TRAVEL LOG</h1>', unsafe_allow_html=True)

# 1. 旅行タイトルの復活と装飾
travel_title = st.text_input("My Trip Plan is...", "ここに旅行のタイトルを入れる")
st.markdown(f'<p class="main-title">📅 {travel_title}</p>', unsafe_allow_html=True)

# 2. 旅行期間の設定
dates = st.date_input("旅行期間", value=(datetime.now(), datetime.now() + timedelta(days=2)), format="YYYY/MM/DD")

# 3. 新規予定追加エリア
with st.expander("➕ 新しい予定を追加する", expanded=False):
    with st.form("add_form", clear_on_submit=True):
        plan_title = st.text_input("予定の名前（例：友達とディナー）")
        
        col1, col2 = st.columns(2)
        with col1:
            plan_date = st.date_input("日付", value=dates[0] if isinstance(dates, tuple) and len(dates) > 0 else datetime.now())
        with col2:
            plan_time = st.selectbox("開始時間", [f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)])
        
        plan_place = st.text_input("場所（例：東京タワー、レストラン名）")
        
        if plan_place:
            encoded_place = urllib.parse.quote(plan_place)
            map_search_url = f"https://www.google.com/maps/search/{encoded_place}"
            st.markdown(f'🔗 [Googleマップで「{plan_place}」を詳しく探す]({map_search_url})')
            
        plan_memo = st.text_area("メモ・詳細")
        
        if st.form_submit_button("予定を確定"):
            if plan_title:
                st.session_state.plans.append({
                    "id": datetime.now().timestamp(),
                    "date": plan_date,
                    "time": plan_time,
                    "title": plan_title,
                    "place": plan_place,
                    "memo": plan_memo
                })
                st.rerun()

# 4. 予定の表示
if isinstance(dates, tuple) and len(dates) == 2:
    start_date, end_date = dates
    diff = (end_date - start_date).days + 1
    tabs = st.tabs([f"{i+1}日目 ({(start_date + timedelta(days=i)).strftime('%m/%d')})" for i in range(diff)])
    
    for i, tab in enumerate(tabs):
        current_date = start_date + timedelta(days=i)
        with tab:
            day_plans = [(idx, p) for idx, p in enumerate(st.session_state.plans) if p["date"] == current_date]
            day_plans.sort(key=lambda x: x[1]["time"])
            
            for original_idx, p in day_plans:
                with st.container(border=True):
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"### 🕒 {p['time']}")
                        st.markdown(f"**【{p['title']}】**")
                        if p['place']: st.write(f"📍 場所: {p['place']}")
                        if p['memo']: st.caption(f"📝 {p['memo']}")
                    with c2:
                        if st.button("📝 編集", key=f"edit_btn_{p['id']}"):
                            edit_plan_dialog(original_idx)
                        if st.button("🗑️ 削除", key=f"del_btn_{p['id']}"):
                            st.session_state.plans.pop(original_idx)
                            st.rerun()
                    
                    # 地図表示（場所が入力されている場合のみ）
                    if p['place']:
                        encoded_place = urllib.parse.quote(p['place'])
                        map_html = f"""
                            <iframe width="100%" height="200" frameborder="0" style="border:0; border-radius:10px;"
                            src="https://maps.google.com/maps?q={encoded_place}&output=embed" allowfullscreen></iframe>
                        """
                        st.components.v1.html(map_html, height=210)