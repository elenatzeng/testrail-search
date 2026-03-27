import streamlit as st
import re
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 頁面基本設定
st.set_page_config(page_title="TestRail 精確檢索", layout="wide", page_icon="🧪")
apply_custom_style()

# 🛡️ 版本檢測標誌
st.markdown('<div style="background-color:#ff4b4b; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold;">🚀 目前運行：【2026 最終鋼鐵鎖死版】</div>', unsafe_allow_html=True)

# 側邊欄：連線資訊
with st.sidebar:
    st.header("🔐 TestRail 連線")
    tr_url = st.text_input("URL", value="https://gorun.testrail.io/")
    tr_user = st.text_input("Email", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    st.divider()
    if st.button("🔄 強制刷新所有數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 主程式邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.info(f"📍 專案：{p_name} | 最後更新：{last_up}")
        q_text = st.text_input("● 搜尋關鍵字 (支援多詞搜尋，例如: 充值 CNY):", placeholder="在此輸入...")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡 數據隔離：只提煉標題與步驟，不准搜尋原始 JSON
                t_content = str(c.get('title', ''))
                s_content = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                # --- ⚔️ 嚴格 AND 邏輯 ---
                is_all_passed = True
                case_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 搜尋判定：標題、步驟內容、ID 必須有一個中
                    hit_t = any(match_visual_only(t_content, v) for v in variants)
                    hit_s = any(match_visual_only(s_content, v) for v in variants)
                    hit_i = (t == cid)

                    if hit_t or hit_s or hit_i:
                        # 計算權重排序
                        if hit_i: case_score += 50000
                        if hit_t: case_score += 10000
                        if hit_s: case_score += 100
                    else:
                        # 只要有一個詞沒中，整筆 Case 出局
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    f_path = str(path_map.get(c.get('section_id'), "Unknown"))
                    u_cfg = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    results.append((case_score + u_cfg['weight'], f_path, c, u_cfg))

            # 顯示結果排序
            results.sort(key=lambda x: x[0], reverse=True)
            st.success(f"找到 {len(results)} 筆完全匹配的案例")
            
            for _, path, item, u in results:
                st.markdown(f'<div style="color:#8b949e; font-size:11px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                
                tag_class = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag_class}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                
                with st.expander("查看步驟內容"):
                    st.text(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")
