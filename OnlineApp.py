import streamlit as st
import re
import os
import sys

# 🛡️ 1. 路徑保險
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🛡️ 2. 安全導入
try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"⚠️ 核心導入失敗: {e}")
    st.stop()

# 🛡️ 3. 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

# ✨ 錨點
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊並記住", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 4. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="搜尋關鍵字...", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        # --- 🏆 核心排序矩陣 (完全還原昨天版本) ---
        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f
