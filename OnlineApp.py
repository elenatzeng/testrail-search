import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# ✨ 引入字典與「獨立」的使用者管理名單
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

# --- 4. 側邊欄 (完全還原妳的原始配置) ---
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("帳號 Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password", value=st.query_params.get("pw", ""))
    project_id = st.number_input("Project ID", value=int(st.query_params.get("pid", 1)))
    suite_id = st.number_input("Suite ID", value=int(st.query_params.get("sid", 1)))
    
    # ✨ 妳要的儲存至網址按鈕 (已補回)
    if st.button("💾 儲存資訊至網址"):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=str(project_id), sid=str(suite_id))
        st.success("✅ 儲存成功！")
        st.balloons()
        
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
        
        # 💡 名單對應邏輯 (改由 users.py 供應，不影響 UI)
        u_map = {uid: info["name"] for uid, info in USER_CONFIG.items()}
        
        def get_all(method, key, **kwargs):
            all_items, offset = [], 0
            while True:
                res = method(**kwargs, limit=250, offset=offset)
                items = res[key] if isinstance(res, dict) and key in res else res
                if not items: break
                all_items.extend(items)
                if len(items) < 250: break
                offset += 250
            return all_items

        all_sects = get_all(api.sections.get_sections, 'sections', project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in all_sects}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        all_cases = get_all(api.cases.get_cases, 'cases', project_id=pid, suite_id=sid)
        return all_cases, path_map, u_map, time.strftime("%H:%M:%S"), p_name
    except Exception as e:
        return None, str(e), {}, None, ""

# --- 6. 主介面邏輯 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    data_container = st.empty()
    data_container.info("⏳ 正在同步 TestRail 數據...")
    all_cases, path_map, user_map, sync_time, project_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases:
        data_container.empty()
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b>{project_name} | <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        query = st.text_input("🔍 搜尋內容 (輸入 Key、地道繁體或 #ID):", placeholder="依照關鍵字的關聯性與完整度排序")

        if query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            search_terms = multi_lang_search(query)
            
            scored_results = []
            for c in all_cases:
                score = 0
                cid, title = str(c.get('id', '')), c.get('title', '').lower()
                section_path = path_map.get(c.get('section_id'), "").lower()
                author_id = c.get('created_by')
                u_info = USER_CONFIG.get(author_id, DEFAULT_CONFIG)
                
                raw_steps = c.get('custom_steps_separated') or c.get('custom_steps') or c.get('steps') or []
                steps_count = len(raw_steps) if isinstance(raw_steps, list) else 0
                content_len = len(str(raw_steps))
                full_text = str(c).lower()
                
                # --- [ 基礎評分 ] ---
                if query.lower().strip('#') == cid: score += 100000
                if any(term in section_path for term in search_terms): score += 50000
                if any(term in title for term in search_terms): score += 10000
                if any(term in full_text for term in search_terms): score += 1000

                # --- [ 進階排序修正 ] ---
                if score > 0:
                    score += (steps_count * 500) + (content_len // 10)
                    score += u_info.get("weight", 0)
                    if not u_info.get("is_active", True): score -= 45000
                    if steps_count == 0 or content_len < 15: score -= 40000 
                    scored_results.append((score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            
            if scored_results:
                st.write(f"### 🎯 找到 {len(scored_results)} 個案例")
                for _, item, u_info in scored_results:
                    cid = str(item.get('id'))
                    
                    # 💡 視覺標籤控制 (不影響 UI 配置，僅決定顏色與文字)
                    if u_info["is_active"]:
                        author_style = "color: #4CAF50; background: rgba(76, 175, 80, 0.15); border: 1.5px solid #4CAF50;"
                        display_name = u_info["name"]
                    else:
                        author_style = "color: #8b949e; background: rgba(255, 255, 255, 0.05); border: 1px solid #444c56;"
                        display_name = f"{u_info['name']} (離職)"

                    with st.container():
                        st.markdown(f'<span style="font-size:12px; color:#8b949e;">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small style="color:#8b949e">(#{cid})</small> <span class="author-tag" style="{author_style}">👤 {display_name}</span></div>', unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                        with st.expander("🔽 查看測試步驟"):
                            raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or item.get('steps')
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box">{clean_html_and_add_numbers(s.get("content", s.get("step", "")))}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50;">{clean_html_and_add_numbers(s.get("expected", ""))}</div></div>', unsafe_allow_html=True)
                            else: st.info("無步驟資料。")
                        st.markdown("---")
            else: st.warning("查無搜尋結果。")
    else: st.error(f"❌ 同步失敗")
else: st.warning("👈 請輸入連線資訊。")
