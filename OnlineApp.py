import streamlit as st
import re
import os
import sys

# 🛡️ 1. 路徑保險：確保雲端能讀到同目錄組件
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🛡️ 2. 安全導入組件
try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"⚠️ 核心組件導入失敗: {e}")
    st.stop()

# 🛡️ 3. 頁面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)
apply_custom_style()

# ✨ 【停機坪】
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄 (連線設定)
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

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                "", 
                value=st.session_state.q_text, 
                placeholder="請輸入關鍵字查詢，多個關鍵字請以空格隔開", 
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

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 核心權重維度初始化 ---
                exact_id_match = 0    # 1. ID 精準匹配
                path_score = 0        # 2. 功能路徑
                title_score = 0       # 3. 標題關聯
                content_score = 0     # 4. 內容檢索
                step_count = len(steps_raw) if isinstance(steps_raw, list) else 0 # 5. 完整度
                
                is_match = True
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 判斷維度
                    is_id = any(w == cid for w in exp)
                    is_path = any(w in f_path for w in exp)
                    is_title = any(w in title for w in exp)
                    is_content = any(w in steps_str for w in exp)
                    
                    if is_id: exact_id_match = 1
                    if is_path: path_score += 1
                    if is_title: title_score += 1
                    if is_content: content_score += 1
                    
                    if not (is_id or is_path or is_title or is_content):
                        is_match = False; break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 6 & 7. 維護者權重與狀態處理
                    is_active = 1 if user_info.get("is_active") else 0
                    penalty = 0
                    if "Meh" in user_info.get("name", ""): penalty = 1 # 地雷標記
                    
                    # ✨ 封裝排序元組 (Tuple Sort) - 嚴格遵守妳要求的優先級
                    # Python 預設升序，所以「越高越好」的維度要取負數
                    sort_key = (
                        -exact_id_match, # 優先級 1
                        -path_score,     # 優先級 2
                        -title_score,    # 優先級 3
                        -content_score,  # 優先級 4
                        -step_count,     # 優先級 5
                        -is_active,      # 優先級 6
                        penalty,         # 優先級 7
                        f_path           # 最後保底：按路徑 A-Z
                    )
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, user_info))

            # ✨ 執行物理鎖死排序
            results.sort(key=lambda x: x[0])

            # --- 渲染結果 ---
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
                        # ... (步驟渲染邏輯保持不變)
                        st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">請輸入關鍵字開始檢索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 請先在左側完成連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
