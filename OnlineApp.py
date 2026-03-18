import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 搜尋邏輯與 UI 設定 (保持不變) ---
def multi_lang_search(text):
    dictionary = [["登入", "登录", "login"], ["註冊", "注册", "register"], ["錢包", "钱包", "wallet"]]
    text_lower = text.lower().strip()
    related_words = [text_lower]
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
    return list(set(related_words))

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

# --- 2. 側邊欄：加入「讀取網址參數」功能 ---
with st.sidebar:
    st.header("🔐 連線設定")
    st.caption("Connection Settings")

    # 取得網址上的參數 (如果有跑掉或沒填，就給空字串)
    query_params = st.query_params

    # 優先級：網址參數 > Secrets > 空字串
    default_url = query_params.get("url", st.secrets.get("TR_URL", ""))
    default_user = query_params.get("user", st.secrets.get("TR_USER", ""))
    
    tr_url = st.text_input("TestRail URL", value=default_url)
    tr_user = st.text_input("帳號 Email", value=default_user)
    
    # 為了安全，密碼(API Key)通常不建議存網址，但如果你想存也可以比照辦理
    tr_pw = st.text_input("API Key", type="password", value=st.secrets.get("TR_PW", ""))
    
    project_id = st.number_input("Project ID", value=int(st.secrets.get("PROJECT_ID", 1)))
    suite_id = st.number_input("Suite ID", value=int(st.secrets.get("SUITE_ID", 1)))

    if st.button("💾 儲存至網址 (Save to URL)"):
        # 將目前的設定寫入網址列
        st.query_params.update(url=tr_url, user=tr_user)
        st.success("已更新網址！請將此頁面加入書籤。 (URL Updated! Please bookmark this page.)")

    if st.button("🔄 強制更新數據 (Force Update)"):
        st.cache_data.clear()
        st.rerun()

# --- 3. 數據抓取與顯示邏輯 (與之前版本一致) ---
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
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
                cid, author = str(c.get('id', '')), user_map.get(c.get('created_by'), f"User_{c.get('created_by')}")
                title, sid = c.get('title', ''), c.get('section_id')
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
                            st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{item["id"]}" target="_blank" style="background:#238636; color:white; padding:5px 10px; border-radius:6px; text-decoration:none; font-size:12px;">📖 Open</a></div>', unsafe_allow_html=True)
                        with st.expander("🔽 查看步驟 (Steps)"):
                            st.write(item['steps'])
                        st.markdown("---")
            else:
                st.info("查無結果 (No results found).")
else:
    st.warning("👈 請填寫連線資訊 (Please enter connection info).")
