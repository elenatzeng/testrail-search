import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# --- 1. 工具函式 ---
def clean_html(raw_html):
    if not raw_html: return ""
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', str(raw_html))
    cleantext = cleantext.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return cleantext.strip()

# --- 2. 三語聯想搜尋字典 ---
def multi_lang_search(text):
    dictionary = [
        ["登入", "登录", "login", "auth", "sign in"],
        ["註冊", "注册", "register", "signup"],
        ["提現", "提现", "withdraw", "payout"],
        ["帳號", "账号", "account", "user"],
        ["錢包", "钱包", "wallet", "balance"],
        ["訂單", "订单", "order", "history"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 3. UI 視覺風格：徹底解決按鈕看不見的問題 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 1. 全域背景染黑 */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0b0e14 !important;
    }

    /* 2. 側邊欄按鈕：改用「深灰色背景」，讓原本的白字顯示出來 */
    div[data-testid="stSidebar"] .stButton button {
        background-color: #21262d !important; /* GitHub 經典深灰色 */
        color: #ffffff !important;           /* 強制白色文字 */
        border: 1px solid #30363d !important;
        width: 100%;
        height: 45px;
        border-radius: 8px !important;
    }
    
    /* 3. 強力覆蓋按鈕內文字顏色與透明度 */
    div[data-testid="stSidebar"] .stButton button p,
    div[data-testid="stSidebar"] .stButton button span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* 4. 輸入框與標籤文字提亮 */
    .stTextInput input, .stNumberInput input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }
    .stMarkdown, p, span, label, h1, h2, h3, h4, h5 {
        color: #ffffff !important;
    }
    
    /* 5. 位置標籤 (Status Bar) */
    .location-tag {
        background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; 
        font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px;
    }

    .author-tag { 
        font-size: 11px; color: #4CAF50 !important; background: rgba(76, 175, 80, 0.15); 
        padding: 3px 12px; border-radius: 12px; margin-left: 8px; border: 1.5px solid #4CAF50;
        display: inline-block; vertical-align: middle;
    }

    .view-btn {
        display: inline-block; padding: 6px 16px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold;
    }

    .step-item { 
        background: #161b22 !important; padding: 18px; border-radius: 10px; margin-bottom: 15px; 
        border-left: 6px solid #4CAF50; border: 1px solid #30363d;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 讀取與儲存參數 ---
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
    if st.button("💾 儲存資訊至網址 (Save to URL)"):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=str(project_id), sid=str(suite_id))
        st.success("✅ 已儲存！")
        st.balloons()
    if st.button("🔄 強制更新數據 (Force Sync)"):
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
        st.markdown(f"""
            <div class="location-tag">
                📍 <b>Project：</b><span style="color:#58a6ff; font-weight:bold;">{project_name}</span> 
                <span style="color:#444c56; margin: 0 10px;">|</span> 
                <b>Suite：</b>#{suite_id}
            </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🔍 支援繁體 / 簡體 / 英文 跨語言搜尋")
        query = st.text_input("搜尋內容 (Search Content):", placeholder="請輸入關鍵字或 #ID")

        if query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            search_terms = multi_lang_search(query)
            results = [c for c in all_cases if any(t in c.get('title','').lower() or t in path_map.get(c.get('section_id'),"").lower() for t in search_terms) or (query.strip('#') == str(c.get('id','')))]
            
            for item in results:
                cid, author = str(item.get('id')), user_map.get(item.get('created_by'), f"ID_{item.get('created_by')}")
                with st.container():
                    st.markdown(f'<span style="font-size:12px; color:#8b949e !important;">{path_map.get(item.get("section_id"), "Unknown")}</span>', unsafe_allow_html=True)
                    col_t, col_b = st.columns([7, 1.5])
                    with col_t:
                        st.markdown(f'<div style="font-size:16px; color:#ffffff !important; font-weight:bold;">{item.get("title")} <small style="color:#8b949e">(#{cid})</small> <span class="author-tag">👤 {author}</span></div>', unsafe_allow_html=True)
                    with col_b:
                        st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    with st.expander("🔽 查看測試步驟"):
                        raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or item.get('steps')
                        if isinstance(raw_steps, list) and len(raw_steps) > 0:
                            for i, s in enumerate(raw_steps, 1):
                                st.markdown(f"""<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div style="color:white;">{clean_html(s.get('content', s.get('step', '')))}</div><div style="color:#c9d1d9; font-size:14px; margin-top:10px; padding-top:10px; border-top:1px solid #30363d;"><span style="color:#8b949e; font-weight:bold;">Expected:</span>{clean_html(s.get('expected', ''))}</div></div>""", unsafe_allow_html=True)
                        elif isinstance(raw_steps, str) and raw_steps.strip():
                            st.markdown(f"""<div class="step-item"><div style="color:white;">{clean_html(raw_steps)}</div></div>""", unsafe_allow_html=True)
                        else:
                            st.info("無步驟資料。")
                    st.markdown("---")
else:
    st.warning("👈 請輸入連線資訊。")
