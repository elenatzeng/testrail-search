import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_strict_visual
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TR Search Pro", layout="wide")
apply_custom_style()

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    
    st.divider()
    bad_id = st.text_input("🚫 排除特定 ID (逗號隔開)", value="")
    blacklist = [i.strip() for i in bad_id.split(",") if i.strip()]

    if st.button("🔄 刷新數據"): st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 精確檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("● 搜尋內容:", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                if cid in blacklist: continue
                
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                
                # --- ⚔️ 鋼鐵交集 (AND) ---
                is_match = True
                final_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    h_title = any(match_strict_visual(title, v) for v in variants)
                    h_path  = any(match_strict_visual(f_path, v) for v in variants)
                    h_steps = any(match_strict_visual(steps, v) for v in variants)
                    h_id    = (t == cid)

                    if h_title or h_path or h_steps or h_id:
                        # 分層權重
                        if h_id:    final_score += 50000
                        if h_title: final_score += 10000
                        if h_path:  final_score += 1000
                        if h_steps: final_score += 100
                    else:
                        is_match = False # 一票否決
                        break
                
                if is_match:
                    u_cfg = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    score = final_score + u_cfg['weight']
                    results.append((score, f_path, c, u_cfg))

            results.sort(key=lambda x: x[0], reverse=True)
            
            st.success(f"找到 {len(results)} 筆精確符合案例")
            for _, path, item, u in results:
                st.markdown(f'<div style="color:#6e7681; font-size:12px; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_class = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag_class}">{"🟢" if u["is_active"] else "🔴"} {u["name"]}</span></h4>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                with st.expander("預覽內容"): st.write(smart_format(steps))
                st.markdown("---")
