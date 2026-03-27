import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TR Search Pro", layout="wide", page_icon="🧪")
apply_custom_style()

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 鋼鐵檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("● 搜尋內容 (嚴格交集模式):", placeholder="例如: 充值 CNY")
        
        if q_text:
            # 1. 拆分詞彙 (AND 邏輯的基礎)
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                # 💡 只抓紅框欄位：標題與內容
                visual_data = {
                    "title": str(c.get('title', '')),
                    "steps": str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                }
                f_path = str(path_map.get(c.get('section_id'), ""))
                cid = str(c.get('id'))
                
                # --- ⚔️ 嚴格交集判定 (必須滿足所有詞) ---
                is_all_passed = True
                case_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 搜尋判定：只准在「標題」和「內容」裡找！絕不准看 Folder 名稱 (f_path)
                    h_title = any(match_visual_only(visual_data["title"], v) for v in variants)
                    h_steps = any(match_visual_only(visual_data["steps"], v) for v in variants)
                    h_id    = (t == cid)

                    # 只要標題或內容其中一個有中，這一組詞就算過關
                    if h_title or h_steps or h_id:
                        # 權重計算
                        if h_id:    case_score += 50000
                        if h_title: case_score += 10000
                        if h_steps: case_score += 100
                        
                        # 路徑只負責「排序加分」，不准決定生死
                        if any(match_visual_only(f_path, v) for v in variants):
                            case_score += 1000 
                    else:
                        # 💡 關鍵：只要有一個搜尋詞在標題和內容都找不到，直接出局 (AND 邏輯)
                        is_all_passed = False
                        break
                
                if is_all_passed:
                    u_cfg = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((case_score + u_cfg.get('weight', 0), f_path, c, u_cfg))

            # 排序
            results.sort(key=lambda x: x[0], reverse=True)
            
            st.success(f"找到 {len(results)} 筆完全符合紅框標註之案例")
            for _, path, item, u in results:
                st.markdown(f'<div style="color:#6e7681; font-size:11px; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_class = "status-active" if u.get("is_active") else "status-inactive"
                icon = "🟢" if u.get("is_active") else "🔴"
                
                c1.markdown(f'''
                    <div style="display:flex; align-items:center;">
                        <h4 style="margin:0;">{item.get("title")} (#{item.get("id")})</h4>
                        <span class="author-tag {tag_class}">{icon} {u["name"]}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{item.get("id")}" target="_blank" class="view-btn">📖 Open</a></div>', unsafe_allow_html=True)
                
                with st.expander("查看步驟詳情"):
                    st.write(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")
