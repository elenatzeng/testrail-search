import streamlit as st
from keywords import SEARCH_DICTIONARY
from users import USER_CONFIG, DEFAULT_CONFIG
from style import apply_custom_style, show_sleeping_mode
from utils import clean_html_and_add_numbers, multi_lang_search, fetch_data_from_tr

# 1. 初始化頁面
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# 2. 清除搜尋邏輯
def clear_search_action():
    if "search_box" in st.session_state:
        st.session_state["search_box"] = ""
    st.session_state.query_text = ""

# 3. 側邊欄記憶與連線設定
def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"), key="input_url")
    tr_user = st.text_input("帳號 Email", value=get_val("user"), key="input_user")
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"), key="input_pw")
    project_id = st.number_input("Project ID", value=int(get_val("pid", "1")), key="input_pid")
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "1")), key="input_sid")
    
    st.session_state.update({"store_url": tr_url, "store_user": tr_user, "store_pw": tr_pw, "store_pid": project_id, "store_sid": suite_id})

    if st.button("💾 儲存資訊至網址"):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")

# 4. 主畫面檢索邏輯
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id, USER_CONFIG)
    
    if all_cases:
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b>{p_name} | 最後同步：{sync_time}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "query_text" not in st.session_state: st.session_state.query_text = ""

        with col_search:
            query = st.text_input("🔍 搜尋內容:", placeholder="多關鍵字請以空格分隔", key="search_box")
            st.session_state.query_text = query

        with col_clear:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除", use_container_width=True, on_click=clear_search_action):
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 查詢", use_container_width=True):
                st.rerun()

        # 搜尋渲染邏輯
        final_query = st.session_state.query_text
        if final_query:
            raw_input_terms = final_query.strip().split()
            scored_results = []
            for c in all_cases:
                cid, title = str(c.get('id', '')), c.get('title', '').lower()
                section_path = path_map.get(c.get('section_id'), "").lower()
                full_text = str(c).lower()
                
                is_all_match, combined_score = True, 0
                for term in raw_input_terms:
                    expanded_terms = multi_lang_search(term, SEARCH_DICTIONARY)
                    match_this_term = False
                    if term.strip('#') == cid:
                        combined_score += 100000
                        match_this_term = True
                    elif any(et in section_path for et in expanded_terms):
                        combined_score += 50000
                        match_this_term = True
                    elif any(et in title for et in expanded_terms):
                        combined_score += 10000
                        match_this_term = True
                    elif any(et in full_text for et in expanded_terms):
                        combined_score += 1000
                        match_this_term = True
                    if not match_this_term:
                        is_all_match = False
                        break
                
                if is_all_match:
                    author_id = c.get('created_by')
                    u_info = USER_CONFIG.get(author_id, DEFAULT_CONFIG)
                    raw_steps = c.get('custom_steps_separated') or c.get('custom_steps') or c.get('steps') or []
                    score = combined_score + (len(raw_steps) * 500) + u_info.get("weight", 0)
                    if not u_info.get("is_active", True): score -= 45000
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji, author_style = ("🟢", "color: #4CAF50; background: rgba(76,175,80,0.15); border: 1.5px solid #4CAF50;") if u_info.get("is_active", True) else ("🔴", "color: #ff4b4b; background: rgba(255,75,75,0.15); border: 1.5px solid #ff4b4b;")
                
                with st.container():
                    st.markdown(f'<span style="font-size:12px; color:#8b949e;">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small style="color:#8b949e">(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                    with st.expander("🔽 查看步驟"):
                        raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or item.get('steps')
                        if isinstance(raw_steps, list) and len(raw_steps) > 0:
                            for i, s in enumerate(raw_steps, 1):
                                st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html_and_add_numbers(s.get("content", s.get("step", "")))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html_and_add_numbers(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    st.markdown("---")
else:
    st.warning("👈 請在側邊欄輸入連線資訊。")
