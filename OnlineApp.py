import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr
from users import USER_CONFIG, DEFAULT_CONFIG

# 1. 配置 (標記 1)
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 2. 側邊欄 (標記 2, 3)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "10")))

    if st.button("💾 儲存資訊至網址", use_container_width=True): # 標記 2
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")

    if st.button("🔄 強制刷新數據", use_container_width=True): # 標記 3
        st.cache_data.clear()
        st.rerun()

# 3. 主畫面 (標記 4-12)
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        # 標記 4: 專案資訊
        st.markdown(f'<div style="color:#8b949e; font-size:14px;">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        # 標記 5, 11, 12: 搜尋與按鈕併排
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容 (輸入關鍵字查詢：支援繁體簡體與英文):</div>', unsafe_allow_html=True)
            query = st.text_input("", placeholder="多關鍵字請以空格分隔 (交集搜尋)", key="search_box", label_visibility="collapsed")
            st.session_state.q_text = query

        with col_clear:
            st.markdown('<p style="margin-bottom: 23px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除條件", use_container_width=True): # 標記 11
                st.session_state["search_box"] = ""
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 23px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 重新查詢", use_container_width=True): # 標記 12
                st.rerun()

        # 結果渲染
        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []

            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '').lower()
                section_path = str(path_map.get(c.get('section_id'), "")).lower()
                steps_raw = str(c.get('custom_steps_separated', '')) + str(c.get('custom_steps', ''))
                searchable_text = (title + section_path + steps_raw).lower()
                
                if all(term in searchable_text or term in cid for term in raw_terms):
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    score = 1000 if any(t in title for t in raw_terms) else 0
                    score += u_info.get("weight", 0)
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例 (已過濾交集結果)")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji = "🟢" if u_info.get("is_active") else "🔴"
                author_style = "color: #4CAF50; background: rgba(76,175,80,0.15); border: 1.5px solid #4CAF50;" if u_info.get("is_active") else "color: #ff4b4b; background: rgba(255,75,75,0.15); border: 1.5px solid #ff4b4b;"
                
                # 標記 6: 淺灰路徑
                curr_path = path_map.get(item.get('section_id'), "None")
                st.markdown(f'<div class="case-path-text">{curr_path}</div>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    # 標記 7, 8: 標題與作者
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    # 標記 10: Open Case 按鈕
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 標記 9: 步驟展開
                with st.expander("🔽 查看測試步驟"):
                    raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or []
                    if isinstance(raw_steps, list) and len(raw_steps) > 0:
                        for i, s in enumerate(raw_steps, 1):
                            st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html(s.get("content", ""))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{clean_html(item.get("custom_steps", ""))}</div>', unsafe_allow_html=True)
                st.markdown("---")
else:
    st.info("👈 請在左側輸入資料後開始查詢。")
