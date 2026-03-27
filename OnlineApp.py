import streamlit as st
import re
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail Search Pro", layout="wide")
apply_custom_style()

# 頂部狀態列
st.success("✅ 系統已修復：解決標籤錯誤與搜尋精度優化")

with st.sidebar:
    st.header("🔐 連線設定")
    # 🛡️ 這裡的標籤文字絕對不能是空的 ""
    tr_url = st.text_input("TestRail 網址", value="https://gorun.testrail.io/")
    tr_user = st.text_input("帳號 Email", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API Key / 密碼", type="password")
    pid = st.number_input("專案 ID (PID)", value=10)
    sid = st.number_input("測試集 ID (SID)", value=10)
    
    st.divider()
    if st.button("🔄 強制刷新所有數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.info(f"📍 當前專案：{p_name} | 資料更新：{last_up}")
        q_text = st.text_input("🔍 請輸入關鍵字搜尋：", placeholder="例如: 充值 cny")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                t_content = str(c.get('title', ''))
                s_content = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                is_all_passed = True
                for t in terms:
                    # 幣別鎖死邏輯
                    variants = [t] if (len(t) == 3 and t.isalpha()) else multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 呼叫 utils 裡的鎖死比對
                    hit = any(match_visual_only(t_content, v) or match_visual_only(s_content, v) or t == cid for v in variants)
                    
                    if not hit:
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    path = path_map.get(c.get('section_id'), "Unknown")
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((path, c, u_cfg))

            st.success(f"找到 {len(results)} 筆精確匹配結果")
            for path, item, u in results:
                st.markdown(f'<div style="color:gray; font-size:11px; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                
                tag = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 打開案例</a></div>', unsafe_allow_html=True)
                
                with st.expander("查看步驟詳情"):
                    st.text(smart_format(s_content))
                st.markdown("---")
