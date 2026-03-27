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

# 💡 妳提供的精確匹配核心函數
def match_keyword(text, keyword):
    # \b 確保是獨立單字匹配，不會搜尋 CNY 卻搜到 ACNY
    return re.search(rf'\b{re.escape(keyword)}\b', text, re.IGNORECASE)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄
with st.sidebar:
    st.header("🔐 连线设定")
    tr_url = st.text_input("URL", value=get_val("url"))
    tr_user = st.text_input("Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid") or 10))
    sid = st.number_input("Suite ID", value=int(get_val("sid") or 10))
    if st.button("🔄 强制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        q_input = st.text_input("● 搜尋內容 (精確邊界模式):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            input_terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                steps_text = str(steps_raw)
                
                # --- ⚔️ 分組嚴格判定 (AND Logic) ---
                is_all_passed = True
                score = 0

                for term in input_terms:
                    # 獲取搜尋詞及其同義詞
                    variants = multi_lang_search(term, SEARCH_DICTIONARY)
                    
                    # 檢查這組同義詞中，是否有任何一個「精確」命中標題、路徑、內容
                    hit_group = False
                    for v in variants:
                        # 分別對各個欄位使用 match_keyword 進行邊界判定
                        t_match = match_keyword(title, v) or (term == cid)
                        p_match = match_keyword(f_path, v)
                        s_match = match_keyword(steps_text, v)

                        if t_match or p_match or s_match:
                            hit_group = True
                            if t_match: score += 10
                            elif p_match: score += 1
                            break # 這組命中一個替身就算成功，檢查下一個 input_term
                    
                    if not hit_group:
                        is_all_passed = False
                        break # 只要其中一組關鍵字完全沒中，就淘汰
                
                if is_all_passed:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    quality = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((score + quality, f_path, c, u))

            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            st.markdown(f'<div style="background:rgba(46,164,79,0.1); border-left:4px solid #2ea44f; padding:15px; margin:20px 0;">找到 {res_count} 筆符合「精確交集」條件之案例</div>', unsafe_allow_html=True)

            if not results:
                st.info("🚫 找不到同時符合所有關鍵字(含同義詞)的精確匹配案例。")
            else:
                for _, path, item, u in results:
                    cid_str = str(item.get('id'))
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active", True) else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    st.markdown(f'<div style="font-size:12px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="display:flex; align-items:center;"><h4>{item.get("title")} (#{cid_str})</h4>{tag}</div>', unsafe_allow_html=True)
                    with st.expander("查看步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown("---")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
