import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)
apply_custom_style()

# ✨ 【停機坪】
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄守護
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases is not None:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                " ", 
                value=st.session_state.q_text, 
                placeholder="請輸入關鍵字查詢，多個關鍵字請以空格隔開", 
                label_visibility="collapsed",
                key=f"search_input_{st.session_state.search_key}"
            )
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): 
                st.session_state.q_text = ""; st.session_state.search_key += 1; st.rerun() 
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            # 🎯 拆分輸入的關鍵字 (交集查詢的核心)
            terms = [t.lower().strip() for t in st.session_state.q_text.strip().split() if t]
            results = []

            for c in all_cases:
                title = str(c.get('title', '')).lower()
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                
                is_match = True
                # 🛠️ AND 邏輯：檢查輸入的每一個字組
                for t in terms:
                    # 📖 呼叫字典聯想：若字典有則聯想，若無則返回原文 [t]
                    expanded_words = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    term_hit = False
                    for word in expanded_words:
                        word = word.lower()
                        # 🔒 幣別鎖死 (3碼英文才用正則，否則用一般包含)
                        if len(word) == 3 and word.isalpha():
                            if re.search(rf'\b{re.escape(word)}\b', title) or \
                               re.search(rf'\b{re.escape(word)}\b', f_path) or \
                               word == cid:
                                term_hit = True; break
                        else:
                            if word in title or word in f_path or word == cid:
                                term_hit = True; break
                    
                    if not term_hit:
                        is_match = False; break # 只要有一個詞組沒中就淘汰
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((f_path, c, u))

            if results:
                for path, item, u in results:
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; color:white; font-size:20px; font-weight:bold;">{item.get("title")} (#{item.get("id")}){tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'<a href="{tr_url.strip("/")}/index.php?/cases/view/{item.get("id")}" target="_blank" class="view-btn">📖 Open Case</a>', unsafe_allow_html=True)
                    with st.expander("查閱測試步驟"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.markdown("---")
            else:
                st.markdown('<div style="color:#8b949e; margin-top:20px; padding-left:5px;">🚫 找不到符合的案例。</div>', unsafe_allow_html=True)
    else:
        st.error(f"❌ 抓取失敗：{sync_time}")
else:
    st.info("👈 請先在左側完成連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
