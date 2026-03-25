import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from keywords import SEARCH_DICTIONARY

# (前面 import 維持不變)
import re, time, ast
from testrail_api import TestRailAPI

# 🚀 1. 使用者設定中心 (在此修改離職狀態與權重)
# is_active=True 是綠燈綠線，False 是紅燈紅線
USER_CONFIG = {
    'Esther': {'id': 1001, 'is_active': True, 'weight': 500},  # 🟢 在職：綠燈綠線
    'Cooper': {'id': 1002, 'is_active': False, 'weight': -100}, # 🔴 離職範例
}
DEFAULT_CONFIG = {'id': 0, 'is_active': True, 'weight': 0}

# (基礎頁面配置邏輯維持不變)
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 🚀 2. 側邊欄設定 (連線設定維持不變)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "10")))
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 🚀 3. 主程式搜尋與顯示邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div style="color:#8b949e; font-size:14px;">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="充值 CNY", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()
        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_input_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []
            
            for c in all_cases:
                # 搜尋邏輯维持不變
                cid = str(c.get('id', '')).strip()
                title = str(c.get('title', '')).lower()
                section_path = str(path_map.get(c.get('section_id', ""), "")).lower()
                clean_body_data = clean_html(str(c.get('custom_steps','')) + str(c.get('custom_steps_separated','')))
                search_text = str(clean_body_data).lower()
                searchable_pool = title + section_path + search_text
                
                is_all_match = True
                total_score = 0
                for term in raw_input_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    if not (any(word in searchable_pool for word in expanded) or any(word == cid for word in expanded)):
                        is_all_match = False; break
                    else:
                        if any(word in title for word in expanded): total_score += 1000
                
                if is_all_match:
                    author_name = item.get('custom_testrail_author_name', 'Esther') 
                    u_info = USER_CONFIG.get(author_name, DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    if len(search_text.strip()) < 10: total_score -= 500000 # 懲罰分數維持
                    scored_results.append((total_score, c, u_info, author_name))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例")

            for _, item, u_info, author_name in scored_results:
                cid = str(item.get('id'))
                
                # 🚀 4. ✨ 終極修正：生成正確的膠囊弧形發光 HTML (徹底取代白框代碼)
                if u_info.get('is_active'):
                    # 🟢 在職：亮綠燈綠線 + 微發光
                    tag_color = "#4CAF50" # 亮綠色
                    status_emoji = "🟢"
                else:
                    # 🔴 離職：亮紅燈紅線 + 微發光
                    tag_color = "#ff4b4b" # 亮紅色
                    status_emoji = "🔴"
                
                # 生成漂亮的 HTML 膠囊發光標籤
                author_tag_html = f"""
                    <span class="author-tag" style="border-color: {tag_color} !important; box-shadow: 0 0 5px {tag_color} !important;">
                        <span style="font-size: 14px; margin-right: 6px;">{status_emoji}</span>{author_name}
                    </span>
                """
                
                st.markdown(f'<div class="case-path-text">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7.5, 1.5], vertical_alignment="center")
                with c_title:
                    # 🚀 在標題旁邊顯示我們做好的漂亮膠囊發光標籤
                    st.markdown(f'<div style="font-size:16px; font-weight:bold; display: flex; align-items: center;">{item.get("title")} (#{cid}) {author_tag_html}</div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("🔽 查看測試步驟"):
                    # 測試步驟渲染維持不變，確保無詳細步驟不帶 HTML 標籤
                    steps_data = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    if isinstance(steps_data, list):
                        for i, step in enumerate(steps_data, 1):
                            st.markdown(f"""
                                <div class="step-item">
                                    <div style="font-weight:bold; color:#ffffff; margin-bottom:5px;">Step {i}:</div>
                                    <div class="step-content-box">{step.get('content','').replace('\n', '<br>')}</div>
                                    <div style="font-weight:bold; color:#ffffff; margin-top:10px; margin-bottom:5px;">Expected:</div>
                                    <div class="step-content-box" style="border-left: 2px dashed #444c56;">{step.get('expected','').replace('\n', '<br>')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box">{steps_data if steps_data else "（無詳細步驟）"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # 🚀 5. 回到頂端按鈕補丁 (維持不受影響)
    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)

else:
    st.info("👈 請在左側輸入資料開始查詢。")
