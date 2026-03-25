import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 基礎頁面設定
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄連線設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_val = get_val("pid")
    sid_val = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_val) if pid_val else 10)
    sid = st.number_input("Suite ID", value=int(sid_val) if sid_val else 10)
    
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f'<div style="color:#8b949e; font-size:13px;">📍 {p_name} | #{sid}</div>', unsafe_allow_html=True)
        q_input = st.text_input("● 搜尋內容:", value=st.session_state.get("q_text", ""), placeholder="輸入關鍵字...")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            for case_item in all_cases:
                cid = str(case_item.get('id'))
                title = str(case_item.get('title', '')).lower()
                path = str(path_map.get(case_item.get('section_id'), '')).lower()
                
                # 取得清理後的步驟內容
                steps_data = clean_html(str(case_item.get('custom_steps','')) + str(case_item.get('custom_steps_separated','')))
                steps_str = str(steps_data).lower()
                
                is_match = True
                score = 0
                for t in terms:
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title + path + steps_str) for w in expanded) or any(w == cid for w in expanded)):
                        is_match = False; break
                    if any(w in title for w in expanded): score += 5000
                
                if is_match:
                    u_info = USER_CONFIG.get(int(case_item.get('created_by', 0)), DEFAULT_CONFIG)
                    score += u_info.get("weight", 0)
                    # 🚀 沉底邏輯：無內容直接扣兩百萬分
                    if len(steps_str.strip()) < 10 or "(無詳細步驟)" in steps_str:
                        score -= 2000000
                    results.append((score, case_item, u_info))

            results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(results)} 個案例")

            for _, item, u_info in results:
                cid = str(item.get('id'))
                is_active = u_info.get('is_active', True)
                author_color = '#4CAF50' if is_active else '#8b949e'
                
                # 1. 顯示路徑 (圓圈 6)
                st.markdown(f'<div style="font-size:13px; color:#8b949e; margin-bottom:5px; margin-top:25px;">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                
                # 2. 標題與標籤 (圓圈 7 & 8)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                with c1:
                    tag_html = f'<span class="author-tag" style="border-color:{author_color}!important; box-shadow: 0 0 5px {author_color}!important;">{"🟢" if is_active else "⚪"} {u_info["name"]}</span>'
                    st.markdown(f"""
                        <div style="display:flex; align-items:center;">
                            <span style="font-size:18px; font-weight:bold; color:white;">{item.get('title')} (#{cid})</span>
                            {tag_html}
                        </div>
                    """, unsafe_allow_html=True)
                
                # 3. 按鈕 (圓圈 10)
                with c2:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 4. 展開步驟 (圓圈 9)
                with st.expander("🔽 查看測試步驟"):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    if isinstance(steps, list):
                        for i, s in enumerate(steps, 1):
                            st.markdown(f"""
                                <div class="step-container">
                                    <div class="step-label" style="color:#4CAF50;">Step {i}:</div>
                                    <div class="step-content-box">{s.get('content','')}</div>
                                    <div class="step-label" style="color:#8b949e; margin-top:10px;">Expected:</div>
                                    <div class="step-content-box" style="border-left: 1px dashed #444c56;">{s.get('expected','')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{steps if steps else "(無詳細步驟)"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)
