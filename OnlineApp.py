import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# ✨ 引入字典與獨立的使用者管理名單
try:
    from keywords import SEARCH_DICTIONARY
except ImportError:
    SEARCH_DICTIONARY = []

try:
    from users import USER_CONFIG, DEFAULT_CONFIG
except ImportError:
    USER_CONFIG = {}
    DEFAULT_CONFIG = {"name": "Other", "weight": 0, "is_active": True}

# --- 1. 核心邏輯：步驟格式整理 ---
def clean_html_and_add_numbers(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    text = text.replace('<li>', '\n')
    text = re.sub(r'<(br\s*/?|/div|/p|/li)>', '\n', text) 
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    raw_lines = text.split('\n')
    lines = [l.strip() for l in raw_lines if l.strip()]
    if not lines: return text.strip() if text.strip() else "（無詳細步驟）"
    numbered_lines = [f"{i}. {line}" if not re.match(r'^\d+[\.\、]', line) else line for i, line in enumerate(lines, 1)]
    return "\n".join(numbered_lines)

# --- 2. 三語聯想搜尋核心 ---
def multi_lang_search(text):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in SEARCH_DICTIONARY:
        group_lower = [str(word).lower() for word in group]
        if any(text_lower in word for word in group_lower) or any(word in text_lower for word in group_lower):
            related_words.update(group_lower)
    return list(related_words)

# --- 3. UI 視覺風格 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
    h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }
    [data-testid="stHeader"], [data-testid="stTopBar"], div[data-testid="stMainMenu"] { display: none !important; visibility: hidden !important; }
    [data-testid="stSidebarCollapse"] { top: 10px !important; left: 10px !important; position: fixed !important; z-index: 1000001 !important; color: white !important; background-color: rgba(255,255,255,0.1) !important; border-radius: 50% !important; }
    div[data-testid="stSidebar"] .stButton button { background-color: #ffffff !important; color: #000000 !important; border: 1px solid #ffffff !important; width: 100% !important; height: 45px !important; font-weight: 800 !important; }
    div[data-testid="stSidebar"] .stButton button p { color: #000000 !important; }
    .step-content-box { color: #ffffff !important; font-size: 15px !important; line-height: 1.8 !important; white-space: pre-wrap !important; background: #1c2128; padding: 15px; border-radius: 10px; margin-top: 8px; border: 1px solid #30363d; }
    .step-item { border-left: 5px solid #4CAF50; padding-left: 20px; margin-bottom: 30px; }
    .stTextInput input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    .location-tag { background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px; }
    .author-tag { font-size: 11px; border-radius: 12px; padding: 3px 12px; display: inline-block; margin-left: 10px; }
    .view-btn { display: inline-block; padding: 6px 16px; background-color: #238636; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 側邊欄 ---
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("帳號 Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password", value=st.query_params.get("pw", ""))
    project_id = st.number_input("Project ID", value=int(st.query_params.get("pid", 1)))
    suite_id = st.number_input("Suite ID", value=int(st.query_params.get("sid", 1)))
    if st.button("🔄 強制更新數據"):
        st.cache_data.clear()
        st.rerun()

# --- 5. 數據抓取 ---
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    if not _url or not _user or not _pw: return None, "資訊不足", {}, None, ""
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        p_name = p_info.get('name', f"Project #{pid}")
        all_sects = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in all_sects}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        all_cases = api.cases.get_cases(project_id=pid, suite_id=sid)
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_name
    except Exception as e:
        return None, str(e), None, ""

# --- 6. 主介面 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, project_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    if all_cases:
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b>{project_name} | <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        query = st.text_input("🔍 搜尋內容 (輸入 Key、地道繁體或 #ID):")

        if query:
            search_terms = multi_lang_search(query)
            scored_results = []
            for c in all_cases:
                score = 0
                cid, title = str(c.get('id', '')), c.get('title', '').lower()
                section_path = path_map.get(c.get('section_id'), "").lower()
                author_id = c.get('created_by')
                
                # 取得使用者配置
                u_info = USER_CONFIG.get(author_id, DEFAULT_CONFIG)
                
                # 基礎評分邏輯
                if query.lower().strip('#') == cid: score += 100000
                if any(term in section_path for term in search_terms): score += 50000
                if any(term in title for term in search_terms): score += 10000
                
                if score > 0:
                    score += u_info["weight"] # 套用權重
                    # 💡 自動處理離職降權：如果不是在職，大幅扣分
                    if not u_info.get("is_active", True): score -= 45000
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            for _, item, u_info in scored_results:
                # 💡 動態決定頭像顏色
                if u_info["is_active"]:
                    # 在職：亮綠標
                    author_style = "color: #4CAF50; background: rgba(76, 175, 80, 0.15); border: 1.5px solid #4CAF50;"
                    display_name = u_info["name"]
                else:
                    # 離職：灰標
                    author_style = "color: #8b949e; background: rgba(255, 255, 255, 0.05); border: 1px solid #444c56;"
                    display_name = f"{u_info['name']} (離職)"

                with st.container():
                    st.markdown(f'<span style="font-size:12px; color:#8b949e;">{path_map.get(item.get("section_id"))}</span>', unsafe_allow_html=True)
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small style="color:#8b949e">(#{item.get("id")})</small> <span class="author-tag" style="{author_style}">👤 {display_name}</span></div>', unsafe_allow_html=True)
                    # (下方省略 Open Case 與 Steps 顯示邏輯，保持原本架構即可)
