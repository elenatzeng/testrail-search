import streamlit as st
import re
import os
import sys

# 🛡️ 路徑保險
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"導入失敗: {e}"); st.stop()

# 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# 頂部錨點
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

# 數據讀取
def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("User", value=get_val("user"))
    tr_pw = st.text_input("PW", type="password", value=get_val("pw"))
    pid = st.number_input("PID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("SID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("💾 儲存並記住我", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 刷新數據", use_container_width=True): st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        # 搜尋框介面
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="搜尋關鍵字...", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        # --- 🏆 核心排序引擎 ---
        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                exact_id_m, path_s, title_s, content_s = 0, 0, 0, 0
                is_match = True
                
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    id_m, p_m, t_m, c_m = any(w==cid for w in exp), any(w in f_path for w in exp), any(w in title for w in exp), any(w in steps_str for w in exp)
                    if id_m: exact_id_m = 1
                    if p_m: path_s += 1
                    if t_m: title_s += 1
                    if c_m: content_s += 1
                    if not (id_m or p_m or t_m or c_m): is_match = False; break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 💡 優先級鎖死：1.ID匹配 > 2.人員權重(70/5) > 3.步驟長度 > 4.標題匹配
                    sort_key = (
                        -exact_id_m,
                        -u.get("weight", 0),  # 70 會排在 5 前面
                        -len(steps_str),     # 內容越長越好
                        -path_s, 
                        -title_s, 
                        -content_s,
                        f_path
                    )
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, u))

            results.sort(key=lambda x: x[0])

            # --- 渲染區 ---
            for _, path, item, u in results:
                cid = str(item.get('id'))
                st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                
                # 🔴 離職紅燈邏輯
                st_class = "active" if u.get("is_active") else "inactive"
                st_icon = "🟢" if u.get("is_active") else "🔴"
                tag = f'<span class="author-tag status-{st_class}">{st_icon} {u["name"]}</span>'
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("查閱測試步驟"):
                    # 步驟渲染邏輯 (簡略，請保持妳原本的完整渲染)
                    st.write(item.get('custom_steps') or item.get('custom_steps_separated'))

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
