import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪", initial_sidebar_state="expanded")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

# 2. 側邊欄 (維持現狀...)
# ... 這裡保留妳目前能正常運作的連線設定代碼 ...

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
# (假設已成功獲取 results)
if 'results' in locals() or 'results' in globals():
    for _, item, u in results:
        cid = str(item.get('id'))
        # 目錄
        st.markdown(f'<div style="font-size:13px; color:#8b949e; margin-top:20px; margin-bottom:5px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
        
        tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
        c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
        
        # ✨ 【修正】標題 20px，字體加粗，顏色亮白
        c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:700; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
        
        # ✨ 綠色按鈕
        c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
        
        with st.expander("查閱測試步驟", expanded=False):
            steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
            
            def render_list_logic(text):
                if not text: return "(無內容)"
                lines = str(text).splitlines()
                html_out = '<div>'
                for line in lines:
                    s = line.strip()
                    if not s: continue
                    is_list = re.match(r'^([•\-\*]|\d+\.)', s)
                    className = "list-item" if is_list else ""
                    html_out += f'<div class="{className}">{s}</div>'
                html_out += '</div>'
                return html_out

            if isinstance(steps_data, list):
                for s_idx, s in enumerate(steps_data, 1):
                    st.markdown(f'''
                        <div style="border-left:4px solid #2ea44f; padding-left:18px; margin-bottom:25px;">
                            <div style="color:#8b949e; font-size:13px; font-weight:500; margin-bottom:8px;">Step {s_idx}:</div>
                            <div class="content-box">{render_list_logic(s.get('content'))}</div>
                            <div style="color:#8b949e; font-size:13px; font-weight:500; margin-top:15px; margin-bottom:8px;">Expected:</div>
                            <div class="content-box">{render_list_logic(s.get('expected'))}</div>
                        </div>
                    ''', unsafe_allow_html=True)
        st.markdown('<div style="border-bottom:1px solid #30363d; margin: 15px 0;"></div>', unsafe_allow_html=True)

# 火箭按鈕
st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
