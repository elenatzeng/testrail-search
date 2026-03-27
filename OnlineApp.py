import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TR Search Ghost Buster", layout="wide")
apply_custom_style()

# 側邊欄連線區 (保持原樣)...
with st.sidebar:
    st.header("🔐 連線")
    tr_url, tr_user, tr_pw = st.text_input("URL"), st.text_input("Email"), st.text_input("Key", type="password")
    pid, sid = st.number_input("PID", 10), st.number_input("SID", 10)
    if st.button("🔄 刷新數據"): st.cache_data.clear(); st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("● 搜尋關鍵字:", placeholder="例如: CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡【物理隔離】：不准搜尋 c 物件，只把這兩段文字拿出來洗乾淨
                title_clean = str(c.get('title', ''))
                steps_raw = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                
                is_all_passed = True
                debug_info = [] # 儲存抓鬼證據

                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    found_term = False
                    
                    for v in variants:
                        hit_t, msg_t = match_visual_only(title_clean, v)
                        hit_s, msg_s = match_visual_only(steps_raw, v)
                        
                        if hit_t:
                            debug_info.append(f"標題命中: {msg_t}")
                            found_term = True; break
                        if hit_s:
                            debug_info.append(f"步驟內隱藏文字命中: {msg_s}")
                            found_term = True; break
                        if t == cid:
                            debug_info.append(f"Case ID 命中: {t}")
                            found_term = True; break
                    
                    if not found_term:
                        is_all_passed = False; break
                
                if is_all_passed:
                    path = path_map.get(c.get('section_id'), "Unknown")
                    u = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((path, c, u, debug_info))

            st.success(f"找到 {len(results)} 筆案例")
            for path, item, u, debug in results:
                st.markdown(f'<div style="color:#8b949e; font-size:11px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                c1.markdown(f'<h4>{item["title"]} (#{item["id"]})</h4>', unsafe_allow_html=True)
                
                # 💡【靈異現形】：如果搜尋不到卻出現，這行紅字會告訴妳它到底在哪裡抓到的
                st.markdown(f'<p style="color:#FF4B4B; font-size:11px; font-weight:bold;">🔍 偵錯原因: {", ".join(debug)}</p>', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url}/index.php?/cases/view/{item["id"]}" target="_blank" class="view-btn">Open</a></div>', unsafe_allow_html=True)
                with st.expander("預覽內容"): st.write(smart_format(steps_raw))
                st.divider()
