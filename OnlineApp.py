import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG

# 1. 初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

# 🛑 【物理驅逐黑名單】把妳不想看到的 Case ID 通通寫在這裡
# 這裡寫的是字串，例如 "31316"
BLACKLIST_IDS = ["31316"] 

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
    
    if st.button("🔄 强制刷新并清空快取", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能检索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        # 搜寻佈局
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("● 搜寻內容:", value=st.session_state.q_text, placeholder="輸入多個關鍵字 (例如: 充值 CNY)", key=f"input_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True): 
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查询", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                
                # 🛡️ 物理屏障：只要 ID 在黑名單裡，管妳搜什麼，這筆 Case 直接當作不存在
                if cid in BLACKLIST_IDS:
                    continue

                title = str(c.get('title', '')).lower()
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw).lower()
                
                # --- ⚔️ 硬核交集核心 (AND Logic) ---
                is_match = True
                score = 0
                for t in terms:
                    # 判斷這一個詞是否在任何可見欄位中
                    if (t in title) or (t in f_path) or (t in steps_text) or (t == cid):
                        if t in title: score += 10
                        elif t in f_path: score += 1
                    else:
                        # 🚨 只要有一個關鍵字「完全沒中」，直接淘汰
                        is_match = False
                        break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質加分 (依據步驟內容長度)
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((score + quality_weight, f_path, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            st.markdown(f'''<div style="background:rgba(46,164,79,0.1); border-left:5px solid #2ea44f; padding:10px 15px; margin:20px 0;">找到 {res_count} 笔符合交集条件的案例</div>''', unsafe_allow_html=True)

            if res_count == 0:
                st.info("🚫 找不到符合所有关键字的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    color = "#32CD32" if is_active else "#FF4B4B"
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到顶端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
