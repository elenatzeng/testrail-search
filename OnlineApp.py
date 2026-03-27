import streamlit as st
import re
import os
import sys

# 🛡️ 1. 路徑保險
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🛡️ 2. 安全導入
try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"⚠️ 核心導入失敗: {e}")
    st.stop()

# 🛡️ 3. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="請輸入關鍵字...", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # 初始化得分
                exact_id_match, path_score, title_score, content_score = 0, 0, 0, 0
                is_match = True
                
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    is_id, is_path, is_title, is_content = any(w == cid for w in exp), any(w in f_path for w in exp), any(w in title for w in exp), any(w in steps_str for w in exp)
                    
                    if is_id: exact_id_match = 1
                    if is_path: path_score += 1
                    if is_title: title_score += 1
                    if is_content: content_score += 1
                    if not (is_id or is_path or is_title or is_content): is_match = False; break
                
                if is_match:
                    # 💡 核心：抓取 users.py 的權重與在職狀態
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    user_weight = u_info.get("weight", 0)
                    is_active_val = 1 if u_info.get("is_active") else 0
                    
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    
                    # ✨ 權重優先級排序：ID > 路徑 > 標題 > 使用者權重 > 步驟數
                    sort_key = (
                        -exact_id_match, 
                        -path_score, 
                        -title_score, 
                        -user_weight,   # 💡 這裡吃 USER_CONFIG 的 70/5，權重高的排前面
                        -step_count, 
                        -content_score,
                        -is_active_val, # 在職優先
                        f_path
                    )
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, u_info))

            results.sort(key=lambda x: x[0])

            if results:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    
                    # 💡 渲染紅燈邏輯
                    st_class = "active" if u.get("is_active") else "inactive"
                    st_icon = "🟢" if u.get("is_active") else "🔴"
                    tag = f'<span class="author-tag status-{st_class}">{st_icon} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟"):
                        # ... (此處放妳原本的渲染 logic)
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center;">請輸入關鍵字開始檢索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 請先完成連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
