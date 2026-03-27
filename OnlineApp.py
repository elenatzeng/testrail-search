import streamlit as st
from utils import fetch_data_from_tr, smart_format

# 頁面基本設定
st.set_page_config(page_title="TestRail 檢索系統 (昨日穩定版)", layout="wide")

st.info("🕒 目前運行：昨日穩定修復版 (已補齊輸入標籤)")

with st.sidebar:
    st.header("🔐 連線設定")
    # 🛡️ 這裡的標籤文字全部補齊，防止「Oh no」崩潰
    tr_url = st.text_input("TestRail 網址", value="https://gorun.testrail.io/")
    tr_user = st.text_input("登入 Email", value="ela@intellianalyze.com")
    tr_pw = st.text_input("API Key 密鑰", type="password")
    pid = st.number_input("專案 ID (PID)", value=10)
    sid = st.number_input("測試集 ID (SID)", value=10)
    
    if st.button("🔄 刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, last_up, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.write(f"✅ 已連線到專案：{p_name}")
        # 搜尋框標籤
        q = st.text_input("🔍 輸入關鍵字搜尋標題：", value="")
        
        if q:
            # 使用昨天的簡單搜尋邏輯
            results = [c for c in all_cases if q.lower() in str(c.get('title', '')).lower()]
            
            st.success(f"找到 {len(results)} 筆結果")
            for item in results:
                st.markdown(f"---")
                st.markdown(f"#### {item['title']} (#{item['id']})")
                with st.expander("查看步驟詳情"):
                    # 顯示步驟
                    steps = item.get('custom_steps') or item.get('custom_steps_separated') or "無內容"
                    st.text(smart_format(steps))
    else:
        st.error(f"連線失敗或資料為空。錯誤訊息：{last_up}")
