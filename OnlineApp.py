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
        q_input = st.text_input("● 搜尋內容 (多關鍵字請用空格):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            # 💡 獲取搜尋詞清單：['充值', 'cny']，長度為 2
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 🛡️ 物理驅逐邏輯：AND (交集) ---
                matched_term_count = 0
                temp_score = 0
                
                for t in terms:
                    # 💡 幣種保護：長度 3 的字 (CNY/THB/VND) 採精確匹配，不進字典
                    exp = [t] if len(t) == 3 else multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    in_title = any(w in title for w in exp) or (t == cid)
                    in_path = any(w in f_path for w in exp)
                    in_content = any(w in steps_str for w in exp)
                    
                    # 只要這一個詞 (或同義詞) 在 Case 裡出現過，計數 +1
                    if in_title or in_path or in_content:
                        matched_term_count += 1
                        if in_title: temp_score += 10000 
                        elif in_path: temp_score += 1000

                # ⚠️ 終極關卡：必須命中「所有」搜尋詞，才准放進結果清單
                # 如果搜尋 2 個詞，但 matched_term_count 只有 1，直接丟棄！
                if matched_term_count == len(terms):
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質加分：每步 2000 分，Katty 贏在內容
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    total_final_score = temp_score + (step_count * 2000) + u.get("weight", 0)
                    results.append((total_final_score, f_path, c, u))

            # 排序
            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            # --- ✨ 筆數統計 (這次一定準) ---
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.15); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 20px 0; border-radius: 4px;">
                    <span style="color: #adb5bd;">搜尋結果：</span>
                    <span style="color: #2ea44f; font-size: 18px; font-weight: bold;">{res_count}</span>
                    <span style="color: #adb5bd;"> 筆「完全符合」條件之案例</span>
                </div>
            ''', unsafe_allow_html=True)

            if res_count == 0:
                st.info("🚫 找不到完全符合所有關鍵字的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    # 🔴 紅標顏色暴力鎖死
                    color = "#32CD32" if is_active else "#FF4B4B"
                    bg = "rgba(50, 205, 50, 0.1)" if is_active else "rgba(255, 75, 75, 0.1)"
                    tag = f'<span style="color:{color} !important; border:1px solid {color} !important; background:{bg} !important; padding:2px 12px; border-radius:20px; font-size:12px; font-weight:bold; margin-left:10px;">{"🟢" if is_active else "🔴"} {u["name"]}</span>'
                    
                    st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:10px;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看測試步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
