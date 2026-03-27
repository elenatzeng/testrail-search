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
    pid_v = get_val("pid")
    sid_v = get_val("sid")
    pid = st.number_input("Project ID (PID)", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID (SID)", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    # 這裡會回傳資料，或者錯誤訊息
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 專案：<span style='color:white; font-weight:bold;'>{p_name}</span> | 更新時間：{sync_time}", unsafe_allow_html=True)
        
        # 搜尋功能開始
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        if "search_key" not in st.session_state: st.session_state.search_key = 0

        col_s, col_c = st.columns([8, 2], vertical_alignment="bottom")
        with col_s:
            q_input = st.text_input("搜尋關鍵字 (例如: cny)", value=st.session_state.q_text, key=f"s_{st.session_state.search_key}")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除", use_container_width=True):
                st.session_state.q_text = ""
                st.session_state.search_key += 1
                st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            
            for c in all_cases:
                title = str(c.get('title', '')).lower()
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                
                is_match = True
                for t in terms:
                    # 抓取聯想詞
                    variants = multi_lang_search(t, SEARCH_DICTIONARY)
                    # 🔒 鎖死幣別精度 (3碼英文)
                    if len(t) == 3 and t.isalpha():
                        # 使用正則表達式鎖死，確保 cny 不會抓到 currency
                        if not any(re.search(rf'\b{re.escape(v)}\b', title) or v == cid for v in variants):
                            is_match = False; break
                    else:
                        # 普通搜尋 (包含即可)
                        if not any(v in title or v in f_path or v == cid for v in variants):
                            is_match = False; break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((f_path, c, user_info))

            if results:
                st.success(f"找到 {len(results)} 筆案例")
                for path, item, u in results:
                    st.write(f"📁 {path}")
                    st.markdown(f"#### {item['title']} (#{item['id']})")
                    with st.expander("查看步驟"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.divider()
            else:
                st.warning("🚫 找不到匹配結果")
        else:
            st.info("💡 請輸入關鍵字開始搜尋...")
    else:
        # 🔥 如果資料抓不到，這裡會顯示原因
        st.error(f"❌ 無法從 TestRail 抓取資料。請檢查：\n1. PID ({pid}) / SID ({sid}) 是否正確？\n2. API Key 是否有效？\n3. TestRail 網址是否正確？")
else:
    st.warning("👈 請先在左側填寫 URL、Email 和 API Key。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
