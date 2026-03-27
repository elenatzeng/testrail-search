import streamlit as st
import re
import os
import sys

# 🛡️ 1. 導入設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

try:
    from style import apply_custom_style
    from utils import clean_html, fetch_data_from_tr, multi_lang_search
    from users import USER_CONFIG, DEFAULT_CONFIG
    from keywords import SEARCH_DICTIONARY
except Exception as e:
    st.error(f"導入失敗: {e}"); st.stop()

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄保持原樣
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    if st.button("💾 儲存設定", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, _, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="搜尋多個關鍵字 (例如: 充值 CNY)...", key=f"s_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            # 拆分關鍵字
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 核心邏輯：AND (交集) 過濾 ---
                match_count = 0
                total_bonus = 0
                
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    in_title = any(w in title for w in exp) or (t == cid)
                    in_path = any(w in f_path for w in exp)
                    in_content = any(w in steps_str for w in exp)
                    
                    # 💡 只要該關鍵字在標題、路徑、內容中任一處出現，就算該詞命中
                    if in_title or in_path or in_content:
                        match_count += 1
                        # 分數計算：標題命中權重最高
                        if in_title: total_bonus += 2000
                        elif in_path: total_bonus += 500
                        else: total_bonus += 100
                
                # 🛡️ 只有當所有關鍵字都命中時，才放入結果清單 (交集邏輯)
                if match_count == len(terms):
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    u_weight = u.get("weight", 0)
                    
                    # 💡 增加每個步驟的加分 (每個步驟加 500 分，強行壓制雷包)
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    step_bonus = step_count * 500 

                    final_score = total_bonus + step_bonus + u_weight
                    sort_key = (-final_score, f_path, cid)
                    results.append((sort_key, path_map.get(c.get('section_id'), ""), c, u))

            results.sort(key=lambda x: x[0])

            # --- 渲染區 ---
            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px;">🚫 找不到同時符合所有關鍵字的測試案例。</div>', unsafe_allow_html=True)
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    color = "#32CD32" if is_active else "#FF4B4B"
                    bg = "rgba(50, 205, 50, 0.1)" if is_active else "rgba(255, 75, 75, 0.2)"
                    
                    tag_html = f'''
                        <span style="color:{color} !important; border:2px solid {color} !important; 
                        background:{bg} !important; padding:2px 12px; border-radius:20px; 
                        font-size:12px; font-weight:bold; margin-left:10px; display:inline-flex; align-items:center;">
                        {'🟢' if is_active else '🔴'} {u["name"]}
                        </span>
                    '''
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟"):
                        st.write(item.get('custom_steps') or item.get('custom_steps_separated'))
