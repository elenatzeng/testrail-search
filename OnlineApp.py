import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()

# 2. 獲取參數
def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

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
        q_input = st.text_input("● 搜尋內容 (交集模式):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            # 拆分詞彙
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                case_id = str(c.get('id'))
                title = str(c.get('title', '')).lower()
                path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_text = str(steps_raw).lower()

                # --- ⚔️ 硬核交集核心 (AND Logic) ---
                is_all_present = True 
                score = 0

                for t in terms:
                    # 調用隔離後的字典
                    exp_words = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 檢查這一個關鍵字群組是否出現在 Case 裡
                    found_this_term = False
                    for w in exp_words:
                        if w in title or w in path or w in steps_text or t == case_id:
                            found_this_term = True
                            if w in title: score += 10000 # 命中標題高分
                            break
                    
                    # 🛡️ 關鍵：只要有一個搜尋詞「沒中」，這筆 Case 就「滾蛋」
                    if not found_this_term:
                        is_all_present = False
                        break 
                
                # 🛡️ 只有通過「全中測試」的才准進入清單
                if is_all_present:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質加權 (步數越多分數越高)
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    final_score = score + (step_count * 2000) + u.get("weight", 0)
                    results.append((final_score, path, c, u))

            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            # --- ✨ 筆數統計 (我愛你版專屬樣式) ---
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.1); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 20px 0;">
                    搜尋結果： <b>{res_count}</b> 筆完全符合條件之案例
                </div>
            ''', unsafe_allow_html=True)

            for _, path, item, u in results:
                cid = str(item.get('id'))
                is_active = u.get("is_active", True)
                color = "#32CD32" if is_active else "#FF4B4B"
                tag = f'<span style="color:{color}; border:1px solid {color}; padding:2px 10px; border-radius:15px; font-size:12px; font-weight:bold; margin-left:10px;">{"🟢" if is_active else "🔴"} {u["name"]}</span>'
                
                st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="display:flex; align-items:center; margin-bottom:10px;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                with st.expander("查看步驟"):
                    st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
