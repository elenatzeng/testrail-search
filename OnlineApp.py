import streamlit as st
import re
import os
import sys

# 🛡️ 1. 路徑保險
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

# 🛡️ 2. 安全導入
try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"導入失敗: {e}"); st.stop()

# 🛡️ 3. 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

# ✨ 錨點
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("Suite ID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("💾 儲存資訊並記住", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True): st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 4. 核心邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="搜尋關鍵字...", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        # --- 🏆 核心排序引擎 (標題 > 內容 > 權重) ---
        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # 得分初始化
                title_s, content_s, path_s, exact_id_m = 0, 0, 0, 0
                is_match = True
                
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    t_m = any(w in title for w in exp) # 💡 包含字典命中
                    c_m = any(w in steps_str for w in exp)
                    p_m = any(w in f_path for w in exp)
                    id_m = (t == cid)
                    
                    if t_m: title_s += 1
                    if c_m: content_s += 1
                    if p_m: path_s += 1
                    if id_m: exact_id_m = 1
                    
                    if not (id_m or t_m or c_m or p_m):
                        is_match = False; break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    u_weight = u.get("weight", 0)
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0

                    # ✨✨✨ 終極排序元組 (由小到大排序，所以數值越高者加負號) ✨✨✨
                    sort_key = (
                        -title_s,     # 1. 標題命中 (最優先)
                        -step_count,  # 2. 步驟豐富度 (多者在前)
                        -u_weight,    # 3. 人員權重 (70分插隊)
                        -exact_id_m,  # 4. ID 匹配
                        -content_s,   # 5. 內容命中
                        f_path        # 6. 路徑 A-Z
                    )
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, u))

            results.sort(key=lambda x: x[0])

            # --- 渲染區 ---
            for _, path, item, u in results:
                cid = str(item.get('id'))
                st_class = "active" if u.get("is_active") else "inactive"
                st_icon = "🟢" if u.get("is_active") else "🔴"
                tag = f'<span class="author-tag status-{st_class}">{st_icon} {u["name"]}</span>'
                
                st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                
                with st.expander("查閱測試步驟"):
                    st.write(item.get('custom_steps') or item.get('custom_steps_separated'))

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
