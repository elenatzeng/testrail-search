import streamlit as st
from testrail_api import TestRailAPI
import time

# --- 1. 三語語意聯想字典 (核心搜尋邏輯) ---
def multi_lang_search(text):
    """
    支援 繁/簡/英 常用測試詞彙的對照搜尋。
    """
    dictionary = [
        ["登入", "登录", "login", "auth", "sign in"],
        ["註冊", "注册", "register", "signup", "create account"],
        ["提現", "提现", "withdraw", "payout", "cash out"],
        ["帳號", "账号", "account", "user", "profile"],
        ["設定", "设置", "settings", "config", "setup"],
        ["資料", "数据", "data", "info", "record"],
        ["驗證", "验证", "verify", "verification", "otp", "captcha"],
        ["訂單", "订单", "order", "transaction", "history"],
        ["錢包", "钱包", "wallet", "balance", "balance info"],
        ["首提", "首次提现", "first withdraw", "first payout"]
    ]
    
    text_lower = text.lower().strip()
    related_words = [text_lower]
    
    for group in dictionary:
        if any(word.lower() == text_lower for word in group):
            related_words.extend([g.lower() for g in group])
            
    return list(set(related_words))

# --- 2. 頁面設定與 CSS 美化 ---
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #0e1117 0%, #161b22 100%); }
    
    /* 結果卡片樣式 */
    .result-container {
        background-color: rgba(255, 255, 255, 0.04);
        padding: 15px;
        border-radius: 12px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 15px;
    }
    
    .row-text { font-size: 15px; color: #e6edf3; line-height: 1.6; }
    .section-path { font-size: 12px; color: #8b949e; margin-bottom: 4px; display: block; }
    
    /* 按鈕美化 */
    .view-btn {
        display: inline-block; padding: 6px 16px; background-color: #238636;
        color: white !important; border-radius: 6px; text-decoration: none;
        font-size: 13px; font-weight: 600; transition: 0.2s;
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
    
    # 優先從 Secrets 讀取
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
    # 將快取時間拉長到 1 小時 (3600秒)，搜尋會變快
    if st.button("🔄 強制更新數據 (需等待)"):
        st.cache_data.clear()
        st.rerun()

# --- 4. 核心數據抓取 (含步驟欄位) ---
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url, _user, _pw)
        
        # 抓取模組 (Sections)
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
        
        # 抓取案例 (包含步驟)
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

# --- 5. 主介面搜尋與顯示 ---
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    query = st.text_input("🔍 請輸入關鍵字 (支援繁/簡/英/ID)：", placeholder="例如：login, 提現, #12345")

    if query:
        with st.spinner("🚀 正在從伺服器同步大量數據，請稍候..."):
            all_cases, path_map, sync_time = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
        
        if all_cases:
            st.caption(f"⚡ 最後同步時間: {sync_time} (一小時內自動快取)")
            
            search_terms = multi_lang_search(query)
            results = []

            for c in all_cases:
                case_id = str(c.get('id', ''))
                title = c.get('title', '')
                path = path_map.get(c.get('section_id'), "Unknown")
                
                # 取得測試步驟邏輯
                steps_data = c.get('custom_steps', c.get('custom_steps_separated', "無詳細步驟資料"))
                
                title_l, path_l = title.lower(), path.lower()
                clean_q = query.strip('#')

                if any(t in title_l or t in path_l for t in search_terms) or \
                   (clean_q.isdigit() and clean_q == case_id):
                    results.append({'id': case_id, 'title': title, 'path': path, 'steps': steps_data})
            
            if results:
                st.write(f"### 🎯 找到 {len(results)} 個相關案例")
                st.markdown('<div class="table-header"><div style="flex: 3;">📂 模組路徑</div><div style="flex: 4;">📝 案例標題</div><div style="flex: 1; text-align: center;">操作</div></div>', unsafe_allow_html=True)
                
                for item in results:
                    with st.container():
                        st.markdown(f'<span class="section-path">{item["path"]}</span>', unsafe_allow_html=True)
                        col_t, col_b = st.columns([7, 1])
                        
                        with col_t:
                            st.markdown(f'<div class="row-text"><b>{item["title"]}</b> <small>(#{item["id"]})</small></div>', unsafe_allow_html=True)
                        
                        with col_b:
                            case_url = f"{tr_url.strip('/')}/index.php?/cases/view/{item['id']}"
                            st.markdown(f'<div style="text-align:right;"><a href="{case_url}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                        
                        # --- 摺疊步驟區塊 (修復 Duplicate ID) ---
                        with st.expander("🔽 查看測試步驟"):
                            raw_steps = item['steps']
                            if isinstance(raw_steps, list) and len(raw_steps) > 0:
                                for i, s in enumerate(raw_steps, 1):
                                    st.markdown(f"**Step {i}:** {s.get('content', '')}")
                                    st.markdown(f"*Expected:* {s.get('expected', '')}")
                                    st.divider()
                            else:
                                # 加入唯一 key 以修復 Duplicate Element ID 錯誤
                                content = str(raw_steps) if raw_steps else "無詳細步驟資料"
                                st.text_area(f"Step Details (#{item['id']})", value=content, height=150, disabled=True, key=f"area_{item['id']}")
                        
                        st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)
            else:
                st.info("查無結果，請嘗試其他關鍵字。")
        else:
            st.error(f"❌ 無法讀取資料。錯誤詳情: {path_map}")
else:
    st.warning("👈 請在左側側邊欄輸入 TestRail 連線資訊。")
