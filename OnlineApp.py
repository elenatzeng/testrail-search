import streamlit as st
import re
import os
import sys

# 🛡️ 1. 路徑保險：防止雲端 KeyError: 'style'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🛡️ 2. 安全導入自定義組件
try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"⚠️ 核心組件加載失敗: {e}")
    st.stop()

# 🛡️ 3. 頁面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)

# 執行 CSS (包含頂部固定、隱藏貓咪、星空背景)
apply_custom_style()

# ✨ 錨點：火箭飛回頂端用
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

# --- 🛠️ 數據記憶邏輯 ---
def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# --- 🔐 側邊欄設定 ---
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
        st.success("✅ 已儲存設定")
    
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# --- 🧪 核心數據邏輯 ---
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 🔍 搜尋列狀態管理
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                "", 
                value=st.session_state.q_text, 
                placeholder="請輸入關鍵字，多關鍵字請以空格隔開", 
                label_visibility="collapsed",
                key=f"search_input_{st.session_state.search_key}"
            )
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): 
                st.session_state.q_text = "" 
                st.session_state.search_key += 1 
                st.rerun() 
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): 
                st.rerun()

        # --- 🏆 核心排序與檢索 ---
        if st.session_state.q_text:
            raw_q = st.session_state.q_text.strip()
            terms = [t.lower() for t in raw_q.split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                
                match_score = 0
                is_match = True
                
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    title_match = any(w in title.lower() for w in exp) or any(w == cid for w in exp)
                    path_match = any(w in f_path.lower() for w in exp)
                    
                    if title_match: match_score += 10
                    elif path_match: match_score += 1
                    else: is_match = False; break
                
                if is_match:
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                    # 品質權重 (0 或 1)
                    quality_rank = 1 if len(str(steps_raw)) > 10 else 0
                    
                    # ✨ 鎖死排序：[匹配分(高到低), 品質分(高到低), 路徑(A-Z)]
                    sort_key = (-match_score, -quality_rank, f_path)
                    results.append((sort_key, f_path, c, u_info))

            # 🛠️ 執行元組排序 (Tuple Sort)
            results.sort(key=lambda x: x[0])

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px; padding-left:5px;">🚫 找不到符合的測試案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟", expanded=False):
                        # ... (此處保留妳原本的步驟渲染邏輯)
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        # ... (略過重複的渲染代碼，請保持妳原本的步驟渲染)
                        st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">請輸入關鍵字開始檢索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 請先在左側完成連線設定。")

# ✨ 小火箭 (提示文字改為繁體)
st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
