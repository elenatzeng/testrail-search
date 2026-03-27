import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
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
    
    if st.button("🔄 强制刷新数据", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能检索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        q_input = st.text_input("● 搜寻内容 (字典通用+交集):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', '')).lower()
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw).lower()
                
                # --- ⚔️ 硬核交集判定 (Must Match EVERY Term) ---
                is_all_terms_matched = True
                total_score = 0

                for t in terms:
                    # 1. 拿到這個詞的所有同義詞 (如果是 CNY, 就只有 ['cny'])
                    synonyms = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 2. 檢查這一組同義詞中，是否有任何一個出現在 Case 裡
                    found_any_synonym = False
                    for s in synonyms:
                        if (s in title) or (s in f_path) or (s in steps_text) or (t == cid):
                            found_any_synonym = True
                            # 分數加權 (標題命中給高分)
                            if s in title: total_score += 10
                            elif s in f_path: total_score += 1
                            break # 只要這組同義詞有一個中了，這個關鍵字就算過關
                    
                    # 3. 🚨 如果這一組同義詞「完全沒人命中」，代表這個關鍵字斷了
                    if not found_any_synonym:
                        is_all_terms_matched = False
                        break # 直接淘汰這筆 Case
                
                # 只有每個關鍵字都過關的才顯示
                if is_all_terms_matched:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((total_score + quality_weight, f_path, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))
            
            st.markdown(f'<div style="background:rgba(46,164,79,0.1); border-left:4px solid #2ea44f; padding:10px 15px; margin:20px 0;">找到 {len(results)} 筆完全符合條件之案例</div>', unsafe_allow_html=True)

            if not results:
                st.info("🚫 找不到同時符合所有關鍵字(含同義詞)的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:12px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active", True) else "inactive"}">{"🟢" if u.get("is_active", True) else "🔴"} {u["name"]}</span>'
                    st.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查閱步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")
