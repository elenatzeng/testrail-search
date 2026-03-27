import streamlit as st
from style import apply_custom_style
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 初始化
st.set_page_config(page_title="TestRail Search Pro", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

# 2. 側邊欄與連線
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("Project ID", value=10)
    sid = st.number_input("Suite ID", value=10)
    
    st.divider()
    bad_id = st.text_input("🚫 排除 ID (黑名單)", placeholder="例如: 31735")
    blacklist = [i.strip() for i in bad_id.split(",") if i.strip()]

    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 鋼鐵檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        st.markdown(f"📍 **{p_name}** | Suite：#{sid}")
        q_text = st.text_input("● 搜尋關鍵字 (多詞請用空格分開):", placeholder="例如: 充值 CNY")
        
        if q_text:
            # --- ⚔️ 分詞處理 (多詞交集核心) ---
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []

            for c in all_cases:
                cid = str(c.get('id'))
                if cid in blacklist: continue # 黑名單跳過
                
                title = str(c.get('title', ''))
                f_path = str(path_map.get(c.get('section_id'), ""))
                steps = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                
                # --- 核心邏輯：所有輸入詞都必須命中才放行 ---
                is_all_passed = True
                total_score = 0
                
                for t in terms:
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 檢查這組同義詞 (或鎖死的幣別) 是否出現在這筆 Case
                    hit_title = any(match_visual_only(title, v) for v in variants)
                    hit_path  = any(match_visual_only(f_path, v) for v in variants)
                    hit_steps = any(match_visual_only(steps, v) for v in variants)
                    hit_id    = (t == cid)

                    if hit_title or hit_path or hit_steps or hit_id:
                        # 計算權重分數
                        if hit_id:    total_score += 50000 # ID 最優先
                        if hit_title: total_score += 10000 # 標題其次
                        if hit_path:  total_score += 1000
                        if hit_steps: total_score += 100
                    else:
                        is_all_passed = False # 只要有一組關鍵字沒中，整筆 Case 出局
                        break
                
                if is_all_passed:
                    u_info = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    # 分數 = 命中權重 + 作者權重 + 長度加乘
                    final_score = total_score + u_info.get('weight', 0) + (50 if len(steps) > 50 else 0)
                    results.append((final_score, f_path, c, u_info))

            # --- 排序與顯示 ---
            results.sort(key=lambda x: x[0], reverse=True)
            st.success(f"找到 {len(results)} 筆完全符合條件之案例")
            
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
                
                with st.expander("查看內容"):
                    st.write(smart_format(str(item.get('custom_steps') or item.get('custom_steps_separated'))))
                st.markdown("---")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
