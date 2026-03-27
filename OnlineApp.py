import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url") or "https://gorun.testrail.io/")
    tr_user = st.text_input("帳號 Email", value=get_val("user") or "ela@intellianalyze.com")
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    p_val = get_val("pid")
    s_val = get_val("sid")
    pid = st.number_input("Project ID", value=int(p_val) if p_val else 10)
    sid = st.number_input("Suite ID", value=int(s_val) if s_val else 10)
    
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases is not None:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | 更新時間：{sync_time}", unsafe_allow_html=True)
        
        # 搜尋功能
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(" ", value=st.session_state.q_text, placeholder="搜尋標題或 ID...", label_visibility="collapsed", key=f"q_{st.session_state.search_key}")
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun()
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                is_match = True
                for t in terms:
                    # 🔒 鎖死幣別精度
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    if len(t) == 3 and t.isalpha():
                        if not any(re.search(rf'\b{re.escape(v)}\b', title) or v == cid for v in variants):
                            is_match = False; break
                    else:
                        if not any(v in title or v == cid for v in variants):
                            is_match = False; break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((path_map.get(c.get('section_id'), ""), c, u))

            if results:
                st.success(f"找到 {len(results)} 筆結果")
                for path, item, u in results:
                    st.write(f"📁 {path} | 👤 {u['name']}")
                    st.markdown(f"#### {item['title']} (#{item['id']})")
                    with st.expander("查看步驟"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.divider()
            else:
                st.warning("🚫 找不到結果")
        else:
            st.info("💡 請輸入關鍵字搜尋...")
    else:
        # 🔥 顯示報錯內容
        st.error(f"❌ 抓取失敗：{sync_time}")
else:
    st.info("👈 請完成側邊欄連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
