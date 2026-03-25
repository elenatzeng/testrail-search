import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 基礎配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid") or 10))
    sid = st.number_input("Suite ID", value=int(get_val("sid") or 10))
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅")
    if st.button("🔄 強制刷新", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f'<div style="color:#8b949e; font-size:13px;">📍 {p_name} | #{sid}</div>', unsafe_allow_html=True)
        q_input = st.text_input("● 搜尋內容:", value=st.session_state.get("q_text", ""), placeholder="輸入關鍵字...")
        st.session_state.q_text = q_input

        final_query = st.session_state.q_text
        if final_query:
            terms = [t.lower() for t in final_query.strip().split() if t]
            results = []
            for case in all_cases:
                cid = str(case.get('id'))
                title = str(case.get('title', '')).lower()
                path = str(path_map.get(case.get('section_id'), '')).lower()
                steps_data = clean_html(str(case.get('custom_steps','')) + str(case.get('custom_steps_separated','')))
                steps_str = str(steps_data).lower()
                
                is_match = True
                score = 0
                for t in terms:
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title + path + steps_str) for w in expanded) or any(w == cid for word in expanded)):
                        is_match = False; break
                    if any(w in title for w in expanded): score += 5000
                
                if is_match:
                    u_info = USER_CONFIG.get(int(case.get('created_by', 0)), DEFAULT_CONFIG)
                    score += u_info.get("weight", 0)
                    if len(steps_str.strip()) < 10 or "(無詳細步驟)" in steps_str: score -= 2000000
                    results.append((score
