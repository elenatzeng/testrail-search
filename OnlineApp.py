import streamlit as st
import re
from keywords import SEARCH_DICTIONARY
from users import USER_CONFIG, DEFAULT_CONFIG
from style import apply_custom_style
from utils import clean_html, multi_lang_search, fetch_data_from_tr

# 1. 頁面配置
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# 2. 功能函數：強制二次斷行 (處理那些擠在一起的 1. 2. 3.)
def force_step_break(text):
    if not text: return "（無步驟資料）"
    # 🚀 無敵拆分術：只要看到「數字.」或「數字、」就強制換行，不管它前面有沒有空格
    text = re.sub(r'(\d+[\.\、])', r'\n\1', str(text))
    # 清理多餘空行並結合
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return "\n".join(lines)

def clear_search_action():
    st.session_state["search_box"] = ""
    st.session_state.q_text = ""

def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

# 3. 側邊欄
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("🔗 TestRail URL", value=get_val("url"))
    tr_user = st.text_input("📧 帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("🔑 API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("🆔 Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("🆔 Suite ID", value=int(get_val("sid", "10")))

    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")

    if st.button("🔄 強制更新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 4. 主畫面
st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    # 從 utils 獲取數據
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases:
        st.markdown(f'<div class="location-tag">🏢 <b>Project：</b>{p_name} | 📋 <b>Suite：</b>#{suite_id}</div>', unsafe_allow_html=True)
        
        # 搜尋區域
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            query = st.text_input(
                "🔍 精準交集搜尋 (支援繁簡中、英文):", 
                placeholder="多關鍵字請以空格分隔 (交集搜尋)",
                key="search_box"
            )
            st.session_state.q_text = query

        with col_clear:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True) 
            if st.button("🗑️ 清除條件", use_container_width=True, on_click=clear_search_action):
                st.rerun()

        with col_run:
            st.markdown('<p style="margin-bottom: 28px;"></p>', unsafe_allow_html=True)
            if st.button("🔎 重新查詢", use_container_width=True):
                st.rerun()

        # 5. 精準搜尋邏輯與渲染
        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            # 🚀 修正點：分詞搜尋，確保交集
            raw_terms = [t.lower() for t in final_query.strip().split() if len(t) > 1 or t.isalnum()]
            scored_results = []

            for c in all_cases:
                cid = str(c.get('id', ''))
                title = c.get('title', '').lower()
                section_path = str(path_map.get(c.get('section_id'), "")).lower()
                # 撈取所有可搜內容
                steps_raw = str(c.get('custom_steps_separated', '')) + str(c.get('custom_steps', ''))
                searchable_text = (title + section_path + steps_raw).lower()
                
                is_all_match = True
                total_score = 0
                
                # 核心：交集搜尋 (所有關鍵字都必須在內容中)
                for term in raw_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    if not any(word in searchable_text or word in cid for word in expanded):
                        is_all_match = False
                        break
                    else:
                        # 評分加重
                        if any(word in title for word in expanded): total_score += 1000
                        if any(word in section_path for word in expanded): total_score += 500
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    if not u_info.get("is_active"): total_score -= 50000 # 離職員工權重降低
                    scored_results.append((total_score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.write(f"### 🎯 找到 {len(scored_results)} 個案例")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji = "🟢" if u_info.get("is_active") else "🔴"
                author_style = "color: #4CAF50; background: rgba(76,175,80,0.15);" if u_info.get("is_active") else "color: #ff4b4b; background: rgba(255,75,75,0.15);"
                
                # 📂 案例路徑 (修正路徑顯示)
                curr_path = path_map.get(item.get('section_id'), "None")
                st.markdown(f'<span style="font-size:12px; color:#8b949e;">📂 {curr_path}</span>', unsafe_allow_html=True)
                
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">📄 {item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} 👤 {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 📜 測試步驟 (使用無敵斷行術)
                with st.expander("🔽 查看測試步驟"):
                    raw_steps = item.get('custom_steps_separated') or item.get('custom_steps') or []
                    if isinstance(raw_steps, list) and len(raw_steps) > 0:
                        for i, s in enumerate(raw_steps, 1):
                            # 對 content 與 expected 分別強制斷行
                            c_text = force_step_break(clean_html(s.get("content", "")))
                            e_text = force_step_break(clean_html(s.get("expected", "")))
                            
                            st.markdown(f'<div class="step-item"><span style="color:#79c0ff; font-weight:800;">Step {i}:</span><div class="step-content-box" style="white-space: pre-wrap;">{c_text}</div><div style="margin-top:10px;"><span style="color:#8b949e; font-weight:bold;">Expected:</span></div><div class="step-content-box" style="border-left: 2px solid #4CAF50; white-space: pre-wrap;">{e_text}</div></div>', unsafe_allow_html=True)
                    else:
                        # 處理單一欄位步驟
                        full_desc = item.get('custom_steps') or ""
                        st.markdown(f'<div class="step-content-box" style="white-space: pre-wrap;">{force_step_break(clean_html(full_desc))}</div>', unsafe_allow_html=True)
                st.markdown("---")
else:
    st.warning("👈 請在側邊欄輸入連線資訊。")
