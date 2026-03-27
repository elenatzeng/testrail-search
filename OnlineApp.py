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
        
        # 搜尋框
        q_input = st.text_input("● 搜尋內容 (輸入多關鍵字，如: 充值 CNY):", value=st.session_state.q_text)
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 🧠 核心：交集過濾計數器 ---
                matched_count = 0
                final_weight = 0
                
                for t in terms:
                    # 💡 幣種嚴格判定 (長度 3 的代碼)
                    is_currency = (len(t) == 3 and t.isalpha())
                    
                    if is_currency:
                        # 幣種必須出現在標題或路徑，否則這筆不計分
                        if t in title or t in f_path:
                            matched_count += 1
                            final_weight += 100000  # 幣種命中給 10 萬分 (絕殺)
                    else:
                        # 一般詞走字典擴展
                        exp = multi_lang_search(t, SEARCH_DICTIONARY)
                        t_m = any(w in title for w in exp) or (t == cid)
                        p_m = any(w in f_path for w in exp)
                        c_m = any(w in steps_str for w in exp)
                        if t_m or p_m or c_m:
                            matched_count += 1
                            if t_m: final_weight += 5000

                # 🛡️ 嚴格交集：必須「全部」關鍵字都中才准計入結果
                if matched_count == len(terms):
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質壓制：以步驟數量為準
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    total_score = final_weight + (step_count * 2000) + u.get("weight", 0)
                    
                    results.append(((-total_score, f_path, cid), f_path, c, u))

            results.sort(key=lambda x: x[0])
            res_count = len(results)

            # --- ✨ 筆數顯示區 (就在搜尋框正下方) ---
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.15); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 20px 0; border-radius: 4px;">
                    <span style="color: #adb5bd;">搜尋結果：</span>
                    <span style="color: #2ea44f; font-size: 18px; font-weight: bold;">{res_count}</span>
                    <span style="color: #adb5bd;"> 筆符合條件之案例</span>
                </div>
            ''', unsafe_allow_html=True)

            if res_count == 0:
                st.info("🚫 找不到完全符合所有關鍵字的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    # 🔴 紅標鎖死樣式
                    color = "#32CD32" if is_active else "#FF4B4B"
                    bg = "rgba(50, 205, 50, 0.1)" if is_active else "rgba(255, 75, 75, 0.1)"
                    tag = f'<span style="color:{color}; border:1px solid {color}; background:{bg}; padding:2px 12px; border-radius:20px; font-size:12px; font-weight:bold; margin-left:10px;">{"🟢" if is_active else "🔴"} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:10px;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看測試步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")
