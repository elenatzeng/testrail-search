import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from keywords import SEARCH_DICTIONARY
# 🚀 如果妳有 users 模組，請在這裡匯入 USER_CONFIG

# (連線設定邏輯维持不變...)

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        # ... (搜尋欄位邏輯維持不變...)

        final_query = st.session_state.q_text
        if final_query:
            # ... (搜尋篩選與權重排序邏輯維持不變...)

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                
                # 檔案目錄路徑文字
                st.markdown(f'<div class="case-path-text">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                
                # 標題與名字標籤欄
                c_title, c_btn = st.columns([7, 1.5], vertical_alignment="center")
                with c_title:
                    # 🚀 修正點 (箭頭 1)：加粗弧形名字標籤，並使用 margin-left 拉開距離
                    author_color = '#4CAF50' if u_info.get('is_active') else '#ff4b4b'
                    st.markdown(f"""
                        <div style="font-size:16px; font-weight:bold; display:flex; align-items:center;">
                            {item.get('title')} <small style="color:#8b949e; font-weight:normal;">(#{cid})</small>
                            <span class="author-tag" style="border: 1px solid {author_color}; color:{author_color}; margin-left:10px;">
                                {"🟢" if u_info.get("is_active") else "🔴"} {u_info["name"]}
                            </span>
                        </div>
                    """, unsafe_allow_html=True)

                with c_btn:
                    # (Open Case 按鈕邏輯維持不變)

                # 🔽 測試步驟展開
                with st.expander("🔽 查看測試步驟"):
                    # 🚀 utils.py 已經在 Python 端拆解並加入換行符號
                    steps_data = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    if isinstance(steps_data, list):
                        # 如果是分離步驟 (Separated Steps)，用漂亮的深灰盒子和綠色邊條顯示
                        for i, step in enumerate(steps_data, 1):
                            st.markdown(f"""
                                <div class="step-item">
                                    <div style="font-weight:bold; color:#ffffff; margin-bottom:5px;">Step {i}:</div>
                                    <div class="step-content-box">{step.get('content','')}</div>
                                    <div style="font-weight:bold; color:#ffffff; margin-top:10px; margin-bottom:5px;">Expected:</div>
                                    <div class="step-content-box" style="border-left: 1px dashed #444c56;">{step.get('expected','')}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        # 如果是普通文字，直接顯示在一個深灰盒子裡 (utils.py 已處理換行)
                        st.markdown(f'<div class="step-content-box">{steps_data if steps_data else "（無詳細步驟）"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # (回到頂端按鈕邏輯維持不變)
