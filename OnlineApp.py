import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="Final Pro Search", layout="wide", page_icon="🧪")
apply_custom_style()

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    if st.button("🔄 刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 鋼鐵檢索")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 **{p_name}** | 更新: `{last_up}`")
        q_text = st.text_input("● 請輸入搜尋內容:", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡 數據隔離：我們只單獨提煉這兩個肉眼欄位，徹底無視路徑與後台 JSON
                title_val = str(c.get('title', ''))
                steps_val = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                # --- ⚔️ 鋼鐵 AND 判定 (每個搜尋詞都必須命中) ---
                all_matched = True
                case_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    # 🔍 搜尋判定：絕對不看路徑，絕對不看原始 JSON 欄位
                    hit_t = any(match_visual_only(title_val, v) for v in variants)
                    hit_s = any(match_visual_only(steps_val, v) for v in variants)
                    hit_i = (t == cid)

                    if hit_t or hit_s or hit_i:
                        if hit_i: case_score += 50000
                        if hit_t: case_score += 10000
                        if hit_s: case_score += 100
                    else:
                        # 只要有一個搜尋詞（如 CNY）沒中，直接出局
                        all_matched = False
                        break 
                
                if all_matched:
                    f_path = str(path_map.get(c.get('section_id'), ""))
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((case_score + u_cfg['weight'], f_path, c, u_cfg))

            # 顯示結果
            results.sort(key=lambda x: x[0], reverse=True)
            st.success(f"找到 {len(results)} 筆精確案例")
            
            for _, path, item, u in results:
                st.markdown(f'<div style="color:#6e7681; font-size:11px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                with st.expander("內容詳情"):
                    st.write(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")
