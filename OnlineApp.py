import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_strict
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail Search", layout="wide", page_icon="🧪")
apply_custom_style()

# ... (側邊欄連線代碼) ...

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("● 搜尋內容:", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                
                # --- ⚔️ 搜尋邏輯：硬性交集 (AND) ---
                is_match = True
                current_case_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    # 檢查這組詞是否有命中任何欄位 (剝離 HTML 後)
                    hit_title = any(match_strict(title, v) for v in variants)
                    hit_path = any(match_strict(f_path, v) for v in variants)
                    hit_steps = any(match_strict(steps, v) for v in variants)
                    hit_id = (t == str(c.get('id')))

                    if hit_title or hit_path or hit_steps or hit_id:
                        # --- 📈 排序邏輯：權重分配 ---
                        if hit_title: current_case_score += 1000  # 標題命中最高分
                        if hit_path:  current_case_score += 100   # 路徑命中次之
                        if hit_steps: current_case_score += 10    # 內容命中加點分
                    else:
                        is_match = False
                        break # 只要有一組詞沒中，直接淘汰
                
                if is_match:
                    user_id = c.get('created_by')
                    u_cfg = USER_CONFIG.get(user_id, DEFAULT_CONFIG)
                    
                    # 最終分數 = 命中位置分 + 作者權重 + (內容長度獎勵)
                    length_bonus = 50 if len(steps) > 20 else 0
                    final_score = current_case_score + u_cfg['weight'] + length_bonus
                    
                    results.append((final_score, f_path, c, u_cfg))

            # 根據 final_score 由高到低排序
            results.sort(key=lambda x: x[0], reverse=True)

            st.success(f"找到 {len(results)} 筆精確符合案例")
            for score, path, item, u in results:
                # ... (渲染介面，保持妳提供的 CSS 佈局) ...
                st.markdown(f'<div style="color:#adb5bd; font-size:12px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                # (後面渲染代碼略，請套用妳原有的呈現方式)
