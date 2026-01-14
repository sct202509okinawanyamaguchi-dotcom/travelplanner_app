import streamlit as st
from datetime import datetime, timedelta
import urllib.parse
import os
from supabase import create_client, Client

# 環境変数を読み込み
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    st.error("環境変数が設定されていません。Streamlit CloudのSecretsで設定してください。")
    st.stop()

st.set_page_config(page_title="たび Planner", layout="centered")

# CSS
st.markdown("""
    <style>
    [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background-color: #E6D8E2 !important;
    }
    .main-title {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #2E86C1;
        font-size: 35px !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    [data-testid="stImage"] {
        display: flex !important;
        justify-content: center !important;
    }
    [data-testid="stImage"] > img {
        margin-left: auto !important;
        margin-right: auto !important;
    }
    label p {
        color: black !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    button[data-baseweb="tab"] p {
        color: black !important;
        font-size: 18px !important;
    }
    input[id="text_input_1"],
    input[aria-label="My Trip Plan is..."] {
        background-color: white !important;
        color: black !important;
        caret-color: black !important;
    }
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] textarea {
        color: black !important;
        caret-color: black !important;
    }
    input::placeholder {
        color: white !important;
        opacity: 1 !important;
    }
    textarea::placeholder {
        color: black !important;
        opacity: 1 !important;
    }
    div[data-testid="stExpander"] details summary {
        background-color: black !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    div[data-testid="stExpander"] details summary p {
        color: white !important;
    }
    div[data-testid="stExpander"] div[data-baseweb="input"],
    div[data-testid="stExpander"] div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] input,
    div[data-testid="stExpander"] textarea,
    div[data-testid="stExpander"] div[data-baseweb="select"] div {
        color: black !important;
        background-color: white !important;
    }
    div[data-testid="stExpander"] textarea {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="input"] input {
        color: black !important;
    }
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] div {
        color: black !important;
    }
    textarea {
        color: black !important;
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    .st-emotion-cache-yfw52f p,
    .st-emotion-cache-yfw52f h3,
    .st-emotion-cache-1fq9onn p,
    .st-emotion-cache-yfw52f strong {
        color: black !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] span,
    div[data-testid="stVerticalBlockBorderWrapper"] div {
        color: black !important;
    }
    .st-emotion-cache-10yj5h9 p {
        color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] label p {
        color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] div[value] {
        color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] .st-e5 {
        color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="input"],
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"],
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="textarea"] {
        background-color: white !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] input,
    div[class*="st-emotion-cache-1n6tfoc"] textarea {
        color: black !important;
        caret-color: black !important;
        background-color: white !important;
    }
    div[class*="st-emotion-cache-1n6tfoc"] div[data-baseweb="select"] div {
        color: black !important;
    }
    input, textarea {
        caret-color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 認証機能
def login_signup():
    st.title("🌍 Travel Planner")
    
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("メールアドレス")
            password = st.text_input("パスワード", type="password")
            
            if st.form_submit_button("ログイン"):
                try:
                    response = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })
                    st.session_state.user = response.user
                    st.success("ログインしました!")
                    st.rerun()
                except Exception as e:
                    st.error(f"ログインエラー: {str(e)}")
    
    with tab2:
        with st.form("signup_form"):
            email = st.text_input("メールアドレス", key="signup_email")
            password = st.text_input("パスワード", type="password", key="signup_password")
            password_confirm = st.text_input("パスワード(確認)", type="password")
            
            if st.form_submit_button("登録"):
                if password != password_confirm:
                    st.error("パスワードが一致しません")
                elif len(password) < 6:
                    st.error("パスワードは6文字以上にしてください")
                else:
                    try:
                        response = supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })
                        st.success("登録完了!メールを確認してください")
                    except Exception as e:
                        st.error(f"登録エラー: {str(e)}")

# データベース操作関数
def save_plan_to_db(user_id, plan_data):
    try:
        supabase.table('plans').insert({
            'user_id': user_id,
            'date': str(plan_data['date']),
            'time': plan_data['time'],
            'title': plan_data['title'],
            'place': plan_data['place'],
            'memo': plan_data['memo']
        }).execute()
    except Exception as e:
        st.error(f"保存エラー: {str(e)}")

def get_plans_from_db(user_id, start_date, end_date):
    try:
        response = supabase.table('plans').select('*').eq('user_id', user_id).gte('date', str(start_date)).lte('date', str(end_date)).execute()
        return response.data
    except Exception as e:
        st.error(f"取得エラー: {str(e)}")
        return []

def update_plan_in_db(plan_id, plan_data):
    try:
        supabase.table('plans').update({
            'time': plan_data['time'],
            'title': plan_data['title'],
            'place': plan_data['place'],
            'memo': plan_data['memo']
        }).eq('id', plan_id).execute()
    except Exception as e:
        st.error(f"更新エラー: {str(e)}")

def delete_plan_from_db(plan_id):
    try:
        supabase.table('plans').delete().eq('id', plan_id).execute()
    except Exception as e:
        st.error(f"削除エラー: {str(e)}")

# 編集用ポップアップ
@st.dialog("予定を編集")
def edit_plan_dialog(plan):
    new_title = st.text_input("予定の名前", value=plan["title"])
    new_place = st.text_input("場所", value=plan["place"] or "")
    new_time = st.selectbox("時間", [f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)], 
                            index=([f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)]).index(plan["time"]))
    new_memo = st.text_area("メモ・住所", value=plan["memo"] or "")
    
    if st.button("更新を保存"):
        update_plan_in_db(plan['id'], {
            "title": new_title,
            "place": new_place,
            "time": new_time,
            "memo": new_memo
        })
        st.rerun()

# メイン画面
if "user" not in st.session_state:
    login_signup()
else:
    user = st.session_state.user
    
    # ログアウトボタン
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("ログアウト"):
            supabase.auth.sign_out()
            st.session_state.clear()
            st.rerun()
    
    # 画像表示
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        try:
            st.image("my_header.png", width=300)
        except:
            st.markdown('<h1 style="text-align: center;">TRAVEL LOG</h1>', unsafe_allow_html=True)
    
    # 旅行タイトル
    travel_title = st.text_input("My Trip Plan is...", "ここに旅行のタイトルを入れる")
    st.markdown(f'<p class="main-title">📅 {travel_title}</p>', unsafe_allow_html=True)
    
    # 旅行期間
    dates = st.date_input("旅行期間", value=(datetime.now(), datetime.now() + timedelta(days=2)), format="YYYY/MM/DD")
    
    # 新規予定追加
    with st.expander("➕ 新しい予定を追加する", expanded=False):
        with st.form("add_form", clear_on_submit=True):
            plan_title = st.text_input("予定の名前（例：友達とディナー）")
            
            col1, col2 = st.columns(2)
            with col1:
                plan_date = st.date_input("日付", value=dates[0] if isinstance(dates, tuple) and len(dates) > 0 else datetime.now())
            with col2:
                plan_time = st.selectbox("開始時間", [f"{h:02d}:00" for h in range(24)] + [f"{h:02d}:30" for h in range(24)])
            
            plan_place = st.text_input("場所（例:東京タワー、レストラン名）")
            
            if plan_place:
                encoded_place = urllib.parse.quote(plan_place)
                map_search_url = f"https://www.google.com/maps/search/{encoded_place}"
                st.markdown(f'🔗 [Googleマップで「{plan_place}」を詳しく探す]({map_search_url})')
                
            plan_memo = st.text_area("メモ・詳細")
            
            if st.form_submit_button("予定を確定"):
                if plan_title:
                    save_plan_to_db(user.id, {
                        "date": plan_date,
                        "time": plan_time,
                        "title": plan_title,
                        "place": plan_place,
                        "memo": plan_memo
                    })
                    st.success("予定を保存しました!")
                    st.rerun()
    
    # 予定の表示
    if isinstance(dates, tuple) and len(dates) == 2:
        start_date, end_date = dates
        diff = (end_date - start_date).days + 1
        tabs = st.tabs([f"{i+1}日目 ({(start_date + timedelta(days=i)).strftime('%m/%d')})" for i in range(diff)])
        
        all_plans = get_plans_from_db(user.id, start_date, end_date)
        
        for i, tab in enumerate(tabs):
            current_date = start_date + timedelta(days=i)
            with tab:
                day_plans = [p for p in all_plans if p["date"] == str(current_date)]
                day_plans.sort(key=lambda x: x["time"])
                
                for p in day_plans:
                    with st.container(border=True):
                        c1, c2 = st.columns([3, 1])
                        with c1:
                            st.markdown(f"### 🕒 {p['time']}")
                            st.markdown(f"**【{p['title']}】**")
                            if p['place']: st.write(f"📍 場所: {p['place']}")
                            if p['memo']: st.caption(f"📝 {p['memo']}")
                        with c2:
                            if st.button("📝 編集", key=f"edit_btn_{p['id']}"):
                                edit_plan_dialog(p)
                            if st.button("🗑️ 削除", key=f"del_btn_{p['id']}"):
                                delete_plan_from_db(p['id'])
                                st.rerun()
                        
                        if p['place']:
                            encoded_place = urllib.parse.quote(p['place'])
                            map_html = f"""
                                <iframe width="100%" height="200" frameborder="0" style="border:0; border-radius:10px;"
                                src="https://maps.google.com/maps?q={encoded_place}&output=embed" allowfullscreen></iframe>
                            """
                            st.components.v1.html(map_html, height=210)
