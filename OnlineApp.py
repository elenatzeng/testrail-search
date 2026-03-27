import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TR Search Final Check", layout="wide")
apply_custom_style()

# ... (側邊欄連線代碼省略，保持原樣) ...

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("● 搜尋內容 (偵錯模式):", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title = str(c.get('title', ''))
                steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                f_path = str(path_map.get(c.get('section_id'), ""))
                
                is_all_passed = True
                match_reasons = [] # 儲存抓鬼證據

                # --- ⚔️ 嚴格 AND 邏輯 ---
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 檢查這組詞是否命中 (完全不看 f_path)
                    hit_t = any(match_visual_only(title, v) for v in variants)
                    hit_s = any(match_visual_only(steps, v) for v in variants)
                    hit_i = (t == cid)

                    if hit_t or hit_s or hit_i:
                        # 記錄是誰命中的，方便抓鬼
                        if hit_t: match_reasons.append(f"標題命中 '{t}'")
                        if hit_s: match_reasons.append(f"內容命中 '{t}'")
                        if hit_i: match_reasons.append(f"ID 命中 '{t}'")
                    else:
                        is_all_passed = False # 只要一個詞沒中，直接淘汰
                        break
                
                if is_all_passed:
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((f_path, c, u_cfg, match_reasons))

            st.success(f"找到 {len(results)} 筆案例")
            for path, item, u, reasons in results:
                st.markdown(f'<div style="color:#6e7681; font-size:11px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag = "status-active" if u["is_active"] else "status-inactive"
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]}) <span class="author-tag {tag}">{u["name"]}</span></h4>', unsafe_allow_html=True)
                
                # 💡 這裡會告訴妳為什麼它會出現在結果裡！
                st.markdown(f'<p style="color:#FF4B4B; font-size:11px; font-weight:bold;">🔍 抓鬼證據: {", ".join(set(reasons))}</p>', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                with st.expander("內容預覽"): st.write(smart_format(steps))
                st.markdown("---")
