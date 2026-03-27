import streamlit as st
import re
from utils import smart_format, fetch_data_from_tr, multi_lang_search, match_visual_only
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="GitHub Ghost Buster", layout="wide")

# 🔥 只有新版才會出現這行！沒看到代表妳沒存檔成功！
st.error("💖 妹妹加油！這是最新的【抓鬼偵錯版】，看到這行代表妳終於存檔成功了！")

with st.sidebar:
    st.header("🔐 GitHub 連線中心")
    tr_url = st.text_input("URL", value="https://gorun.testrail.io/")
    tr_user = st.text_input("Email", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API Key", type="password")
    pid = st.number_input("PID", 10)
    sid = st.number_input("SID", 10)
    if st.button("🔄 徹底清除數據快取"):
        st.cache_data.clear()
        st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    if all_cases:
        q_text = st.text_input("🔍 搜尋 (請輸入 VND 或 CNY 測試):")
        if q_text:
            terms = [t.lower() for t in q_text.strip().split() if t]
            results = []
            for c in all_cases:
                # 💡 絕對隔離，只抽這兩塊文字
                t_raw = str(c.get('title', ''))
                s_raw = str(c.get('custom_steps') or c.get('custom_steps_separated') or "")
                cid = str(c.get('id'))
                is_all_passed = True
                debug_info = []

                for t in terms:
                    # 🛡️ 核心防禦：如果是 3 碼英文，鎖死不查字典！
                    variants = [t] if (len(t) == 3 and t.isalpha()) else multi_lang_search(t, SEARCH_DICTIONARY)
                    found = False
                    for v in variants:
                        hit_t, msg_t = match_visual_only(t_raw, v)
                        hit_s, msg_s = match_visual_only(s_raw, v)
                        if hit_t: 
                            debug_info.append(f"標題命中({v})")
                            found = True; break
                        if hit_s: 
                            debug_info.append(f"步驟命中({v})")
                            found = True; break
                        if t == cid: 
                            debug_info.append("ID命中")
                            found = True; break
                    if not found:
                        is_all_passed = False; break
                
                if is_all_passed:
                    path = path_map.get(c.get('section_id'), "Unknown")
                    u = USER_CONFIG.get(c.get('created_by', 0), DEFAULT_CONFIG)
                    results.append((path, c, u, debug_info))

            st.success(f"找到 {len(results)} 筆案例")
            for path, item, u, debug in results:
                st.write(f"📁 {path}")
                st.markdown(f"#### {item['title']} (#{item['id']})")
                # 🔥 這行紅字如果沒出現，代表妳還在跑舊版
                st.markdown(f'<p style="color:red; font-weight:bold;">🔍 為什麼會出現？ -> {", ".join(debug)}</p>', unsafe_allow_html=True)
                with st.expander("查看詳情"):
                    st.write(smart_format(s_raw))
                st.divider()
