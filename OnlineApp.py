import streamlit as st
import re
from keywords import SEARCH_DICTIONARY
from users import USER_CONFIG, DEFAULT_CONFIG
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr

# 1. 基礎配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

def clear_search_action():
    st.session_state["search_box"] = ""
    st.session_state.q_text = ""

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("🔗 TestRail URL", value=get_val("url"))
    tr_user = st.text_input("📧 帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("🔑 API Key", type="password", value=get_val("pw"))
    
    try:
        def_pid = int(get_val("pid", "10"))
        def_sid = int(get_val("sid", "10"))
    except:
        def_pid, def_sid = 10, 10
        
    project_id = st.number_input("🆔 Project ID", value=def_pid)
    suite_id = st.number_input("🆔 Suite ID", value=def_sid)

    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存至網址")

    if st.button("🔄 強制更新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 3. 主畫面
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    with st.spinner("🚀 正在從 TestRail 搬運案例中..."):
        all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div class="location-tag">🏢 <b>Project：</b>{p_name} | 📋 <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            # 🚀 標題改為精確模式提示
            query = st.text_input(
                "🔍 關鍵字精確搜尋 (多詞空格交集):", 
                placeholder="輸入 Fragment 或案例 ID...",
                key="search_box"
            )
            st.session_state.q_text = query

        with col_clear:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除條件", use_container_width=True, on_click=clear_search_action):
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 重新查詢", use_container_width=True):
                st.rerun()

        # 4. 精確搜尋結果渲染
        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            # 💡 只保留使用者輸入的原始詞，移除所有自動聯想邏輯
            raw_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []

            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '').lower()
                section_path = str(path_map.get(c.get('section_id'), "")).lower()
                steps_raw = str(c.get('custom_steps_separated', '')) + str(c.get('custom_steps', ''))
                searchable_text = (title + section_path + steps_raw).lower()
                
                is_all_match = True
                total_score = 0
                
                # 核心：嚴格交集搜尋 (所有輸入的詞都必須在該案例中出現)
                for term in raw_terms:
                    # 🚀 不再調用 multi_lang_search，只比對原詞
                    if not (term in searchable_text or term in cid):
                        is_all_match = False
                        break
                    else:
                        # 評分僅用於排序：標題含有關鍵字排最前面
                        if term in title: total_score += 1000
                        if term in section_path: total_score += 500
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    scored_results.append((total_score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.write(f"### 🎯 找到 {len(scored_results)} 個案例")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji = "🟢" if u_info.get("is_active") else "🔴"
                author_style = "color: #4CAF50; background: rgba(76,175,80,0.15);" if u_info.get("is_active") else "color: #ff4b4b; background: rgba(255,75,75,0.15);"
                
                curr_path = path_map.get(item.get('section_id'), "None")
                st.markdown(f'<div class="case-path-text">📂 {curr_path}</div>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">📄 {item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} 👤 {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("🔽 查看測試步驟"):
                    raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or []
                    if isinstance(raw_steps, list) and len(raw_steps) > 0:
                        for i, s in enumerate(raw_steps, 1):
                            st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html(s.get("content", ""))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{clean_html(item.get("custom_steps", ""))}</div>', unsafe_allow_html=True)
                st.markdown("---")
    else:
        st.error(f"❌ 無法連線至 TestRail，請檢查設定。")
else:
    st.info("👈 請在左側 [連線設定] 輸入資料後開始查詢。")
