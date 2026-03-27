import streamlit as st
import re
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail Search Pro", layout="wide")
apply_custom_style()

# 版本確認橫幅 (Demo 完可以自行刪除這行)
st.success("✅ 系統已更新：已啟動單字邊界鎖死邏輯 (CNY / VND 精度修復)")

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value="https://gorun.testrail.io/")
    tr_user = st.text_input("Email", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.info(f"📍 當前專案：{p_name} | 資料更新時間：{last_up}")
        q_text = st.text_input("🔍 請輸入搜尋詞 (支援多詞搜尋):", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 提取純文字內容
                title_txt = str(c.get('title', ''))
                steps_txt = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                is_all_passed = True
                
                for t in terms:
                    # 判斷是否為 3 碼英文幣別，是的話鎖死不聯想
                    variants = [t] if (len(t) == 3 and t.isalpha()) else multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 搜尋標題、步驟內容或 ID
                    hit = any(match_visual_only(title_txt, v) or match_visual_only(steps_txt, v) or t == cid for v in variants)
                    
                    if not hit:
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    path = path_map.get(c.get('section_id'), "Unknown")
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((path, c, u_cfg))

            st.success(f"找到 {len(results)} 筆完全匹配結果")
            for path, item, u in results:
                st.markdown(f'<div style="color:gray; font-size:11px; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                
                tag = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                
                with st.expander("查看步驟詳情"):
                    st.text(smart_format(steps_txt))
                st.markdown("---")
