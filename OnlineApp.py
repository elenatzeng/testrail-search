import streamlit as st
import os
import sys

# 🛡️ 1. 環境路徑保險 (解決 KeyError: 'style' 報錯)
# 強制將當前目錄加入 Python 搜尋路徑，確保雲端能讀到 style.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 嘗試匯入自定義樣式
try:
    from style import apply_custom_style
except ImportError:
    # 備用方案：若讀取失敗，定義空函數避免程式崩潰
    def apply_custom_style():
        pass

# 🛡️ 2. 匯入妳的工具函式與設定 (請確保檔名正確)
try:
    from utils import fetch_data_from_tr, multi_lang_search
    # 如果妳有這些設定檔，請取消註解；若無，請確認妳的邏輯
    # from users import USER_CONFIG, DEFAULT_CONFIG
    # from keywords import SEARCH_DICTIONARY
except ImportError as e:
    st.error(f"缺少必要組件: {e}")

# --- 🛠️ 頁面基本配置 ---
st.set_page_config(
    page_title="TestRail AI Search Center", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)

# 執行 CSS 樣式 (隱藏貓咪、設定星空、保留左側拉環)
apply_custom_style()

# --- 🚀 自動記憶與 URL 參數邏輯 ---
# 這些 Key 用於在換螢幕或重整時保住數據
keys_to_store = ["url", "user", "pw", "pid", "sid"]
for k in keys_to_store:
    store_key = f"store_{k}"
    if store_key not in st.session_state:
        st.session_state[store_key] = ""

def get_val(key):
    # 先看網址參數有沒有，沒有再看 Session 暫存
    val = st.query_params.get(key)
    if val is not None:
        return val
    return st.session_state.get(f"store_{key}", "")

# --- 🔐 側邊欄設定 ---
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    
    # 讀取 PID / SID
    pid_v = get_val("pid")
    sid_v = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存並記住我", use_container_width=True):
        # 將設定寫入網址參數，這樣重整就不會丟失
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.session_state.store_url = tr_url
        st.session_state.store_user = tr_user
        st.session_state.store_pw = tr_pw
        st.session_state.store_pid = str(pid)
        st.session_state.store_sid = str(sid)
        st.success("✅ 已儲存連線資訊")

# --- 🧪 主畫面邏輯 ---
st.title("🧪 TestRail 智能邏輯檢索")
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

if tr_url and tr_user and tr_pw:
    # 獲取數據 (這部分通常在 utils.py)
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project: **{p_name}** | Suite: **#{sid}**", unsafe_allow_html=True)
        
        # 搜尋框邏輯
        if "q_text" not in st.session_state:
            st.session_state.q_text = ""
            
        q_input = st.text_input(
            "多維精準檢索 :", 
            value=st.session_state.q_text, 
            placeholder="支援多關鍵字交集過濾，兼容繁/簡/英關鍵字或 #ID",
            key="search_input_box"
        )
        st.session_state.q_text = q_input

        # 執行搜尋與排序
        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            
            for c in all_cases:
                # 這裡放妳的排序權重算法...
                # (這部分依據妳之前的邏輯：標題匹配度 + 步驟完整度權重)
                # results.append((score, path, case_data, user_info))
                pass
            
            # 排序：權重由高到低
            # results.sort(key=lambda x: (-x[0], x[1]))
            
            # 渲染結果...
            st.info(f"🔍 找到符合的測試用例...")
        else:
            st.info("💡 請在上方輸入關鍵字開始檢索")
else:
    st.warning("👈 請先在側邊欄輸入連線資訊")

# --- 🚀 回頂端火箭 (配合 style.py) ---
st.markdown('<a href="#top-anchor" class="scroll-to-top" style="color:white;text-decoration:none;">🚀</a>', unsafe_allow_html=True)
