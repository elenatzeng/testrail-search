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
        ["錢包", "钱包", "wallet", "balance"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

# --- 2. 頁面介面與 CSS 美化 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); }
    .author-tag { 
        font-size: 11px; color: #4CAF50; background: rgba(76, 175, 80, 0.1); 
        padding: 2px 10px; border-radius: 12px; margin-left: 8px; border: 1px solid rgba(76, 175, 80, 0.3);
    }
    .view-btn {
        display: inline-block; padding: 6px 16px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600;
    }
    .row-text { font-size: 15px; color: #e6edf3; }
    .section-path { font-size: 11px; color: #8b949e; display: block; margin-bottom: 4px; }
    .step-item { background: rgba(0,0,0,0.2); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #8b949e; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄 ---
with st.sidebar:
    st.header("🔐 連線設定")
    sec_url = st.secrets.get("TR_URL", "")
    sec_user = st.secrets.get("TR_USER", "")
    sec_pw = st.secrets.get("TR_PW", "")
    sec_pid = st.secrets.get("PROJECT_ID", 1)
    sec_sid = st.secrets.get("SUITE_ID", 1)

    tr_url = st.text_input("TestRail URL", value=sec_url)
    tr_user = st.text_input("帳號 (Email)", value=sec_user)
    tr_pw = st.text_input("API Key", type="password", value=sec_pw)
    project_id = st.number_input("Project ID", value=int(sec_pid))
    suite_id = st.number_input("Suite ID", value=int(sec_sid))
    
    if st.button("🔄 強制更新數據"):
        st.cache_data.clear()
        st.rerun()

# --- 4. 數據抓取 (已手動餵食 User 清單) ---
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        clean_url = _url.split('/index.php')[0].strip('/')
        api = TestRailAPI(clean_url, _user, _pw)
        
        # --- 這裡餵食了你提供的名單 ---
        u_map = {
            2: "Elena",
            3: "Esther",
            4: "Emma",
            5: "Baron",
            6: "Katty",
            8: "Copper"
        }
        
        # 嘗試自動抓取補充其餘成員
        try:
            api_users = api.users.get_users()
            for u in api_users:
                u_map[u['id']] = u['name']
        except: pass

        # 抓取模組
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
        
        # 抓取案例
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

# --- 5. 主介面 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    query = st.text_input("🔍 輸入關鍵字：", placeholder="搜尋功能、標題、ID 或作者...")

    if query:
        with st.spinner("🚀 同步數據中..."):
            all_cases, path_map, user_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.caption(f"⚡ 同步時間: {sync_time}")
            search_terms = multi_lang_search(query)
            results = []

            for c in all_cases:
                created_id = c.get('created_by')
                # 自動對照名單
                author_name = user_map.get(created_id, f"User_{created_id}")
                
                steps = c.get('custom_steps') or c.get('steps') or c.get('custom_steps_separated') or "無詳細步驟"
                case_id = str(c.get('id', ''))
                title = c.get('title', '')
                path = path_map.get(c.get('section_id'), "Unknown")
                
                # 搜尋邏輯：支援作者搜尋
                if any(t in title.lower() or t in path.lower() or t in author_name.lower() for t in search_terms) or \
                   (query.strip('#').isdigit() and query.strip('#') == case_id):
                    results.append({'id': case_id, 'title': title, 'path': path, 'steps': steps, 'author': author_name})
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個相關案例")
                for item in results:
                    with st.container():
                        st.markdown(f'<span class="section-path">{item["path"]}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1])
                        with col_t:
                            st.markdown(f'''
                                <div class="row-text">
                                    <b>{item["title"]}</b> <small>(#{item["id"]})</small>
                                    <span class="author-tag">👤 Created by: {item["author"]}</span>
                                </div>
                            ''', unsafe_allow_html=True)
                        with col_b:
                            case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{item['id']}"
                            st.markdown(f'<div style="text-align:right;"><a href="{case_url}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                        
                        with st.expander("🔽 查看測試步驟"):
                            raw_steps = item['steps']
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    st.markdown(f"""<div class="step-item">
                                        <b>Step {i}:</b> {s.get('content', s.get('step', ''))}<br>
                                        <i>Expected:</i> {s.get('expected', '')}
                                    </div>""", unsafe_allow_html=True)
                            else:
                                st.text_area(f"Details #{item['id']}", value=str(raw_steps), height=100, disabled=True, key=f"t_{item['id']}")
                        st.markdown("---")
            else:
                st.info("查無結果。")
        else:
            st.error(f"❌ 無法讀取資料：{path_map}")
else:
    st.warning("👈 請在左側輸入連線資訊開始使用。")
