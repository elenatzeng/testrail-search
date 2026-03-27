import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

# ✨ 錨點
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄 (連線與強制重刷)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存並強制刷新", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.cache_data.clear() # 🚀 暴力清除快取
        st.success("✅ 已儲存並清空舊資料")
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心搜尋邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 搜尋輸入框
        q_text = st.text_input("● 搜尋內容:", placeholder="搜尋多個詞請用空格，例如：充值 CNY", key="search_bar")

        if q_text:
            # 🎯 拆分關鍵字 (AND 邏輯)
            terms = [t.lower().strip() for t in q_text.split() if t]
            results = []

            for c in all_cases:
                # 🔒 全部轉小寫，確保大小寫不敏感
                title = str(c.get('title', '')).lower()
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                
                is_match = True
                for t in terms:
                    # 📖 呼叫字典聯想詞 (保底一定會包含搜尋詞原文)
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 🔍 只要標題、路徑或 ID 包含這組詞中的「任何一個」，這關就算過
                    # 用最原始的 "in" 比對，不管是 [CNY]、CNY: 還是 (CNY) 通通都能搜到
                    term_hit = False
                    for word in expanded:
                        w = word.lower()
                        if w in title or w in f_path or w == cid:
                            term_hit = True
                            break
                    
                    if not term_hit:
                        is_match = False
                        break
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((f_path, c, u))

            # 顯示結果
            if results:
                for path, item, u in results:
                    st.markdown(f'<div style="color:#adb5bd; margin-top:20px;">📁 {path}</div>', unsafe_allow_html=True)
                    tag = f'<span class="author-tag">🟢 {u["name"]}</span>'
                    c1, c2 = st.columns([8, 1.5])
                    c1.markdown(f'<div style="color:white; font-size:18px; font-weight:bold;">{item.get("title")} (#{item.get("id")}) {tag}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{item.get("id")}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    with st.expander("查閱測試步驟"):
                        st.text(clean_html(item.get('custom_steps') or ""))
                    st.markdown("---")
            else:
                st.markdown('<div style="color:#8b949e; margin-top:20px;">🚫 找不到符合的測試案例。</div>', unsafe_allow_html=True)
    else:
        st.error(f"❌ 抓取失敗，請確認連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
