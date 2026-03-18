import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 三語語意聯想字典 ---
def multi_lang_search(text):
    """
    支援 繁/簡/英 常用測試詞彙的對照搜尋。
    當輸入其中一種，會關聯出該組內的所有詞。
    """
    dictionary = [
        ["登入", "登录", "login", "auth", "sign in"],
        ["註冊", "注册", "register", "signup", "create account"],
        ["提現", "提现", "withdraw", "payout", "cash out"],
        ["帳號", "账号", "account", "user", "profile"],
        ["設定", "设置", "settings", "config", "setup"],
        ["資料", "数据", "data", "info", "record"],
        ["確認", "确认", "confirm", "ok", "submit"],
        ["驗證", "验证", "verify", "verification", "otp", "captcha"],
        ["首提", "首次提现", "first withdraw", "first payout"],
        ["訂單", "订单", "order", "transaction", "history"],
        ["錢包", "钱包", "wallet", "balance", "balance info"]
    ]
    
    text_lower = text.lower().strip()
    related_words = [text_lower]
    
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
            
    return list(set(related_words))

# --- 2. 頁面介面設定與 CSS 美化 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); }
    
    /* 搜尋結果卡片化 */
    div[data-testid="stVerticalBlock"] > div:has(div.row-text) {
        background-color: rgba(255, 255, 255, 0.04);
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
        transition: 0.3s;
    }
    div[data-testid="stVerticalBlock"] > div:has(div.row-text):hover {
        background-color: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
    }

    .row-text { font-size: 15px; color: #e6edf3; line-height: 1.6; }
    .section-path { font-size: 12px; color: #8b949e; margin-bottom: 4px; display: block; }
    
    .view-btn {
        display: inline-block; padding: 8px 18px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none;
        font-size: 13px; font-weight: 600;
    }
    .view-btn:hover { background-color: #2ea043; box-shadow: 0 0 10px rgba(46, 160, 67, 0.4); }

    .table-header {
        background-color: rgba(255, 255, 255, 0.08); padding: 12px; border-radius: 8px;
        font-weight: 700; margin-bottom: 15px; display: flex; color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄：自動讀取 Secrets ---
with st.sidebar:
    st.header("🔐 連線設定")
    
    # 從 Secrets 讀取 (若無則留空)
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
    
    st.markdown("---")
    if st.button("🔄 強制重新同步"):
        st.cache_data.clear()
        st.rerun()

# --- 4. 核心快取數據抓取 ---
@st.cache_data(show_spinner=False, ttl=300)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url, _user, _pw)
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
            
        return all_cases, path_map, time.strftime("%H:%M:%S")
    except Exception as e:
        return None, str(e), None

# --- 5. 主介面搜尋邏輯 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    query = st.text_input("🔍 請輸入關鍵字 (支援繁/簡/英/ID)：")

    if query:
        with st.spinner("🚀 正在檢索數據..."):
            all_cases, path_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.caption(f"⚡ 最後同步時間: {sync_time} (5分鐘內自動快取)")
            
            # 關鍵字擴展
            search_terms = multi_lang_search(query)
            results = []

            for c in all_cases:
                # 確保安全取得欄位內容
                case_id = str(c.get('id', ''))
                title = c.get('title', '')
                section_id = c.get('section_id')
                path = path_map.get(section_id, "Unknown")
                
                title_l = title.lower()
                path_l = path.lower()
                clean_q = query.strip('#')

                # 比對邏輯
                is_text_match = any(term in title_l or term in path_l for term in search_terms)
                is_id_match = clean_q.isdigit() and clean_q == case_id
                
                if is_text_match or is_id_match:
                    results.append({'id': case_id, 'title': title, 'path': path})
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個相關案例")
                st.markdown('<div class="table-header"><div style="flex: 3;">📂 模組路徑</div><div style="flex: 4;">📝 案例標題</div><div style="flex: 1; text-align: center;">操作</div></div>', unsafe_allow_html=True)
                
                for item in results:
                    case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{item['id']}"
                    col1, col2, col3 = st.columns([3, 4, 1])
                    with col1:
                        st.markdown(f'<div class="row-text"><span class="section-path">{item["path"]}</span></div>', unsafe_allow_html=True)
                    with col2:
                        st.markdown(f'<div class="row-text"><b>{item["title"]}</b> <small>(#{item['id']})</small></div>', unsafe_allow_html=True)
                    with col3:
                        st.markdown(f'<div style="text-align:center;"><a href="{case_url}" target="_blank" class="view-btn">📖 查看</a></div>', unsafe_allow_html=True)
            else:
                st.info("查無結果。")
        else:
            st.error(f"❌ 無法連線至 TestRail，錯誤: {path_map}")
else:
    st.warning("👈 請在左側輸入連線資訊開始搜尋。")
