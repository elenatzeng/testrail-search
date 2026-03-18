import streamlit as st
from testrail_api import TestRailAPI
import time
import re  # 引入正規表示式，用來清理 HTML 標籤

# --- 1. 工具函式：掃除隱藏的 HTML 格式 (解決字體變灰的核心) ---
def clean_html(raw_html):
    if not raw_html:
        return ""
    # 移除所有 HTML 標籤 (例如 <span style="color:rgb(30,30,30)">)
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    # 處理常見的轉義字元
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&amp;', '&')
    return cleantext.strip()

# --- 2. 三語語意聯想字典 ---
def multi_lang_search(text):
    dictionary = [
        ["登入", "登录", "login", "auth", "sign in"],
        ["註冊", "注册", "register", "signup", "create account"],
        ["提現", "提现", "withdraw", "payout", "cash out"],
        ["帳號", "账号", "account", "user", "profile"],
        ["設定", "设置", "settings", "config", "setup"],
        ["驗證", "验证", "verify", "verification", "otp", "captcha"],
        ["錢包", "钱包", "wallet", "balance"],
        ["訂單", "订单", "order", "transaction", "history"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 3. 頁面設定與 UI 視覺強化 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 全局背景：深黑色確保高對比 */
    .stApp { background-color: #0b0e14; }
    
    /* 作者標籤：亮綠色 */
    .author-tag { 
        font-size: 11px; color: #4CAF50; background: rgba(76, 175, 80, 0.15); 
        padding: 3px 12px; border-radius: 12px; margin-left: 8px; border: 1.5px solid #4CAF50;
        display: inline-block; vertical-align: middle;
    }
    
    /* 按鈕：深綠色背景 */
    .view-btn {
        display: inline-block; padding: 6px 16px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold;
    }

    /* 步驟區塊：解決變灰、看不清楚的核心 CSS */
    .step-item { 
        background: #161b22; /* 穩定的深色背景 */
        padding: 18px; 
        border-radius: 10px; 
        margin-bottom: 15px; 
        border-left: 6px solid #4CAF50; /* 亮綠邊條 */
        border: 1px solid #30363d; /* 細邊框增加層次 */
    }
    
    /* 步驟標題：霓虹藍 */
    .step-title { 
        color: #79c0ff; 
        font-size: 15px; 
        font-weight: 800; 
        margin-bottom: 6px; 
        display: block;
    }
    
    /* 步驟內容：強制純白色 (#FFFFFF) */
    .step-content { 
        color: #ffffff !important; 
        font-size: 15px; 
        font-weight: 500;
        line-height: 1.6;
    }
    
    /* 預期結果：明亮的灰色 */
    .step-exp { 
        color: #c9d1d9; 
        font-size: 14px; 
        margin-top: 10px; 
        padding-top: 10px; 
        border-top: 1px solid #30363d; 
    }
    .exp-label { color: #8b949e; font-weight: bold; margin-right: 5px; }

    .eng-sub { font-size: 12px; color: #8b949e; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 讀取網址參數 (Query Params) ---
q = st.query_params
init_url = q.get("url", st.secrets.get("TR_URL", ""))
init_user = q.get("user", st.secrets.get("TR_USER", ""))
init_pw = q.get("pw", st.secrets.get("TR_PW", ""))
init_pid = int(q.get("pid", st.secrets.get("PROJECT_ID", 1)))
init_sid = int(q.get("sid", st.secrets.get("SUITE_ID", 1)))

# --- 5. 側邊欄 ---
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=init_url)
    tr_user = st.text_input("帳號 Email", value=init_user)
    tr_pw = st.text_input("API Key", type="password", value=init_pw)
    project_id = st.number_input("Project ID", value=init_pid)
    suite_id = st.number_input("Suite ID", value=init_sid)
    st.markdown("---")
    if st.button("💾 儲存資訊至網址 (Save to URL)"):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=str(project_id), sid=str(suite_id))
        st.success("✅ 已儲存！請將此頁存為書籤。")
        st.balloons()
    if st.button("🔄 強制更新數據 (Force Update)"):
        st.cache_data.clear()
        st.rerun()

# --- 6. 核心數據抓取 ---
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        clean_url = _url.split('/index.php')[0].strip('/')
        api = TestRailAPI(clean_url, _user, _pw)
        u_map = {2: "Elena", 3: "Esther", 4: "Emma", 5: "Baron", 6: "Meh", 8: "Copper", 11: "Katty"}
        try:
            users = api.users.get_users()
            for u in users: u_map[u['id']] = u['name']
        except: pass
        
        all_sects = []
        s_off = 0
        while True:
            s_resp = api.sections.get_sections(project_id=pid, suite_id=sid, limit=250, offset=s_off)
            s_batch = s_resp['sections'] if isinstance(s_resp, dict) and 'sections' in s_resp else s_resp
            if not s_batch: break
            all_sects.extend(s_batch)
            if len(s_batch) < 250: break
            s_off += 250
        
        sect_dict = {s['id']: s for s in all_sects}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            name, p_id = curr['name'], curr.get('parent_id')
            return f"{get_path(p_id)} > {name}" if p_id else name
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        all_cases = []
        c_off = 0
        while True:
            c_resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=c_off)
            c_batch = c_resp['cases'] if isinstance(c_resp, dict) and 'cases' in c_resp else c_resp
            if not c_batch: break
            all_cases.extend(c_batch)
            if len(c_batch) < 250: break
            c_off += 250
        return all_cases, path_map, u_map, time.strftime("%H:%M:%S")
    except Exception as e:
        return None, str(e), {}, None

# --- 7. 主介面 ---
st.title("🧪 TestRail 智能檢索中心")
st.markdown('<span class="eng-sub">TestRail Intelligent Search Center</span>', unsafe_allow_html=True)

if tr_url and tr_user and tr_pw:
    st.markdown("##### 🔍 支援繁體、簡體、英文搜尋")
    query = st.text_input("搜尋內容 (Search Content):", placeholder="e.g. 充值, #31757")

    if query:
        with st.spinner("🚀 同步數據中..."):
            all_cases, path_map, user_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        if all_cases:
            search_terms = multi_lang_search(query)
            results = [c for c in all_cases if any(t in c.get('title','').lower() or t in path_map.get(c.get('section_id'),"").lower() for t in search_terms) or (query.strip('#') == str(c.get('id','')))]
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個案例")
                for item in results:
                    cid = str(item.get('id'))
                    author = user_map.get(item.get('created_by'), f"User_{item.get('created_by')}")
                    with st.container():
                        st.markdown(f'<span class="section-path">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'<div style="font-size:16px; color:#ffffff; font-weight:bold;">{item.get("title")} <small>(#{cid})</small> <span class="author-tag">👤 {author}</span></div>', unsafe_allow_html=True)
                        with col_b:
                            case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{cid}"
                            st.markdown(f'<div style="text-align:right;"><a href="{case_url}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                        
                        with st.expander("🔽 查看測試步驟 (View Test Steps)"):
                            steps = item.get('custom_steps') or item.get('steps') or "No Data"
                            if isinstance(steps, list):
                                for i, s in enumerate(steps, 1):
                                    # 關鍵動作：清理掉原始資料中的 HTML 標籤
                                    clean_step = clean_html(s.get('content', s.get('step', '')))
                                    clean_exp = clean_html(s.get('expected', ''))
                                    
                                    st.markdown(f"""
                                        <div class="step-item">
                                            <span class="step-title">Step {i}:</span>
                                            <div class="step-content">{clean_step}</div>
                                            <div class="step-exp"><span class="exp-label">Expected:</span>{clean_exp}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info(clean_html(str(steps)))
                        st.markdown("---")
            else:
                st.info("No results found.")
else:
    st.warning("👈 Please enter connection info.")
