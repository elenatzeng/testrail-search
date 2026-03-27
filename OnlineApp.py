import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TR Search Final", layout="wide", page_icon="🧪")
apply_custom_style()

# 側邊欄連線區
with st.sidebar:
    st.header("🔐 TestRail 設定")
    tr_url = st.text_input("URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    st.divider()
    if st.button("🔄 刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 鋼鐵檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 **{p_name}** | 更新時間: `{last_up}`")
        q_text = st.text_input("● 搜尋內容 (紅框精確版):", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡 絕對隔離：我們「只」把紅框圈到的文字拿出來，不准程式看 JSON 的其他欄位
                target_title = str(c.get('title', ''))
                target_steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                is_all_passed = True
                case_score = 0
                
                # --- ⚔️ 嚴格 AND 邏輯 ---
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 搜尋權限：只准看標題、內容、ID。不看路徑，不看後台隱藏代碼
                    h_title = any(match_visual_only(target_title, v) for v in variants)
                    h_steps = any(match_visual_only(target_steps, v) for v in variants)
                    h_id    = (t == cid)

                    if h_title or h_steps or h_id:
                        # 權重計分
                        if h_id:    case_score += 50000
                        if h_title: case_score += 10000
                        if h_steps: case_score += 100
                    else:
                        # 只要有一個詞沒中，這筆 Case 直接淘汰
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    f_path = str(path_map.get(c.get('section_id'), ""))
                    u_cfg = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    results.append((case_score + u_cfg['weight'], f_path, c, u_cfg))

            # 顯示結果
            results.sort(key=lambda x: x[0], reverse=True)
            st.success(f"找到 {len(results)} 筆完全符合之案例")
            
            for _, path, item, u in results:
                st.markdown(f'<div style="color:#6e7681; font-size:11px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_style = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag_style}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                with st.expander("查看步驟詳情"):
                    st.write(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")

st.markdown('<div style="text-align:center; padding: 20px; color: #8b949e;">End of Results</div>', unsafe_allow_html=True)
