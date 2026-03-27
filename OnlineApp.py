import streamlit as st
import re
# 注意：確保妳的專案裡有 style.py, users.py, keywords.py
try:
    from style import apply_custom_style
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except ImportError:
    # 如果缺少檔案，讓它不要直接崩潰
    def apply_custom_style(): pass
    USER_CONFIG, DEFAULT_CONFIG = {}, {"name": "Unknown", "is_active": False, "weight": 0}
    SEARCH_DICTIONARY = []

from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only

st.set_page_config(page_title="Final Search Tool", layout="wide")
apply_custom_style()

# 顯示最後修復時間，確保妳跑的是這一版
st.info("🕒 系統版本：2026-03-27 最終修復版 (已修正標籤與精度問題)")

with st.sidebar:
    st.header("連線設定")
    # 🛡️ 這裡的標籤全部填寫文字，絕不留空
    tr_url = st.text_input("TestRail 網址", value="https://gorun.testrail.io/")
    tr_user = st.text_input("登入信箱", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API 密鑰", type="password")
    pid = st.number_input("專案 ID", value=10)
    sid = st.number_input("套件 ID", value=10)
    
    if st.button("🔄 刷新快取", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.write(f"已連線到：{p_name}")
        # 🛡️ 搜尋標籤也填寫文字
        q_text = st.text_input("搜尋關鍵字", placeholder="例如: cny")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                t_content = str(c.get('title', ''))
                s_content = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                is_all_passed = True
                for t in terms:
                    # 幣別鎖死
                    variants = [t] if (len(t) == 3 and t.isalpha()) else multi_lang_search(t, SEARCH_DICTIONARY)
                    hit = any(match_visual_only(t_content, v) or match_visual_only(s_content, v) or t == cid for v in variants)
                    if not hit:
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    path = path_map.get(c.get('section_id'), "Unknown")
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((path, c, u_cfg))

            st.success(f"找到 {len(results)} 筆結果")
            for path, item, u in results:
                st.write(f"📁 {path} | 👤 {u['name']}")
                st.markdown(f"#### {item['title']} (#{item['id']})")
                with st.expander("展開內容"):
                    st.text(smart_format(s_content))
                st.divider()
