import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid") or 10))
    sid = st.number_input("Suite ID", value=int(get_val("sid") or 10))
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f'<div style="color:#8b949e; font-size:14px; margin-bottom:20px;">📍 Project：{p_name} | Suite：#{sid}</div>', unsafe_allow_html=True)
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_search:
            q_input = st.text_input("● 搜尋內容:", value=st.session_state.q_text, placeholder="輸入關鍵字...")
            st.session_state.q_text = q_input

        # 搜尋與過濾邏輯
        final_query = st.session_state.q_text
        if final_query:
            terms = [t.lower() for t in final_query.strip().split() if t]
            results = []
            for case in all_cases:
                cid = str(case.get('id'))
                title = str(case.get('title', '')).lower()
                path = str(path_map.get(case.get('section_id'), '')).lower()
                
                # 取得內容並判斷是否為空
                steps_raw = clean_html(str(case.get('custom_steps','')) + str(case.get('custom_steps_separated','')))
                steps_str = str(steps_raw).lower()
                
                is_match = True
                score = 0
                for t in terms:
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title + path + steps_str) for w in expanded) or any(w == cid for w in expanded)):
                        is_match = False; break
                    if any(w in title for w in expanded): score += 5000
                
                if is_match:
                    u_info = USER_CONFIG.get(int(case.get('created_by', 0)), DEFAULT_CONFIG)
                    score += u_info.get("weight", 0)
                    if len(steps_str.strip()) < 10 or "(無詳細步驟)" in steps_str: score -= 2000000
                    results.append((score, case, u_info))

            results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(results)} 個案例")

            for _, item, u_info in results:
                cid = str(item.get('id'))
                color = '#4CAF50' if u_info.get('is_active') else '#8b949e'
                tag_html = f'<span class="author-tag" style="border-color:{color}!important; box-shadow: 0 0 5px {color}!important;">{"🟢" if u_info.get("is_active") else "⚪"} {u_info["name"]}</span>'
                
                st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:20px;">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([7.5, 1.5], vertical_alignment="center")
                with c1:
                    st.markdown(f'<div style="font-size:17px; font-weight:bold; display:flex; align-items:center;">{item.get("title")} (#{cid}) {tag_html}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("🔽 查看測試步驟"):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    if isinstance(steps, list):
                        for i, s in enumerate(steps, 1):
                            # 🚀 這裡用 pre-line 盒子來裝文字，保證換行
                            st.markdown(f"""
                                <div class="step-container">
                                    <span class="step-label">Step {i}:</span>
                                    <div class="step-content-box">{s.get('content','')}</div>
                                    <span class="step-label">Expected:</span>
                                    <div class="step-content-box" style="border-left: 1px dashed #444c56;">{s.get('expected','')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{steps if steps else "(無詳細步驟)"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)
