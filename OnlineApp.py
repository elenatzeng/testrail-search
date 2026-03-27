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

# 🛡️ 3. 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

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
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        # 搜尋列佈局
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="搜尋關鍵字...", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
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
                
                # --- 排序維度初始化 ---
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
                    u_weight = u.get("weight", 0)
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0

                    # ✨✨✨ 物理鎖死排序元組 ✨✨✨
                    # 順序：1.ID匹配 > 2.人員權重(Katty/Elena優先) > 3.步驟數(豐富度) > 4.關鍵字匹配度
                    sort_key = (
                        -exact_id_m,    # 優先級 1
                        -u_weight,      # 優先級 2 (💡 人對了才優先，雷包 5 分絕對沉底)
                        -step_count,    # 優先級 3 (💡 妳說的：步驟越多越前面)
                        -path_s,        # 優先級 4
                        -title_s,       # 優先級 5
                        -content_s,     # 優先級 6
                        f_path          # 優先級 7
                    )
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, u))

            # 物理排序執行
            results.sort(key=lambda x: x[0])

            # --- 渲染結果 ---
            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px;">🚫 找不到符合的案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_on_job = u.get("is_active", True)
                    st_class = "active" if is_on_job else "inactive"
                    st_icon = "🟢" if is_on_job else "🔴"
                    
                    # 💡 紅框渲染鎖死
                    tag = f'<span class="author-tag status-{st_class}">{st_icon} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟", expanded=False):
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        if steps_data: st.write(steps_data)
                        else: st.write("(無內容)")
                st.markdown("---")
else:
    st.info("👈 請先完成連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
