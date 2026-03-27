import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY # 確保妳的字典檔案名稱正確

# 1. 初始化
st.set_page_config(page_title="TestRail Search", layout="wide", page_icon="🧪")
apply_custom_style()

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid") or 10))
    sid = st.number_input("Suite ID", value=int(get_val("sid") or 10))
    
    if st.button("🔄 强制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        q_input = st.text_input("● 搜尋內容 (字典聯想模式):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            input_terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', '')).lower()
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw).lower()
                
                # --- ⚔️ 分組嚴格交集邏輯 ---
                is_all_groups_matched = True
                case_score = 0

                for term in input_terms:
                    # 獲取該詞的所有同義詞 (如: 搜尋'充值' -> ['deposit', '存款', '充值'])
                    synonyms = multi_lang_search(term, SEARCH_DICTIONARY)
                    
                    # 檢查這組同義詞中，是否有任何一個出現在這筆 Case 裡
                    group_match = False
                    for s in synonyms:
                        if (s in title) or (s in f_path) or (s in steps_text) or (term == cid):
                            group_match = True
                            if s in title: case_score += 10
                            elif s in f_path: case_score += 1
                            break # 這組關鍵字 OK 了，換下一個輸入詞
                    
                    if not group_match:
                        is_all_groups_matched = False
                        break # 只要有一組關鍵字完全沒中，這筆 Case 就淘汰
                
                if is_all_groups_matched:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((case_score + quality_weight, f_path, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))
            
            st.markdown(f'<div style="background:rgba(46,164,79,0.1); border-left:4px solid #2ea44f; padding:15px; margin:20px 0;">找到 {len(results)} 筆符合條件之案例</div>', unsafe_allow_html=True)

            if not results:
                st.info("🚫 找不到同時符合所有關鍵字(含同義詞)的案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    st.markdown(f'<div style="font-size:12px; color:#adb5bd; margin-top:10px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active", True) else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    st.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")
