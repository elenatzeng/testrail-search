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

# 2. 側邊欄 (略，維持原樣)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=st.query_params.get("url", ""))
    tr_user = st.text_input("帳號 Email", value=st.query_params.get("user", ""))
    tr_pw = st.text_input("API Key", type="password", value=st.query_params.get("pw", ""))
    pid = st.number_input("Project ID", value=int(st.query_params.get("pid", 10)))
    sid = st.number_input("Suite ID", value=int(st.query_params.get("sid", 10)))
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases is not None:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span>", unsafe_allow_html=True)
        
        q_text = st.text_input("● 搜尋內容:", placeholder="例如：充值 CNY", key="main_search")

        if q_text:
            terms = [t.lower().strip() for t in q_text.split() if t]
            results = []

            for c in all_cases:
                title = str(c.get('title', '')).lower()
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                
                is_match = True
                for t in terms:
                    # 📖 取得聯想詞 (若字典沒這字，res 就只會包含 [t])
                    expanded_words = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    term_hit = False
                    for word in expanded_words:
                        w = word.lower()
                        # 🔒 妳要求的：精確完整比對 (\b 代表單字邊界)
                        # 這樣搜尋 cny 就不會搜到 currency
                        if re.search(rf'\b{re.escape(w)}\b', title) or \
                           re.search(rf'\b{re.escape(w)}\b', f_path) or w == cid:
                            term_hit = True; break
                        # 補充：如果是非英文（如中文），re.search 依然有效
                        elif w in title or w in f_path:
                            term_hit = True; break
                    
                    if not term_hit:
                        is_match = False; break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((f_path, c, u))

            if results:
                for path, item, u in results:
                    st.markdown(f'<div style="color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="color:white; font-size:18px; font-weight:bold;">{item["title"]} (#{item["id"]}) <span style="border:1px solid #32CD32; border-radius:10px; padding:0 10px; font-size:12px;">{u["name"]}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<a href="{tr_url.strip("/")}/index.php?/cases/view/{item["id"]}" target="_blank" style="color:#2ea44f; text-decoration:none;">📖 Open Case</a>', unsafe_allow_html=True)
                    with st.expander("查閱步驟"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.markdown("---")
            else:
                st.warning("🚫 找不到符合的案例。")
    else:
        st.error(f"❌ 抓取失敗：{sync_time}")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端">🚀</a>', unsafe_allow_html=True)
