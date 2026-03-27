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

# ✨ 【停机坪】在最顶端放置锚点，火箭点击后才能精准飞回顶部
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 侧边栏守护 (连线设定)
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
        # ✨ 显示 Project 资讯
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 搜寻列布局
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        # ✨ 初始化控制变数 (确保清除功能运作)
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
            # 🎯 統一轉小寫處理輸入詞
            terms = [t.lower().strip() for t in st.session_state.q_text.split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                # 🔒 將標題、路徑與 ID 全部轉小寫，確保大小寫不敏感
                title_low = str(c.get('title', '')).lower()
                cid_str = str(c.get('id'))
                path_low = str(path_map.get(c.get('section_id'), "")).lower()
                
                match_score = 0
                is_match = True
                for t in terms:
                    # 📖 取得聯想詞 (字典有中就拿整組，沒中 expanded 就只有 [t])
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 暴力比對：只要標題、路徑或 ID 包含這組詞中的任何一個，就算命中
                    # 這裡不再限定字數，不管字多短，只要 in 就過
                    term_hit = any(w.lower() in title_low or w.lower() in path_low or w.lower() == cid_str for w in expanded)
                    
                    if term_hit:
                        if any(w.lower() in title_low for w in expanded): match_score += 10
                        elif any(w.lower() in path_low for w in expanded): match_score += 1
                    else:
                        is_match = False; break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((match_score + quality_weight, path_low, c, user_info))

            # ✨ 排序
            results.sort(key=lambda x: (-x[0], x[1]))

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px; padding-left:5px;">🚫 找不到符合的测试案例。</div>', unsafe_allow_html=True)
            else:
                for _, _, item, u in results:
                    curr_cid = str(item.get('id'))
                    disp_path = path_map.get(item.get('section_id'), "")
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {disp_path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{curr_cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{curr_cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    
                    with st.expander("查阅测试步骤", expanded=False):
                        # 保留妳原本的渲染邏輯
                        st.text(clean_html(item.get('custom_steps') or item.get('custom_steps_separated') or ""))
                    st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">请输入关键字开始检索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 请先在左侧完成连线设定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到顶端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
