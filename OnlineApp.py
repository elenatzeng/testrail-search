import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# 🚀 埋下頂端錨點 (供橘色按鈕跳轉)
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 2. 側邊欄
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

# 3. 搜尋邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div>📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            q_input = st.text_input("● 搜尋內容 (輸入關鍵字查詢：支援繁體簡體與英文):", value=st.session_state.q_text, placeholder="充值 CNY")
            st.session_state.q_text = q_input

        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()

        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_input_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []
            
            for c in all_cases:
                cid = str(c.get('id', '')).strip()
                title = str(c.get('title', '')).lower()
                section_path = str(path_map.get(c.get('section_id', ""), "")).lower()
                raw_data = clean_html(str(c.get('custom_steps','')) + str(c.get('custom_steps_separated','')))
                search_text = str(raw_data).lower()
                searchable_pool = title + section_path + search_text
                
                is_all_match = True
                total_score = 0
                for term in raw_input_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    if not (any(word in searchable_pool for word in expanded) or any(word == cid for word in expanded)):
                        is_all_match = False; break
                    else:
                        if any(word in title for word in expanded): total_score += 1000
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    if not search_text.strip(): total_score -= 500000 
                    scored_results.append((total_score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例 (已過濾交集結果)")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                author_style = f"color: {'#4CAF50' if u_info.get('is_active') else '#ff4b4b'}; background: rgba(0,0,0,0.2); border: 1.5px solid;"
                
                # 路徑顯示
                st.markdown(f'<div style="font-size:13px; color:#8b949e; margin-bottom:10px;">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                
                # 標題欄
                c_title, c_btn = st.columns([7.5, 1.5], vertical_alignment="center")
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} (#{cid}) <span class="author-tag" style="{author_style}">{"🟢" if u_info.get("is_active") else "🔴"} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 步驟展示 (完美還原截圖格式)
                with st.expander("🔽 查看測試步驟"):
                    steps_data = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    if isinstance(steps_data, list):
                        for i, step in enumerate(steps_data, 1):
                            st.markdown(f"""
                                <div style="border-left: 3px solid #4CAF50; padding-left: 20px; margin-bottom: 25px;">
                                    <div style="font-weight:bold; font-size:14px; margin-bottom:8px;">Step {i}:</div>
                                    <div style="background:#1c2128; padding:15px; border-radius:10px; border:1px solid #30363d; color:#c9d1d9;">{step.get('content','')}</div>
                                    <div style="font-weight:bold; font-size:14px; margin: 15px 0 8px 0;">Expected:</div>
                                    <div style="background:#1c2128; padding:15px; border-radius:10px; border:1px solid #30363d; color:#c9d1d9;">{step.get('expected','')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="background:#1c2128; padding:20px; border-radius:10px; border:1px solid #30363d;">{steps_data if steps_data else "（無詳細步驟）"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # 🚀 活力橘回到頂端按鈕
    st.markdown("""
        <a href="#top-anchor" style="position:fixed; bottom:30px; right:30px; width:50px; height:50px; 
           background:#f77f00; color:white; border-radius:50%; display:flex; align-items:center; 
           justify-content:center; text-decoration:none; font-size:22px; z-index:9999; 
           box-shadow:0 4px 12px rgba(0,0,0,0.4); transition:0.3s;">▲</a>
    """, unsafe_allow_html=True)

else:
    st.info("👈 請在左側輸入連線資訊開始查詢。")
