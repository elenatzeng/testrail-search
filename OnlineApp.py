import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 初始化配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# 🚀 埋下頂部錨點 (隱藏在最上方)
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "10")))

    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")

    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div style="color:#8b949e; font-size:14px;">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        # 搜尋區域 (修復清除按鈕報錯邏輯)
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "q_text" not in st.session_state: 
            st.session_state.q_text = ""

        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容 (輸入關鍵字查詢：支援繁體簡體與英文):</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="多關鍵字請以空格分隔 (交集搜尋)", label_visibility="collapsed")
            st.session_state.q_text = q_input

        with col_clear:
            st.markdown('<p style="margin-bottom: 23px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 23px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 重新查詢", use_container_width=True):
                st.rerun()

        # 核心搜尋與排序邏輯
        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_input_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []

            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '').lower()
                section_path = str(path_map.get(c.get('section_id', ""), "")).lower()
                
                steps_sep = c.get('custom_steps_separated') or []
                steps_txt = str(c.get('custom_steps', '')).strip()
                has_content = len(steps_sep) > 0 or len(steps_txt) > 0
                
                searchable_pool = (title + section_path + steps_txt + str(steps_sep)).lower()
                
                is_all_match = True
                total_score = 0
                
                for term in raw_input_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    if not any(word in searchable_pool or word in cid for word in expanded):
                        is_all_match = False
                        break
                    else:
                        if any(word in title for word in expanded): total_score += 1000
                        if any(word in section_path for word in expanded): total_score += 500
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    if not has_content: total_score -= 100000 
                    scored_results.append((total_score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例 (已過濾交集結果)")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji = "🟢" if u_info.get("is_active") else "🔴"
                author_style = "color: #4CAF50; background: rgba(76,175,80,0.15); border: 1.5px solid #4CAF50;" if u_info.get("is_active") else "color: #ff4b4b; background: rgba(255,75,75,0.15); border: 1.5px solid #ff4b4b;"
                
                curr_path = path_map.get(item.get('section_id'), "None")
                st.markdown(f'<div class="case-path-text">{curr_path}</div>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("🔽 查看測試步驟"):
                    raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or []
                    if isinstance(raw_steps, list) and len(raw_steps) > 0:
                        for i, s in enumerate(raw_steps, 1):
                            c_body = clean_html(s.get("content", ""))
                            e_body = clean_html(s.get("expected", ""))
                            st.markdown(f'''
                                <div class="step-item">
                                    <span style="color:#79c0ff; font-weight:800;">Step {i}:</span>
                                    <div class="step-content-box">{c_body if c_body else "（無操作內容）"}</div>
                                    <div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div>
                                    <div class="step-content-box" style="border-left: 2px solid #4CAF50;">{e_body if e_body else "（無預期結果）"}</div>
                                </div>''', unsafe_allow_html=True)
                    else:
                        body = clean_html(item.get('custom_steps', ''))
                        st.markdown(f'<div class="step-content-box">{(body if body else "（無詳細步驟）")}</div>', unsafe_allow_html=True)
                st.markdown("---")

# 🚀 顯示懸浮「回到頂部」按鈕 (HTML 連結到頂部錨點)
st.markdown("""
    <a href="#top-anchor" class="scroll-to-top" title="回到頂部">
        ▲
    </a>
""", unsafe_allow_html=True)

else:
    st.info("👈 請在左側輸入資料後開始查詢。")
