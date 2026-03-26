import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# --- ✨ 終極大絕：手動按鈕邏輯 ---
if "sidebar_state" not in st.session_state:
    st.session_state.sidebar_state = "expanded"

# 在左上角放一個顯眼的按鈕
col_btn, _ = st.columns([1, 10])
with col_btn:
    btn_label = "⬅️ 收合設定" if st.session_state.sidebar_state == "expanded" else "➡️ 連線設定"
    if st.button(btn_label):
        st.session_state.sidebar_state = "collapsed" if st.session_state.sidebar_state == "expanded" else "expanded"
        st.rerun()

# 根據狀態強制控制側邊欄 (這行要在 sidebar 定義前)
st.markdown(f'<style>div[data-testid="stSidebar"] {{ display: {"block" if st.session_state.sidebar_state == "expanded" else "none"} !important; }}</style>', unsafe_allow_html=True)

# 2. 側邊欄內容
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("帳號 Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password", value=st.query_params.get("pw", ""))
    pid = st.number_input("Project ID", value=int(st.query_params.get("pid", 10)))
    sid = st.number_input("Suite ID", value=int(st.query_params.get("sid", 10)))
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")

st.title("🧪 TestRail 智能檢索中心")

# --- 後續搜尋邏輯保持不變 (直接用妳原本的迴圈代碼即可) ---
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        # ... (這裡接妳原本的搜尋結果顯示代碼) ...
        # 注意：記得保留妳改好的 15px 標題和 13px 內文喔！
        pass
