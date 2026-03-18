import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 搜尋邏輯與 UI 設定 ---
def multi_lang_search(text):
    dictionary = [
        ["登入", "登录", "login", "auth"],
        ["註冊", "注册", "register", "signup"],
        ["提現", "提现", "withdraw", "payout"],
        ["帳號", "账号", "account", "user"],
        ["錢包", "钱包", "wallet", "balance"]
    ]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

# --- 2. 側邊欄：讀取與儲存網址參數 (含 API Key) ---
with st.sidebar:
    st.header("🔐 連線設定")
    st.caption("Connection Settings")

    # 取得網址參數
    query_params = st.query_params

    # 讀取順序：網址參數 > Secrets > 預設值
    default_url = query_params.get("url", st.secrets.get("TR_URL", ""))
    default_user = query_params.get("user", st.secrets.get("TR_USER", ""))
    default_pw = query_params.get("pw", st.secrets.get("TR_PW", ""))
    default_pid = query_params.get("pid", str(st.secrets.get("PROJECT_ID", 1)))
    default_sid = query_params.get("sid", str(st.secrets.get("SUITE_ID", 1)))
    
    tr_url = st.text_input("TestRail URL", value=default_url)
    tr_user = st.text_input("帳號 Email", value=default_user)
    tr_pw = st.text_input("API Key", type="password", value=default_pw)
    project_id = st.number_input("Project ID", value=int(default_pid))
    suite_id = st.number_input("Suite ID", value=int(default_sid))
    
    st.markdown("---")
    # 儲存按鈕：把所有資訊塞進網址
    if st.button("💾 儲存所有資訊至網址 (Save All to URL)"):
        st.query_params.update(
            url=tr_url, 
            user=tr_user, 
            pw=tr_pw, 
            pid=project_id, 
            sid=suite_id
        )
        st.success("✅ 已儲存！請將目前的「網址」加入瀏覽器書籤。")
        st.caption("Done! Please bookmark this current URL.")

    if st.button("🔄 強制更新數據 (Force Update)"):
        st.cache_data.clear()
        st.rerun()

# --- 3. 核心數據抓取 ---
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        clean_url = _url.split('/index.php')[0].strip('/')
        api = TestRailAPI(clean_url, _user, _pw)
        
        # 作者對照表
        u_map = {2: "Elena", 3: "Esther", 4: "Emma", 5: "Baron", 6: "Meh", 8: "Copper", 11: "Katty"}
        try:
            users = api.users.get_users()
            for u in users: u_map[u['id']] = u['name']
        except: pass

        # 抓取 Sections
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
        
        # 抓取 Cases
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

# --- 4. 主介面 (中英雙語) ---
st.title("🧪 TestRail 智能檢索中心")
st.markdown("##### 🔍 支援繁體、簡體、英文搜尋 (Supports Traditional/Simplified/English)")

if tr_url and tr_user and tr_pw:
    query = st.text_input("搜尋內容 (Search Content):", placeholder="e.g. 登入, 提现, #30864")

    if query:
        with st.spinner("🚀 同步數據中 (Syncing)..."):
            all_cases, path_map, user_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.caption(f"⚡ 最後同步 (Last Sync): {sync_time}")
            search_terms = multi_lang_search(query)
            results = []
            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '')
                sid = c.get('section_id')
                author = user_map.get(c.get('created_by'), f"User_{c.get('created_by')}")
                
                if any(t in title.lower() or t in path_map.get(sid, "").lower() for t in search_terms) or (query.strip('#') == cid):
                    results.append({'id': cid, 'title': title, 'path': path_map.get(sid, "Unknown"), 'steps': c.get('custom_steps') or c.get('steps') or "No data", 'author': author})
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個案例")
                for item in results:
                    with st.container():
                        st.markdown(f'<p style="color:#8b949e; font-size:11px; margin-bottom:0;">{item["path"]}</p>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1.5])
                        with col_t:
                            st.markdown(f'<b>{item["title"]}</b> <small>(#{item["id"]})</small> <span style="color:#4CAF50; background:rgba(76,175,80,0.1); padding:2px 8px; border-radius:10px; font-size:11px;">👤 {item["author"]}</span>', unsafe_allow_html=True)
                        with col_b:
                            st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{item["id"]}" target="_blank" style="background:#238636; color:white; padding:5px 10px; border-radius:6px; text-decoration:none; font-size:12px;">📖 Open Case</a></div>', unsafe_allow_html=True)
                        with st.expander("🔽 查看步驟 (Steps)"):
                            # 步驟顯示優化
                            raw_steps = item['steps']
                            if isinstance(raw_steps, list):
                                for i, s in enumerate(raw_steps, 1):
                                    st.write(f"**Step {i}:** {s.get('content', '')}")
                                    st.write(f"*Expected:* {s.get('expected', '')}")
                            else:
                                st.text_area(label=f"Details #{item['id']}", value=str(raw_steps), height=100, disabled=True, key=f"area_{item['id']}")
                        st.markdown("---")
            else:
                st.info("查無結果 (No results found).")
else:
    st.warning("👈 請填寫連線資訊 (Please enter connection info).")
