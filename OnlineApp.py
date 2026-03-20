# 3. 側邊欄記憶與連線設定
def get_val(key, default=""):
    # 優先從網址讀，再從 session 讀
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

with st.sidebar:
    st.header("🔐 連線設定")
    
    # 🔄 1. 強制更新按鈕 (放在最上面，確保隨時可見)
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---") # 分隔線
    
    tr_url = st.text_input("TestRail URL", value=get_val("url"), key="input_url")
    tr_user = st.text_input("帳號 Email", value=get_val("user"), key="input_user")
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"), key="input_pw")
    
    # 數字輸入框增加 try-except 避免型別錯誤
    try:
        p_id_val = int(get_val("pid", "1"))
        s_id_val = int(get_val("sid", "1"))
    except:
        p_id_val, s_id_val = 1, 1

    project_id = st.number_input("Project ID", value=p_id_val, key="input_pid")
    suite_id = st.number_input("Suite ID", value=s_id_val, key="input_sid")
    
    # 更新 Session
    st.session_state.update({
        "store_url": tr_url, 
        "store_user": tr_user, 
        "store_pw": tr_pw, 
        "store_pid": project_id, 
        "store_sid": suite_id
    })

    # 💾 2. 儲存按鈕
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存至 URL")
        st.balloons()
