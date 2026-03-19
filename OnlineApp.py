import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# --- 1. 工具函式：掃除 HTML，保留標準換行 ---
def clean_html_basic(raw_html):
    if not raw_html: return ""
    text = str(raw_html)
    # 將 br 標籤轉為換行
    text = re.sub(r'<(br\s*/?)>', '\n', text)
    # 掃除其餘標籤
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    # 處理符號
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    return text.strip()

# --- 2. 三語搜尋字典 ---
def multi_lang_search(text):
    dictionary = [
        ["登入", "登录", "login", "auth"], ["註冊", "注册", "register"],
        ["提現", "提现", "withdraw"], ["帳號", "账号", "account"],
        ["錢包", "钱包", "wallet"], ["訂單", "订单", "order"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 3. UI 視覺風格：鎖定 Dark Mode ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    /* 強制全域深色背景鎖定 */
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0b0e14 !important;
    }
    header[data-testid="stHeader"] { visibility: hidden; }

    /* 側邊欄按鈕強化 */
    div[data-testid="stSidebar"] .stButton button {
        background-color: #21262d !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        width: 100% !important;
        height: 45px !important;
        font-weight: bold !important;
    }
    
    /* 文字與輸入框顏色 */
    h1, h2, h3, h4, h5, p, span, label, small { color: #ffffff !important; }
    .stTextInput input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
    }

    /* ✨【條列式核心修復】✨ */
    .step-content-box {
        color: #ffffff !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
        white-space: pre-wrap !important; /* 保留換行 */
        background: #1c2128;
        padding: 15px;
        border-radius: 10px;
        margin-top: 5px;
        border: 1px solid #30363d;
        font-family: "Segoe UI", Tahoma, sans-serif !important;
    }
    
    /* 人工條列式樣式 (1., 2., 3.) */
    .numbered-list {
        margin: 0; padding: 0; list-style: none;
    }
    .numbered-list li {
        position: relative;
        padding-left: 30px; /* 給數字留空間 */
        margin-bottom: 10px;
    }
    .numbered-list li::before {
        content: counter(item) ". ";
        counter-increment: item;
        position: absolute;
        left: 0;
        color: #79c0ff; /* 數字顏色 */
        font-weight: bold;
    }
    .numbered-list { counter-reset: item; }

    .step-item { 
        border-left: 5px solid #4CAF50;
        padding-left: 20px;
        margin-bottom: 25px;
    }
    .location-tag {
        background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; 
        font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px;
    }
    .author-tag { font-size: 11px; color: #4CAF50 !important; background: rgba(76, 175, 80, 0.15); border-radius: 12px; padding: 3px 12px; border: 1.5px solid #4CAF50; }
    .view-btn { display: inline-block; padding: 6px 16px; background-color: #238636; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 參數處理 ---
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
        st.success("✅ 已儲存！")
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
        query = st.text_input("搜尋內容:", placeholder="請輸入關鍵字（支援繁簡英）或 #ID")

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
                                    # ✨核心修復：清理 HTML，並使用 split('\n') 將內容切成陣列
                                    content_raw = clean_html_basic(s.get('content', s.get('step', '')))
                                    expected_raw = clean_html_basic(s.get('expected', ''))
                                    
                                    # 將內容按換行符切開，移除空行
                                    content_lines = [line for line in content_raw.split('\n') if line.strip()]
                                    expected_lines = [line for line in expected_raw.split('\n') if line.strip()]
                                    
                                    # 人工組裝條列式 HTML
                                    content_html = "<ol class='numbered-list'>" + "".join([f"li>{line}</li>" for line in content_lines]) + "</ol>"
                                    expected_html = "<ol class='numbered-list'>" + "".join([f"li>{line}</li>" for line in expected_lines]) + "</ol>"

                                    st.markdown(f"""
                                        <div class="step-item">
                                            <span style="color:#79c0ff; font-weight:800;">Step {i}:</span>
                                            <div class="step-content-box">{content_html}</div>
                                            <div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div>
                                            <div class="step-content-box" style="border-left: 2px solid #30363d;">{expected_html}</div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            elif isinstance(raw_steps, str) and raw_steps.strip():
                                st.markdown(f'<div class="step-content-box">{clean_html_basic(raw_steps)}</div>', unsafe_allow_html=True)
                            else:
                                st.info("無步驟資料。")
                    st.markdown("---")
else:
    st.warning("👈 請輸入連線資訊。")
