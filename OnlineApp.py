import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# --- 1. 核心邏輯：修復條列式數字 (找回 1. 2. 3.) ---
def clean_html_and_add_numbers(raw_html):
    if not raw_html: return ""
    text = str(raw_html)
    # 將 HTML 條列標籤預處理為換行
    text = text.replace('<li>', '\n')
    text = re.sub(r'<(br\s*/?|/div|/p|/li)>', '\n', text) 
    # 清除其餘 HTML 標籤
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    # 處理特殊符號轉義
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 自動補上數字條列 1. 2. 3.
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    numbered_lines = []
    for index, line in enumerate(lines, 1):
        if not re.match(r'^\d+[\.\、]', line):
            numbered_lines.append(f"{index}. {line}")
        else:
            numbered_lines.append(line)
    return "\n".join(numbered_lines)

# --- 2. 三語聯想搜尋字典 (已補上免費旋轉與免費籌碼) ---
def multi_lang_search(text):
    dictionary = [
        ["登入", "登录", "login", "auth", "sign in"],
        ["註冊", "注册", "register", "signup"],
        ["提現", "提现", "withdraw", "payout"],
        ["帳號", "账号", "account", "user"],
        ["錢包", "钱包", "wallet", "balance"],
        ["訂單", "订单", "order", "history"],
        ["免費旋轉", "免费旋转", "free spin"],
        ["免費籌碼", "免费筹码", "free chip"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 3. UI 視覺風格：🏆 究極黑金鎖定版 (物理遮蔽選單) ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 🌑 核心鎖定：強制全域背景深黑色 */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0b0e14 !important;
    }

    /* 🌕 核心鎖定：強制所有文字為白色，防日間模式隱身 */
    h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown {
        color: #ffffff !important;
    }

    /* 🚫 物理遮蔽：隱藏頂部所有選單 (Share, Deploy, 三點點) 🚫 */
    [data-testid="stHeader"], [data-testid="stTopBar"], div[data-testid="stMainMenu"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* 隱藏選單內的日間/夜間切換 Radio 群組 */
    div[role="radiogroup"] {
        display: none !important;
    }

    /* 修正側邊欄箭頭按鈕：確保縮小後能看到白色的展開按鈕 */
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

    /* 步驟顯示區塊 (尊重換行) */
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

    .step-item { 
        border-left: 5px solid #4CAF50;
        padding-left: 20px;
        margin-bottom: 30px;
    }
    
    .stTextInput input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    .location-tag { background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px; }
    .author-tag { font-size: 11px; color: #4CAF50 !important; background: rgba(76, 175, 80, 0.15); border-radius: 12px; padding: 3px 12px; border: 1.5px solid #4CAF50; }
    .view-btn { display: inline-block; padding: 6px 16px; background-color: #238636; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
    
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 參數讀取與儲存 ---
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
        st.success("✅ 已儲存至網址！")
        st.balloons()
    if st.button("🔄 強制更新數據"):
        st.cache_data.clear()
        st.rerun()

# --- 5. 數據抓取 ---
@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
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
        return None, str(e), {}, None, ""

# --- 6. 主介面 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    with st.spinner("🚀 同步數據中..."):
        data = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        all_cases, path_map, user_map, sync_time, project_name = data
    
    if all_cases:
        st.markdown(f'<div class="location-tag">📍 <b>Project：</b><span style="color:#58a6ff; font-weight:bold;">{project_name}</span> | <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        st.markdown("##### 🔍 支援繁體 / 簡體 / 英文 跨語言搜尋")
        query = st.text_input("搜尋內容 (Search Content):", placeholder="請輸入關鍵字（支援繁簡英自動轉換）或 #ID")

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
                        
                        with st.expander("🔽 查看測試步驟 (View Test Steps)"):
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
    st.warning("👈 請在左側輸入連線資訊。")
