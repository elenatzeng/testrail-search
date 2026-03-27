import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG

# 1. 初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
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

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}", unsafe_allow_html=True)
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="请输入关键字，如: 充值 CNY", label_visibility="collapsed", key=f"s_i_{st.session_state.search_key}")
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除条件", use_container_width=True): 
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun() 
        with col_r:
            if st.button("🔎 查询", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            # 💡 只有空格切開的「純關鍵字」
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', '')).lower()
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw).lower()
                
                # --- ⚔️ 硬核交集判定 (AND Logic) ---
                is_match = True
                score = 0
                for t in terms:
                    # 這裡調用的 multi_lang_search 現在只會回傳原詞
                    if (t in title) or (t in f_path) or (t in steps_text) or (t == cid):
                        if t in title: score += 10
                        elif t in f_path: score += 1
                    else:
                        # 🚨 只要有一個詞沒中，這筆資料直接踢掉！
                        is_match = False
                        break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質加分：長度超過 10 個字元的給權重，讓 Katty 這種有料的排前面
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((score + quality_weight, f_path, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            st.markdown(f'<div style="background:rgba(46,164,79,0.1); border-left:4px solid #2ea44f; padding:10px 15px; margin:20px 0;">找到 {res_count} 笔完全符合条件的案例</div>', unsafe_allow_html=True)

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px;">🚫 找不到符合所有关键字的案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    
                    with st.expander("查阅测试步骤"):
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        if isinstance(steps_data, list):
                            for s_idx, s in enumerate(steps_data, 1):
                                st.markdown(f'**Step {s_idx}:**\n{s.get("content")}\n**Expected:**\n{s.get("expected")}')
                    st.markdown("---")
