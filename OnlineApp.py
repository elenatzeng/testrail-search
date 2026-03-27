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
        q_text = st.text_input("● 搜尋內容 (幣別鎖死模式):", placeholder="例如: 充值 CNY")
        
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                
                # --- ⚔️ 搜尋邏輯：硬性交集 (AND) ---
                is_match = True
                case_score = 0
                
                for t in terms:
                    # 💡 這裡會根據「幣別鎖死」邏輯回傳結果
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 檢查各個欄位 (只看剝離 HTML 後的純文字)
                    hit_title = any(match_strict(title, v) for v in variants)
                    hit_path  = any(match_strict(f_path, v) for v in variants)
                    hit_steps = any(match_strict(steps, v) for v in variants)
                    hit_id    = (t == cid)

                    if hit_title or hit_path or hit_steps or hit_id:
                        # --- 📈 排序權重：分層打分 ---
                        if hit_title: case_score += 10000  # 標題命中最高權重
                        if hit_path:  case_score += 1000   # 路徑其次
                        if hit_steps: case_score += 100    # 內容再次之
                        if hit_id:    case_score += 50000  # 直接搜 ID 必排第一
                    else:
                        is_match = False
                        break # 任何一組詞沒中，直接淘汰
                
                if is_match:
                    # 取得作者配置
                    user_id = c.get('created_by')
                    u_cfg = USER_CONFIG.get(user_id, DEFAULT_CONFIG)
                    
                    # 最終得分 = 命中分數 + 作者權重 + 長度獎勵
                    length_bonus = 50 if len(steps) > 50 else 0
                    final_score = case_score + u_cfg['weight'] + length_bonus
                    
                    results.append((final_score, f_path, c, u_cfg))

            # --- 🏆 執行排序 ---
            results.sort(key=lambda x: x[0], reverse=True)

            # --- 渲染介面 ---
            st.success(f"找到 {len(results)} 筆精確案例")
            for score, path, item, u in results:
                cid_str = str(item.get('id'))
                st.markdown(f'<div style="color:#adb5bd; font-size:11px; margin-top:15px;">📁 {path}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_class = "status-active" if u["is_active"] else "status-inactive"
                icon = "🟢" if u["is_active"] else "🔴"
                
                c1.markdown(f'''
                    <div style="display:flex; align-items:center;">
                        <h4 style="margin:0;">{item["title"]} (#{cid_str})</h4>
                        <span class="author-tag {tag_class}">{icon} {u["name"]}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid_str}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("查看內容預覽"):
                    st.write(smart_format(steps))
                st.markdown("---")
