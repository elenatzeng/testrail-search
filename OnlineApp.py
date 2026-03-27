import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 页面初始化 (保持妳的版本)
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
    if st.button("💾 储存资讯", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
    if st.button("🔄 强制刷新数据", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能检索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        # --- 搜寻列 ---
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜寻内容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="输入关键字 (例如: 充值 CNY)...", key=f"s_in_{st.session_state.search_key}", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查询", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- ✨ 嚴格交集邏輯 ---
                match_count = 0
                match_score = 0
                for t in terms:
                    # 💡 幣種鎖死：長度 <= 4 (CNY) 不進字典，避免抓到 THB
                    exp = [t] if len(t) <= 4 else multi_lang_search(t, SEARCH_DICTIONARY)
                    t_m = any(w in title for w in exp) or (t == cid)
                    p_m = any(w in f_path for w in exp)
                    c_m = any(w in steps_str for w in exp)
                    if t_m or p_m or c_m:
                        match_count += 1
                        if t_m: match_score += 10
                
                if match_count == len(terms):
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 💡 內容品質權重：每一步加 1000 分，壓死 Meh
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    quality_bonus = step_count * 1000
                    results.append((match_score + quality_bonus + u.get("weight", 0), f_path, c, u))

            results.sort(key=lambda x: (-x[0], x[1]))

            # --- 🚀🚀🚀 這裡就是妳要的「顯示筆數」區塊 ---
            res_count = len(results)
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.1); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 20px 0; border-radius: 4px;">
                    <span style="color: #adb5bd; font-size: 14px;">搜尋結果：</span>
                    <span style="color: #2ea44f; font-size: 18px; font-weight: bold;">{res_count}</span>
                    <span style="color: #adb5bd; font-size: 14px;"> 筆符合條件之案例</span>
                </div>
            ''', unsafe_allow_html=True)
            # --- 🚀🚀🚀 ---

            if res_count == 0:
                st.info("🚫 找不到符合「所有關鍵字」的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    # 🔴 顏色暴力鎖死：保證紅標會亮
                    color = "#32CD32" if is_active else "#FF4B4B"
                    bg = "rgba(50, 205, 50, 0.1)" if is_active else "rgba(255, 75, 75, 0.15)"
                    tag_html = f'<span style="color:{color} !important; border:1px solid {color} !important; background:{bg} !important; padding:2px 10px; border-radius:15px; font-size:12px; font-weight:bold; margin-left:10px; display:inline-flex; align-items:center;">{"🟢" if is_active else "🔴"} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")
