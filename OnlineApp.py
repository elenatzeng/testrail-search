import streamlit as st
from testrail_api import TestRailAPI
import time
import re

# --- 1. 工具函式：修復條列式並自動補上數字 ---
def clean_html_and_add_numbers(raw_html):
    if not raw_html: return ""
    text = str(raw_html)
    
    # 步驟 A: 將 <li> 標籤先換成一個特殊的換行符號，方便後續切割
    text = text.replace('<li>', '\n')
    text = re.sub(r'<(br\s*/?|/div|/p|/li)>', '\n', text) 
    
    # 步驟 B: 掃除所有 HTML 標籤
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    
    # 步驟 C: 處理特殊符號
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 步驟 D: 重新組裝數字條列 (這是最關鍵的一步！)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    numbered_lines = []
    for index, line in enumerate(lines, 1):
        # 如果妳原本就有手打數字，就不要重複加；如果沒手打，我們幫妳加上 1. 2. 3.
        if not re.match(r'^\d+\.', line):
            numbered_lines.append(f"{index}. {line}")
        else:
            numbered_lines.append(line)
            
    return "\n".join(numbered_lines)

# --- 2. 搜尋字典 ---
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

# --- 3. UI 視覺風格：鎖定深色模式 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
        background-color: #0b0e14 !important;
    }
    header[data-testid="stHeader"] { visibility: hidden; }

    /* 側邊欄按鈕強化 (亮色按鈕 + 黑字) */
    div[data-testid="stSidebar"] .stButton button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        width: 100% !important;
        height: 45px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stSidebar"] .stButton button p { color: #000000 !important; }

    /* 步驟顯示區塊：保留換行 */
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
    
    h1, h2, h3, h4, h5, p, span, label, small { color: #ffffff !important; }
    .stTextInput input { background-color: #161b22 !important; color: #ffffff !important; border: 1px solid #30363d !important; }
    .location-tag { background: #1c2128 !important; color: #adbac7 !important; padding: 10px 20px; border-radius: 10px; font-size: 15px; border: 1px solid #444c56; display: inline-block; margin-bottom: 25px; }
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
    if st.button("💾 儲存至網址"):
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
                                # ✨核心修復：使用 clean_html_and_add_numbers 自動補上數字
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
