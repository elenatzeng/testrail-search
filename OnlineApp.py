import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# ✨ 嘗試引入外部字典，若檔案不存在則預設為空，防止當機
try:
    from keywords import SEARCH_DICTIONARY
except ImportError:
    SEARCH_DICTIONARY = []

# --- 1. 核心邏輯：修復條列式數字 (找回 1. 2. 3. 並防止空白) ---
def clean_html_and_add_numbers(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 預處理換行標籤
    text = text.replace('<li>', '\n')
    text = re.sub(r'<(br\s*/?|/div|/p|/li)>', '\n', text) 
    
    # 清除 HTML
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    
    # 符號轉義
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 重新組裝數字，確保不會因為 split 導致空白
    raw_lines = text.split('\n')
    lines = [l.strip() for l in raw_lines if l.strip()]
    
    if not lines:
        return text.strip() if text.strip() else "（無詳細步驟）"
    
    numbered_lines = []
    for index, line in enumerate(lines, 1):
        if not re.match(r'^\d+[\.\、]', line):
            numbered_lines.append(f"{index}. {line}")
        else:
            numbered_lines.append(line)
            
    return "\n".join(numbered_lines)

# --- 2. 三語聯想搜尋 ---
def multi_lang_search(text):
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in SEARCH_DICTIONARY:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 3. UI 視覺風格：🏆 究極黑金鎖定版 (物理遮蔽選單) ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 🌑 強制深色背景與文字 */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0b0e14 !important;
    }
    h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown {
        color: #ffffff !important;
    }

    /* 🚫 徹底移除頂部所有選單與按鈕 */
    [data-testid="stHeader"], [data-testid="stTopBar"], div[data-testid="stMainMenu"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* 修正展開箭頭按鈕位置 */
    [data-testid="stSidebarCollapse"] {
        top: 10px !important;
        left: 10px !important;
        position: fixed !important;
        z-index: 1000001 !important;
        color: white !important;
        background-color: rgba(255,255,255,0.1) !important;
        border-radius: 50% !important;
    }

    /* 側邊欄按鈕強化 (白底黑字) */
    div[data-testid="stSidebar"] .stButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        width: 100% !important;
        height: 45px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stSidebar"] .stButton button p { color: #000000 !important; }

    /* 內容區塊樣式 */
    .step-content-box {
        color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
        white-space: pre-wrap !important; 
        background: #1c2128;
        padding: 15px;
        border-radius: 10px;
        margin-top: 8px;
        border: 1px solid #30363d;
    }
    .step-item { border-left: 5px solid #4CAF50; padding-left: 20px; margin-bottom: 30px; }
    .stTextInput input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    .location-tag { background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px; }
    .author-tag { font-size: 11px; color: #4CAF50 !important; background: rgba(76, 175, 80, 0.15); border-radius: 12px; padding: 3px 12px; border: 1.5px solid #4CAF50; }
    .view-btn { display: inline-block; padding: 6px 16px; background-color: #238636; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 參數讀取 ---
q = st.query_params
init_url = q.get("url", st.secrets.get("TR_URL", ""))
init_user = q.get("user", st.secrets.get("TR_USER", ""))
init_pw = q.get("pw", st.secrets.get("TR_PW", ""))
init_pid = int(q.get("pid", st.secrets.get("PROJECT_ID", 1)))
init_sid = int(q.get("sid", st.secrets.get("SUITE_ID", 1)))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=init_url)
    tr_user = st.text_input("帳號 Email", value=init_user)
    tr_pw = st.text_input("API Key", type="password", value=init_pw)
    project_id = st.number_input("Project ID", value=init_pid)
    suite_id = st.number_input("Suite ID", value=init_sid)
    st.markdown("---")
    if st.button("💾 儲存資訊至網址"):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=str(project_id), sid=str(suite_id))
        st.success("✅ 儲存成功！")
        st.balloons()
    if st.button("🔄 強制更新數據"):
        st.cache_data.clear()
        st.rerun()

# --- 5. 數據抓取 (增加連線穩定性) ---
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    if not _url or not _user or not _pw: return None, "請填寫完整連線資訊", {}, None, ""
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        p_name = p_info.get('name', f"Project #{pid}")
        u_map = {2: "Elena", 3: "Esther", 4: "Emma", 5: "Baron", 6: "Meh", 8: "Copper", 11: "Katty"}
        
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
        return None, f"連線失敗: {str(e)}", {}, None, ""

# --- 6. 主介面邏輯 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    # 這裡顯示一個較小的進度提示，避免畫面完全卡死
    data_container = st.empty()
    data_container.info("⏳ 正在同步 TestRail 最新數據，請稍候...")
    
    all_cases, path_map, user_map, sync_time, project_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases:
        data_container.empty() # 清除讀取中提示
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b><span style="color:#58a6ff; font-weight:bold;">{project_name}</span> | <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        
        query = st.text_input("搜尋內容 (Search Content):", placeholder="輸入關鍵字或 #ID")

        if query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            search_terms = multi_lang_search(query)
            results = [c for c in all_cases if any(t in c.get('title','').lower() or t in path_map.get(c.get('section_id'),"").lower() for t in search_terms) or (query.strip('#') == str(c.get('id','')))]
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個案例")
                for item in results:
                    cid, author = str(item.get('id')), user_map.get(item.get('created_by'), f"User_{item.get('created_by')}")
                    with st.container():
                        st.markdown(f'<span style="font-size:12px; color:#8b949e !important;">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small style="color:#8b949e">(#{cid})</small> <span class="author-tag">👤 {author}</span></div>', unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                        
                        with st.expander("🔽 查看測試步驟"):
                            raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or item.get('steps')
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    step_txt = clean_html_and_add_numbers(s.get('content', s.get('step', '')))
                                    exp_txt = clean_html_and_add_numbers(s.get('expected', ''))
                                    st.markdown(f"""
                                        <div class="step-item">
                                            <span style="color:#79c0ff; font-weight:800;">Step {i}:</span>
                                            <div class="step-content-box">{step_txt}</div>
                                            <div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div>
                                            <div class="step-content-box" style="border-left: 2px solid #4CAF50;">{exp_txt}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info("無步驟資料。")
                        st.markdown("---")
            else:
                st.warning("查無搜尋結果，請嘗試其他關鍵字。")
    else:
        # 如果 all_cases 是 None，代表 fetch 過程出錯
        data_container.error(f"❌ 數據同步失敗！錯誤訊息：{path_map}") # 在這種情況下 path_map 存的是錯誤訊息字串
else:
    st.warning("👈 請在左側輸入連線資訊開始使用。")
