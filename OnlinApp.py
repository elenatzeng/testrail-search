import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 繁簡轉換 ---
def cc_convert(text):
    mapping = {
        "登入": "登录", "登录": "登入", "註冊": "注册", "注册": "註冊",
        "帳號": "账号", "账号": "帳號", "提現": "提现", "提现": "提現",
        "資料": "数据", "数据": "資料", "設定": "设置", "设置": "設定"
    }
    return mapping.get(text, text)

# --- 2. 頁面介面設定 ---
st.set_page_config(page_title="TestRail Search Cloud", layout="wide", page_icon="🔍")
st.markdown("""
    <style>
    .view-btn { display: inline-block; padding: 6px 14px; background-color: #4CAF50; color: white !important; border-radius: 4px; text-decoration: none; font-size: 12px; font-weight: bold; }
    .row-text { font-size: 14px; color: #e0e0e0; }
    .section-path { font-size: 11px; color: #888; }
    .table-header { background-color: rgba(255, 255, 255, 0.1); padding: 12px; border-radius: 5px; font-weight: bold; margin-bottom: 10px; display: flex; border-left: 5px solid #4CAF50; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄：連線資訊 (雲端版不存檔) ---
with st.sidebar:
    st.header("🔑 TestRail 連線")
    tr_url = st.text_input("URL", placeholder="https://xxx.testrail.io/")
    tr_user = st.text_input("Email")
    tr_pw = st.text_input("API Key / Password", type="password")
    project_id = st.number_input("Project ID", value=1, step=1)
    suite_id = st.number_input("Suite ID", value=1, step=1)
    
    st.info("💡 為了資安，網頁不會儲存您的密碼。重新整理網頁後需重新輸入。")
    
    if st.button("🔄 重新整理資料"):
        st.cache_data.clear()
        st.rerun()

# --- 4. 核心快取邏輯 ---
@st.cache_data(show_spinner=False, ttl=300)
def fetch_data(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url, _user, _pw)
        # 抓模組
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
        
        # 抓案例
        all_cases = []
        c_off = 0
        while True:
            c_resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=c_off)
            c_batch = c_resp['cases'] if isinstance(c_resp, dict) and 'cases' in c_resp else c_resp
            if not c_batch: break
            all_cases.extend(c_batch)
            if len(c_batch) < 250: break
            c_off += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S")
    except Exception as e:
        return None, str(e), None

# --- 5. 主介面 ---
st.title("📚 TestRail 雲端檢索工具")

if tr_url and tr_user and tr_pw:
    query = st.text_input("🔍 搜尋標題、路徑或 ID：")
    if query:
        with st.spinner("正在同步 TestRail..."):
            all_cases, path_map, sync_time = fetch_data(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.write(f"⚡ 資料同步時間: {sync_time}")
            q_orig = query.lower()
            q_conv = cc_convert(q_orig)
            results = []
            for c in all_cases:
                path = path_map.get(c['section_id'], "Unknown")
                title = c['title'].lower()
                if q_orig in title or q_orig in path.lower() or q_conv in title or q_conv in path.lower() or query.strip('#') == str(c['id']):
                    results.append({'id': c['id'], 'title': c['title'], 'path': path})
            
            if results:
                st.markdown('<div class="table-header"><div style="flex: 3;">模組路徑</div><div style="flex: 4;">案例標題</div><div style="flex: 1; text-align: center;">查看</div></div>', unsafe_allow_html=True)
                for item in results:
                    case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{item['id']}"
                    col1, col2, col3 = st.columns([3, 4, 1])
                    with col1: st.markdown(f'<div class="row-text">{item["path"]}</div>', unsafe_allow_html=True)
                    with col2: st.markdown(f'<div class="row-text"><b>{item["title"]}</b></div>', unsafe_allow_html=True)
                    with col3: st.markdown(f'<div style="text-align:center;"><a href="{case_url}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
            else:
                st.info("查無結果。")
else:
    st.warning("👈 請在左側輸入 TestRail 連線資訊。")