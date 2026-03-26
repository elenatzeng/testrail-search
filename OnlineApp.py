import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄 (省略部分重複代碼，維持妳目前的連線設定即可)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("Suite ID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        # 搜尋欄位邏輯... (維持不變)
        q_text = st.text_input("● 搜尋內容:", placeholder="輸入關鍵字...", label_visibility="collapsed")

        if q_text:
            # 搜尋過濾邏輯... (維持不變)
            results = [] # 假設這裡已經跑完搜尋過濾
            # (為了展示，這裡直接進入渲染迴圈)

            for _, item, u in results: # 這裡對應妳的搜尋結果
                cid = str(item.get('id'))
                st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:20px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
                tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                
                # ✨ 【修正】標題 20px
                c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:12px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get('title')} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("查閱測試步驟", expanded=False):
                    steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                    
                    def render_steps_with_list(text):
                        if not text: return "(無內容)"
                        lines = str(text).splitlines()
                        html_out = '<div>'
                        for line in lines:
                            s = line.strip()
                            if not s: continue
                            # ✨ 早上的邏輯：判斷是否為 1. 2. 3. 或 • 
                            is_list = re.match(r'^([•\-\*]|\d+\.)', s)
                            className = "list-item" if is_list else ""
                            html_out += f'<div class="{className}">{s}</div>'
                        html_out += '</div>'
                        return html_out

                    if isinstance(steps_data, list):
                        for s_idx, s in enumerate(steps_data, 1):
                            st.markdown(f'''
                                <div style="border-left:3px solid #2ea44f; padding-left:15px; margin-bottom:20px;">
                                    <div style="color:#8b949e; font-size:13px; margin-bottom:5px;">Step {s_idx}:</div>
                                    <div class="content-box">{render_steps_with_list(s.get('content'))}</div>
                                    <div style="color:#8b949e; font-size:13px; margin-top:10px; margin-bottom:5px;">Expected:</div>
                                    <div class="content-box">{render_steps_with_list(s.get('expected'))}</div>
                                </div>
                            ''', unsafe_allow_html=True)
                st.markdown('<hr style="border-color:#30363d;">', unsafe_allow_html=True)

st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
