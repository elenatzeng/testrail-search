import streamlit as st
import re
import os
import sys

# 🛡️ 路径保险：确保能正确读取同目录下的 style.py
sys.path.append(os.path.dirname(__file__))

from style import apply_custom_style
from utils import fetch_data_from_tr, multi_lang_search
# 假设你的配置文件名如下，请根据实际情况调整
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

# --- 🚀 自动记忆逻辑 ---
keys_to_store = ["url", "user", "pw", "pid", "sid"]
for k in keys_to_store:
    store_key = f"store_{k}"
    if store_key not in st.session_state:
        st.session_state[store_key] = ""

def get_val(key):
    val = st.query_params.get(key)
    if val is not None:
        return val
    return st.session_state.get(f"store_{key}", "")

# 2. 侧边栏
with st.sidebar:
    st.header("🔐 连线设定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("账号 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 储存资讯并记住我", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.session_state.store_url, st.session_state.store_user = tr_url, tr_user
        st.session_state.store_pw = tr_pw
        st.session_state.store_pid, st.session_state.store_sid = str(pid), str(sid)
        st.success("✅ 已储存并自动记忆")

st.title("🧪 TestRail 智能逻辑检索")

# 3. 核心数据与搜索逻辑
if tr_url and tr_user and tr_pw:
    # 从 TR 获取数据
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：**{p_name}** | Suite：**#{sid}**", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input(
                "多维精准检索 :", 
                value=st.session_state.q_text, 
                placeholder="支持多关键字交集过滤，兼容繁/简/英关键字或 #ID",
                key="search_box"
            )
            st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            
            for c in all_cases:
                title, cid = str(c.get('title', '')), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                
                match_score = 0
                is_match = True
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    # 检查标题、ID、路径
                    t_m = any(w in title.lower() for w in exp) or any(w == cid for w in exp)
                    p_m = any(w in f_path.lower() for w in exp)
                    
                    if t_m: match_score += 10
                    elif p_m: match_score += 1
                    else: is_match = False; break
                
                if is_match:
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                    q_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((match_score + q_weight, f_path, c, u_info))

            # 🛠️ 关键：强制执行排序逻辑
            results.sort(key=lambda x: (-x[0], x[1]))

            for _, path, item, u in results:
                # 渲染结果（省略重复的 Markdown 渲染代码，保持逻辑完整）
                st.write(f"📁 {path} - **{item.get('title')}**")
                # ... (此处接你原有的 Expander 渲染逻辑)
        else:
            st.info("💡 请输入关键字开始多维检索...")

# 回顶火箭
st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
