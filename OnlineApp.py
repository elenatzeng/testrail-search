import streamlit as st
from keywords import SEARCH_DICTIONARY
from users import USER_CONFIG, DEFAULT_CONFIG
from style import apply_custom_style
from utils import clean_html, multi_lang_search, fetch_data_from_tr

# 1. 設置與樣式
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 4. 側邊欄 (標記 1, 2)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "10")))

    if st.button("💾 儲存資訊至網址"): # 標記 1
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")

    if st.button("🔄 強制更新數據"): # 標記 2
        st.cache_data.clear()
        st.rerun()

# 5. 主畫面 (標記 3, 4, 5, 6, 7)
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases:
        st.markdown(f'<div class="location-tag">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        # 標記 3: 搜尋框
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        query = st.text_input("🔍 搜尋內容 (輸入關鍵字查詢：支援繁體簡體與英文 ):", key="search_box", placeholder="多關鍵字請以空格分隔 (交集搜尋)")
        st.session_state.q_text = query

        if st.session_state.q_text:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_terms = st.session_state.q_text.strip().split()
            scored_results = []

            for c in all_cases:
                cid, title, full_text = str(c.get('id', '')), c.get('title', '').lower(), str(c).lower()
                section_path = path_map.get(c.get('section_id'), "").lower()
                is_all_match, score = True, 0
                for term in raw_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    match = False
                    if term.strip('#') == cid: score += 100000; match = True
                    elif any(et in section_path for et in expanded): score += 50000; match = True
                    elif any(et in title for et in expanded): score += 10000; match = True
                    elif any(et in full_text for et in expanded): score += 1000; match = True
                    if not match: is_all_match = False; break
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    steps = c.get('custom_steps_separated') or c.get('custom_steps') or []
                    score += (len(steps) * 500) + u_info.get("weight", 0)
                    if not u_info.get("is_active"): score -= 45000
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.write(f"### 🎯 找到 {len(scored_results)} 個案例 (已過濾交集結果)")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji, author_style = ("🟢", "color: #4CAF50; background: rgba(76,175,80,0.15); border: 1.5px solid #4CAF50;") if u_info.get("is_active") else ("🔴", "color: #ff4b4b; background: rgba(255,75,75,0.15); border: 1.5px solid #ff4b4b;")
                
                # 標記 4: 路徑
                st.markdown(f'<span style="font-size:12px; color:#8b949e;">{path_map.get(item.get("section_id"))}</span>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    # 標記 6: 標題與作者
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    # 標記 7: Open Case
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 標記 5: 測試步驟
                with st.expander("🔽 查看測試步驟"):
                    raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or []
                    if isinstance(raw_steps, list) and len(raw_steps) > 0:
                        for i, s in enumerate(raw_steps, 1):
                            st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html(s.get("content", ""))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                    else: st.info("無步驟資料。")
                st.markdown("---")
else:
    st.warning("👈 請在側邊欄輸入連線資訊。")
