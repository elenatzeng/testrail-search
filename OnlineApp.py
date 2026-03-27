import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 页面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 侧边栏
with st.sidebar:
    st.header("🔐 连线设定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("账号 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 储存资讯至网址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已储存")
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
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜寻内容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="请输入关键字，例如：充值 CNY", label_visibility="collapsed", key=f"search_input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除条件", use_container_width=True): 
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun() 
        with col_r:
            if st.button("🔎 查询", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            # 🎯 拆分關鍵字
            terms = [t.lower().strip() for t in st.session_state.q_text.split() if t]
            results = []

            for c in all_cases:
                # 🔒 全部轉小寫，不做任何長度判斷，不做正則比對
                c_title = str(c.get('title', '')).lower()
                c_id = str(c.get('id'))
                c_path = str(path_map.get(c.get('section_id'), "")).lower()
                
                is_match = True
                for t in terms:
                    # 📖 取得聯想詞
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 只要這組詞裡有任何一個被包含在標題、路徑或 ID 裡
                    # 這裡用最簡單的 "in"，不管字有多短，通通都能搜到
                    if not any(str(w).lower() in c_title or str(w).lower() in c_path or str(w).lower() == c_id for w in expanded):
                        is_match = False
                        break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or ""
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((quality_weight, c_path, c, u))

            results.sort(key=lambda x: (-x[0], x[1]))

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px;">🚫 找不到符合的案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    disp_path = path_map.get(item.get('section_id'), "")
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {disp_path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag">🟢 {u["name"]}</span>'
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{item.get("id")})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{item.get("id")}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    with st.expander("查阅测试步骤"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.markdown("---")
else:
    st.info("👈 请先在左侧完成连线设定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到顶端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
