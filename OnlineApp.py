import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面基礎配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v = get_val("pid")
    sid_v = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    if st.button("💾 儲存並刷新數據", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f'<div style="color:#8b949e; font-size:13px;">📍 {p_name} | #{sid}</div>', unsafe_allow_html=True)
        
        # 🚀 這裡把功能鈕加回來了！排成一列
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="輸入關鍵字...", label_visibility="collapsed")
            st.session_state.q_text = q_input

        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()

        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): 
                st.rerun()

        # 4. 搜尋與排序顯示
        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            terms = [t.lower() for t in final_query.strip().split() if t]
            results = []
            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', '')).lower()
                path = str(path_map.get(c.get('section_id'), '')).lower()
                steps_raw = str(c.get('custom_steps','')) + str(c.get('custom_steps_separated',''))
                
                is_match = True
                score = 0
                for t in terms:
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title + path + steps_raw.lower()) for w in expanded) or any(w == cid for w in expanded)):
                        is_match = False; break
                    if any(w in title for w in expanded): score += 5000
                
                if is_match:
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    score += u_info.get("weight", 0)
                    if len(steps_raw.strip()) < 15: score -= 2000000
                    results.append((score, c, u_info))

            results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(results)} 個案例")

            for _, item, u_info in results:
                cid = str(item.get('id'))
                is_active = u_info.get('is_active', True)
                author_color = '#4CAF50' if is_active else '#8b949e'
                
                # 1. 路徑
                display_path = path_map.get(item.get("section_id"), "Root")
                st.markdown(f'<div class="case-path-box">{display_path}</div>', unsafe_allow_html=True)
                
                # 2. 標題與標籤
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                with c1:
                    tag_html = f'<span class="author-tag" style="border-color:{author_color}!important; box-shadow: 0 0 5px {author_color}!important; margin-left:15px !important;">{"🟢" if is_active else "⚪"} {u_info["name"]}</span>'
                    st.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:19px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 3. 展開步驟
                with st.expander("🔽 查看測試步驟"):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    if isinstance(steps, list):
                        for i, s in enumerate(steps, 1):
                            st.markdown(f"""
                                <div class="step-container">
                                    <div style="color:#4CAF50; font-size:15px; font-weight:bold;">Step {i}:</div>
                                    <div class="step-content-box" style="white-space: pre-wrap;">{s.get('content','')}</div>
                                    <div style="color:#8b949e; font-size:15px; font-weight:bold; margin-top:12px;">Expected:</div>
                                    <div class="step-content-box" style="border-left: 1px dashed #444c56; white-space: pre-wrap;">{s.get('expected','')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box" style="white-space: pre-wrap;">{steps if steps else "(無詳細步驟)"}</div>', unsafe_allow_html=True)
                st.markdown('<hr style="border:0.5px solid #30363d; margin: 25px 0;">', unsafe_allow_html=True)

    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)
