import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

# (前面側邊欄邏輯維持不變...)
tr_url = st.sidebar.text_input("TestRail URL", value=st.query_params.get("url", ""))
tr_user = st.sidebar.text_input("帳號 Email", value=st.query_params.get("user", ""))
tr_pw = st.sidebar.text_input("API Key", type="password", value=st.query_params.get("pw", ""))
pid = st.sidebar.number_input("Project ID", value=10)
sid = st.sidebar.number_input("Suite ID", value=10)

if st.sidebar.button("💾 儲存資訊至網址", use_container_width=True):
    st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
    st.success("✅ 已儲存")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.title("🧪 TestRail 智能檢索中心")
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}")
        q_text = st.text_input("● 搜尋內容:", placeholder="輸入關鍵字查詢...")

        if q_text:
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'
            
            # ... 搜尋邏輯維持不變 ...
            for c in all_cases:
                results.append((100, c, DEFAULT_CONFIG)) # (這裡用原本的權重邏輯)

            for _, item, u in results:
                st.markdown(f"📁 {path_map.get(item.get('section_id'), '')}")
                with st.expander(f"{item.get('title')} (#{item.get('id')})", expanded=False):
                    steps_raw = item.get('custom_steps') or item.get('custom_steps_separated')
                    
                    # 🔥 像素還原渲染器：處理圖片隱藏與階層顏色
                    def final_hierarchy_render(text):
                        if not text: return "(無內容)"
                        text = re.sub(img_kill_pattern, '', str(text), flags=re.IGNORECASE).strip()
                        lines = text.splitlines()
                        html_out = '<div class="inner-text">' # 套上內部去白鉤子
                        for line in lines:
                            s = line.strip()
                            if not s: continue
                            # ✨ 偵測點點或數字列表
                            is_bullet = re.match(r'^([•\-\*]|\d+\.)', s)
                            # 分配對應的 CSS Class 與排版
                            item_class = "list-item" if is_bullet else "normal-item"
                            item_pad = "padding-left:18px;" if is_bullet else ""
                            html_out += f'<div class="{item_class}" style="{item_pad}">{s}</div>'
                        html_out += '</div>'
                        return html_out

                    if isinstance(steps_raw, list) and len(steps_raw) > 0:
                        for s_idx, s in enumerate(steps_raw, 1):
                            c_html = final_hierarchy_render(s.get('content', ''))
                            e_html = final_hierarchy_render(s.get('expected', ''))
                            
                            # 🟢 用完美的 HTML 結構包覆綠線與黑盒子
                            st.markdown(f'''
                                <div class="step-container">
                                    <div style="color:white; font-weight:bold; margin-bottom:8px;">Step {s_idx}:</div>
                                    <div class="content-box">{c_html}</div>
                                    <div style="color:white; font-weight:bold; margin-top:20px; margin-bottom:8px;">Expected:</div>
                                    <div class="content-box">{e_html}</div>
                                </div>
                            ''', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="no-content-hint">💡 (無文字步驟內容)</div>', unsafe_allow_html=True)
                st.markdown("---")

    # 🚀 火箭按鈕
    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
