import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("Suite ID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        
        # 搜尋 UI
        q_input = st.text_input("● 搜尋內容 (多關鍵字請用空格):", value=st.session_state.q_text)
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            # 💡 拆分搜尋詞
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 🧠 核心：交集判定 (AND Logic) ---
                all_terms_matched = True
                case_match_score = 0
                
                for t in terms:
                    # 擴展關鍵字 (同義詞)
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 檢查這一個詞是否出現在標題、路徑或內容
                    term_hit_title = any(w in title for w in exp) or (t == cid)
                    term_hit_path = any(w in f_path for w in exp)
                    term_hit_content = any(w in steps_str for w in exp)
                    
                    if term_hit_title or term_hit_path or term_hit_content:
                        # 只要中了，我們就記錄分數
                        if term_hit_title: case_match_score += 10
                        elif term_hit_path: case_match_score += 1
                    else:
                        # 只要其中一個詞沒中，這個 Case 直接淘汰
                        all_terms_matched = False
                        break 
                
                # --- 🛡️ 只有「所有詞都中」才進行下一步 ---
                if all_terms_matched:
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質加分：按步驟數量算 (Katty 10步 vs Meh 2步)
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    quality_bonus = 10000 if step_count > 5 else 0
                    
                    total_score = case_match_score + quality_bonus + u_info.get("weight", 0)
                    results.append((total_score, f_path, c, u_info))

            # 排序：分數高優先
            results.sort(key=lambda x: (-x[0], x[1]))

            # --- ✨ 筆數顯示區 ---
            count = len(results)
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.1); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 15px 0;">
                    找到了 <b style="color:#2ea44f; font-size:18px;">{count}</b> 筆完全符合條件之案例
                </div>
            ''', unsafe_allow_html=True)

            if count == 0:
                st.info("🚫 找不到完全符合所有關鍵字的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    color = "#32CD32" if is_active else "#FF4B4B"
                    tag = f'<span style="color:{color}; border:1px solid {color}; padding:2px 10px; border-radius:15px; font-size:12px; font-weight:bold; margin-left:10px;">{"🟢" if is_active else "🔴"} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:12px; color:#adb5bd; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看測試步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
