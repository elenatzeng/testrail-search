import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 页面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)
apply_custom_style()

# ✨ 【停机坪】锚点
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

# --- 🚀 自動記憶邏輯開始 ---
# 初始化 Session State，用來存儲本次輸入過的值
keys_to_store = ["url", "user", "pw", "pid", "sid"]
for k in keys_to_store:
    store_key = f"store_{k}"
    if store_key not in st.session_state:
        st.session_state[store_key] = ""

def get_val(key):
    """
    獲取值的優先順序：
    1. 網址參數 (query_params) -> 方便書籤與分享
    2. Session State (store_x) -> 本次輸入過的記憶
    3. 默認空值
    """
    # 嘗試從網址拿
    url_val = st.query_params.get(key)
    if url_val is not None:
        return url_val
    # 嘗試從記憶拿
    return st.session_state.get(f"store_{key}", "")
# --- 🚀 自動記憶邏輯結束 ---

# 2. 侧边栏
with st.sidebar:
    st.header("🔐 连线设定")
    
    # 使用 get_val 賦予初始值
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("账号 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 储存资讯并记住我", use_container_width=True):
        # 1. 寫入網址參數 (安全性：這會讓用戶可以存成書籤，下次點開直接進去)
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        
        # 2. 寫入 Session State (自動記憶：在頁面刷新或切換時不必重新輸入)
        st.session_state.store_url = tr_url
        st.session_state.store_user = tr_user
        st.session_state.store_pw = tr_pw
        st.session_state.store_pid = str(pid)
        st.session_state.store_sid = str(sid)
        
        st.success("✅ 已储存并自动记忆")
        
    if st.button("🔄 强制刷新数据", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能检索中心")

# 3. 核心数据逻辑
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state:
            st.session_state.q_text = ""
        if "search_key" not in st.session_state:
            st.session_state.search_key = 0

        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜寻内容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                "", 
                value=st.session_state.q_text, 
                placeholder="请输入关键字查询，多个关键字请以空格格开", 
                label_visibility="collapsed",
                key=f"search_input_{st.session_state.search_key}"
            )
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除条件", use_container_width=True): 
                st.session_state.q_text = "" 
                st.session_state.search_key += 1 
                st.rerun() 
        with col_r:
            if st.button("🔎 查询", use_container_width=True): 
                st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                
                match_score = 0
                is_match = True
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    title_match = any(w in title.lower() for w in exp) or any(w == cid for w in exp)
                    path_match = any(w in f_path.lower() for w in exp)
                    
                    if title_match: match_score += 10
                    elif path_match: match_score += 1
                    else:
                        is_match = False; break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((match_score + quality_weight, f_path, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px; padding-left:5px;">🚫 找不到符合的测试案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    
                    with st.expander("查阅测试步骤", expanded=False):
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        def final_render(text):
                            if not text: return "(无内容)"
                            text = re.sub(img_kill_pattern, '', str(text), flags=re.IGNORECASE).strip()
                            lines = text.splitlines()
                            html_out = '<div class="inner-text" style="font-weight: 400;">' 
                            for line in lines:
                                s = line.strip()
                                if not s: continue
                                is_list = re.match(r'^([•\-\*]|\d+\.)', s)
                                style = "margin-bottom:4px; display:block; font-size:14px;"
                                if is_list: style += "padding-left:18px;"
                                html_out += f'<div style="{style}">{s}</div>'
                            html_out += '</div>'
                            return html_out

                        if isinstance(steps_data, list) and len(steps_data) > 0:
                            for s_idx, s in enumerate(steps_data, 1):
                                c_html = final_render(s.get('content', ''))
                                e_html = final_render(s.get('expected', ''))
                                st.markdown(f'''
                                    <div style="border-left:4px solid #2ea44f; padding-left:20px; margin-left:5px; margin-bottom:30px; display:block;">
                                        <div style="color:#8b949e; font-weight:500; margin-bottom:10px; font-size:13px;">Step {s_idx}:</div>
                                        <div class="content-box">{c_html}</div>
                                        <div style="color:#8b949e; font-weight:500; margin-top:20px; margin-bottom:10px; font-size:13px;">Expected:</div>
                                        <div class="content-box">{e_html}</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">请输入关键字开始检索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 请先在左侧完成连线设定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到顶端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
