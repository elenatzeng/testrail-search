import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 三語語意聯想字典 ---
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

# --- 2. 頁面設定與 UI 美化 (配色強化版) ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 1. 背景改為深黑色實體漸層，確保基調穩定 */
    .stApp { background-color: #0d1117; background-image: linear-gradient(180deg, #0d1117 0%, #161b22 100%); }
    
    /* 2. 作者標籤：加強邊框與背景對比度 */
    .author-tag { 
        font-size: 11px; color: #4CAF50; background: rgba(76, 175, 80, 0.15); 
        padding: 2px 10px; border-radius: 12px; margin-left: 8px; border: 1px solid rgba(76, 175, 80, 0.4);
        display: inline-block; vertical-align: middle;
    }
    
    /* 3. 按鈕：使用更鮮豔的綠色 */
    .view-btn {
        display: inline-block; padding: 6px 16px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .view-btn:hover { background-color: #2ea043; }

    /* 4. 標題與路徑：調亮文字顏色 */
    .row-text { font-size: 16px; color: #f0f6fc; font-weight: 600; }
    .section-path { font-size: 12px; color: #8b949e; display: block; margin-bottom: 6px; }
    
    /* 5. 核心修正：步驟區塊改用實體深色，徹底解決「灰髒感」 */
    .step-item { 
        background: #1c2128; /* 深灰藍實色背景 */
        padding: 15px; 
        border-radius: 10px; 
        margin-bottom: 12px; 
        border-left: 5px solid #4CAF50; /* 亮綠色側邊條 */
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    /* 步驟文字：調高對比度 */
    .step-item b { color: #58a6ff; font-size: 14px; } /* Step 標題改為亮藍色 */
    .step-content { color: #e6edf3; font-size: 14px; margin-top: 4px; }
    .step-exp { 
        color: #8b949e; font-size: 13px; margin-top: 8px; 
        padding-top: 8px; border-top: 1px solid #30363d; 
    }

    .eng-sub { font-size: 12px; color: #8b949e; margin-top: -10px; margin-bottom: 10px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 讀取網址參數 (Query Params Logic) ---
q = st.query_params
init_url = q.get("url", st.secrets.get("TR_URL", ""))
init_user = q.get("user", st.secrets.get("TR_USER", ""))
init_pw = q.get("pw", st.secrets.get("TR_PW", ""))
init_pid = int(q.get("pid", st.secrets.get("PROJECT_ID", 1)))
init_sid = int(q.get("sid", st.secrets.get("SUITE_ID", 1)))

# --- 4. 側邊欄：連線設定 ---
with st.sidebar:
    st.header("🔐 連線設定")
    st.caption("Connection Settings")

    tr_url = st.text_input("TestRail URL", value=init_url, placeholder="https://xxx.testrail.io")
    tr_user = st.text_input("帳號 Email", value=init_user)
    tr_pw = st.text_input("API Key", type="password", value=init_pw)
    project_id = st.number_input("Project ID", value=init_pid)
    suite_id = st.number_input("Suite ID", value=init_sid)
    
    st.markdown("---")
    
    if st.button("💾 儲存資訊至網址 (Save to URL)"):
        st.query_params.update(
            url=tr_url, 
            user=tr_user, 
            pw=tr_pw, 
            pid=str(project_id), 
            sid=str(suite_id)
        )
        st.success("✅ 已更新網址列！現在請將此頁存為「書籤」。")
        st.balloons()

    if st.button("🔄 強制更新數據 (Force Update)"):
        st.cache_data.clear()
        st.rerun()

# --- 5. 核心數據抓取 ---
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

# --- 6. 主介面 ---
st.title("🧪 TestRail 智能檢索中心")
st.markdown('<span class="eng-sub">TestRail Intelligent Search Center</span>', unsafe_allow_html=True)

if tr_url and tr_user and tr_pw:
    st.markdown("##### 🔍 支援繁體、簡體、英文搜尋")
    st.markdown('<span class="eng-sub">Supports Traditional Chinese, Simplified Chinese, and English</span>', unsafe_allow_html=True)
    
    query = st.text_input("搜尋內容 (Search Content):", placeholder="e.g. 登入, 提现, #30864")

    if query:
        with st.spinner("🚀 同步數據中 (Syncing Data)..."):
            all_cases, path_map, user_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.caption(f"⚡ 最後同步時間 (Last Sync): {sync_time}")
            search_terms = multi_lang_search(query)
            results = []

            for c in all_cases:
                created_id = c.get('created_by')
                author_name = user_map.get(created_id, f"User_{created_id}")
                steps = c.get('custom_steps') or c.get('steps') or c.get('custom_steps_separated') or "No data"
                case_id = str(c.get('id', ''))
                title = c.get('title', '')
                path = path_map.get(c.get('section_id'), "Unknown")
                
                if any(t in title.lower() or t in path.lower() for t in search_terms) or \
                   (query.strip('#').isdigit() and query.strip('#') == case_id):
                    results.append({'id': case_id, 'title': title, 'path': path, 'steps': steps, 'author': author_name})
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個案例 (Found {len(results)} cases)")
                for item in results:
                    with st.container():
                        st.markdown(f'<span class="section-path">{item["path"]}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'''<div class="row-text"><b>{item["title"]}</b> <small>(#{item["id"]})</small><span class="author-tag">👤 {item["author"]}</span></div>''', unsafe_allow_html=True)
                        with col_b:
                            case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{item['id']}"
                            st.markdown(f'<div style="text-align:right;"><a href="{case_url}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                        
                        with st.expander("🔽 查看測試步驟 (View Test Steps)"):
                            raw_steps = item['steps']
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    st.markdown(f"""
                                        <div class="step-item">
                                            <b>Step {i}:</b>
                                            <div class="step-content">{s.get('content', s.get('step', ''))}</div>
                                            <div class="step-exp"><i>Expected:</i> {s.get('expected', '')}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.text_area(label=f"Details (#{item['id']})", value=str(raw_steps), height=100, disabled=True, key=f"area_{item['id']}")
                        st.markdown("---")
            else:
                st.info("查無結果 (No results found).")
        else:
            st.error(f"❌ 錯誤 (Error): {path_map}")
else:
    st.warning("👈 請在左側輸入連線資訊 (Please enter connection info on the left).")
