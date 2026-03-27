import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search, match_keyword
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
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
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        q_input = st.text_input("● 搜尋內容 (精確邊界交集模式):", value=st.session_state.q_text, placeholder="例如: 充值 CNY")
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            # 將搜尋語句拆分為多個關鍵字
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
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

                for t in terms:
                    # 獲取該搜尋詞在字典中的替身
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 💡 核心：這一組關鍵字中，必須有任一個「精確」命中標題、路徑或步驟
                    hit_group = any(
                        match_keyword(title, v) or 
                        match_keyword(f_path, v) or 
                        match_keyword(steps_text, v)
                    ) or (t == cid)
                    
                    if hit_group:
                        # 標題命中給予較高權重
                        if any(match_keyword(title, v) for v in variants):
                            score += 10
                        elif any(match_keyword(f_path, v) for v in variants):
                            score += 1
                    else:
                        # 只要有一組搜尋詞沒精確命中，直接判出局
                        is_all_passed = False
                        break 
                
                if is_all_passed:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 品質權重 (根據內容豐富度)
                    quality = 10000 if len(steps_text) > 20 else 0
                    results.append((score + quality, f_path, c, u))

            # 根據分數排序
            results.sort(key=lambda x: (-x[0], x[1]))
            res_count = len(results)

            st.markdown(f'<div style="background:rgba(46,164,79,0.1); border-left:4px solid #2ea44f; padding:15px; margin:20px 0;">找到 {res_count} 筆精確符合條件之案例</div>', unsafe_allow_html=True)

            if not results:
                st.info("🚫 找不到符合所有關鍵字精確匹配的案例。")
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
