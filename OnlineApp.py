import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v = get_val("pid"); sid_v = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f'<div style="color:#8b949e; font-size:14px;">📍 Project：{p_name} | Suite：#{sid}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容 (輸入關鍵字查詢；支援繁簡體與英文):</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="充值 CNY", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = ""; st.rerun()
        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            for c in all_cases:
                cid = str(c.get('id'))
                # 🚀 抓取正確的路徑字串進行搜尋與顯示
                full_path = path_map.get(c.get('section_id'), "Unknown Path")
                title = str(c.get('title', '')).lower()
                is_match = True; score = 0
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title + full_path.lower()) for w in exp) or any(w == cid for w in exp)):
                        is_match = False; break
                    if any(w in title for w in exp): score += 5000
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((score + u.get("weight", 0), c, u))

            results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(results)} 個案例 (已過濾交集結果)")

            for _, item, u in results:
                cid = str(item.get('id'))
                color = '#4CAF50' if u.get('is_active') else '#8b949e'
                # 🚀 顯示修正後的路徑 (圓圈 6)
                st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:20px; margin-bottom:5px;">{path_map.get(item.get("section_id"), "Unknown Path")}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                with c1:
                    tag = f'<span class="author-tag" style="border-color:{color}!important; box-shadow: 0 0 5px {color}!important;">{"🟢" if u.get("is_active") else "⚪"} {u["name"]}</span>'
                    st.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("🔽 查看測試步驟"):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    if isinstance(steps, list):
                        for i, s in enumerate(steps, 1):
                            st.markdown(f"""<div class="step-container">
                                <div style="color:#ffffff; font-weight:bold; font-size:14px; margin-bottom:5px;">Step {i}:</div>
                                <div class="step-content-box">{s.get('content','')}</div>
                                <div style="color:#ffffff; font-weight:bold; font-size:14px; margin-top:12px; margin-bottom:5px;">Expected:</div>
                                <div class="step-content-box" style="border-left:1px dashed #444c56;">{s.get('expected','')}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{steps if steps else "(無詳細步驟)"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # 🚀 橘色按鈕補完
    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)
