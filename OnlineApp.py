import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面基礎配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 2. 側邊欄設定
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

# 3. 核心邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div style="color:#8b949e; font-size:14px; margin-bottom:20px;">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="輸入關鍵字...", label_visibility="collapsed")
            st.session_state.q_text = q_input

        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()

        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        # 4. 智慧搜尋與權重排序
        final_query = st.session_state.q_text
        if final_query:
            raw_input_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []

            for case_item in all_cases:
                cid = str(case_item.get('id', '')).strip()
                title = str(case_item.get('title', '')).lower()
                section_path = str(path_map.get(case_item.get('section_id', ""), "")).lower()
                
                # 取得清理後的內容
                raw_body = str(case_item.get('custom_steps','')) + str(case_item.get('custom_steps_separated',''))
                clean_body_data = clean_html(raw_body)
                search_text = str(clean_body_data).lower()
                
                searchable_pool = title + section_path + search_text
                
                is_all_match = True
                total_score = 0
                for term in raw_input_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    if any(word == cid for word in expanded): total_score += 1000000
                    
                    if not (any(word in searchable_pool for word in expanded) or any(word == cid for word in expanded)):
                        is_all_match = False
                        break
                    else:
                        if any(word in title for word in expanded): total_score += 5000
                
                if is_all_match:
                    creator_id = int(case_item.get('created_by', 0))
                    u_info = USER_CONFIG.get(creator_id, DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    
                    if len(search_text.strip()) < 10 or "(無詳細步驟)" in search_text:
                        total_score -= 2000000 
                    
                    scored_results.append((total_score, case_item, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                # 🚀 名字弧形外框與配色
                tag_color = '#4CAF50' if u_info.get('is_active', True) else '#8b949e'
                status_emoji = "🟢" if u_info.get('is_active', True) else "⚪"
                
                # ✨ 🚀 修正點：標籤拉開距離 (margin-left: 15px) 與字體加大 (13px)
                author_tag_html = f"""
                    <span class="author-tag" style="border-color: {tag_color} !important; box-shadow: 0 0 5px {tag_color} !important; border-radius: 25px !important; border: 2px solid !important; margin-left: 15px !important;">
                        <span style="font-size: 14px; margin-right: 6px;">{status_emoji}</span>
                        <span style="font-size: 13px; font-weight: 800; color: white !important;">{u_info.get('name', 'Unknown')}</span>
                    </span>
                """
                
                # 路徑顯示
                st.markdown(f'<div style="font-size:12px; color:#8b949e; margin-top:15px;">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7.5, 1.5], vertical_alignment="center")
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold; display: flex; align-items: center;">{item.get("title")} (#{cid}) {author_tag_html}</div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 🔽 查看測試步驟
                with st.expander("🔽 查看測試步驟"):
                    steps_data = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    if isinstance(steps_data, list):
                        for i, step in enumerate(steps_data, 1):
                            # 將內容與預期結果中的 \n 轉換為 <br> 以確保 HTML 換行
                            c_body = step.get('content','').replace('\n', '<br>')
                            e_body = step.get('expected','').replace('\n', '<br>')
                            st.markdown(f"""
                                <div style="border-left:3.5px solid #2ea44f; padding-left:15px; margin-bottom: 20px;">
                                    <div style="font-weight:bold; font-size:13px; margin-bottom:5px; color:#8b949e;">Step {i}:</div>
                                    <div class="step-content-box" style="white-space: pre-wrap;">{c_body}</div>
                                    <div style="font-weight:bold; font-size:13px; margin:12px 0 5px 0; color:#8b949e;">Expected:</div>
                                    <div class="step-content-box" style="border-left:1px dashed #444c56; white-space: pre-wrap;">{e_body}</div>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="step-content-box" style="white-space: pre-wrap;">{steps_data if steps_data else "(無詳細步驟)"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    # 🚀 活力橘回到頂端按鈕
    st.markdown('<a href="#top-anchor" class="scroll-to-top">▲</a>', unsafe_allow_html=True)

else:
    st.info("👈 請在左側輸入連線資訊開始查詢。")
