import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("Suite ID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("🔄 強制刷新數據"):
        st.cache_data.clear(); st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        st.title("🧪 TestRail 智能檢索中心")
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span>", unsafe_allow_html=True)
        
        q_text = st.text_input("● 搜尋內容:", key="q_text_input")
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []
            for c in all_cases:
                f_path = path_map.get(c.get('section_id'), "GoGaming")
                title = str(c.get('title', '')).lower()
                is_match = all(any(w in (title + f_path.lower()) for w in multi_lang_search(t, SEARCH_DICTIONARY)) for t in terms)
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((c, u))

            st.markdown(f"### 🎯 找到 {len(results)} 個案例")
            for item, u in results:
                is_active = u.get("is_active", False)
                # 🚀 根據 True/False 決定主色調
                main_color = "#32CD32" if is_active else "#FF4B4B"
                status_emoji = "🟢" if is_active else "🔴"
                
                st.markdown(f'<div style="font-size:14px; color:#adb5bd; margin-top:25px;"><span style="margin-right:8px;">📁</span> {path_map.get(item.get("section_id"), "GoGaming")}</div>', unsafe_allow_html=True)
                
                # 🚀 這裡！內聯樣式直接鎖死顏色！
                tag_html = f'''
                <span class="author-tag" style="border-color:{main_color} !important; color:{main_color} !important; box-shadow: 0 0 10px {main_color}88 !important;">
                    {status_emoji} {u["name"]}
                </span>
                '''
                st.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")}</span>{tag_html}</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
