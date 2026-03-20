import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 背景色層次 */
        .stApp { background-color: #0d1117 !important; }
        [data-testid="stSidebar"] { 
            background-color: #161b22 !important; 
            border-right: 1px solid #30363d; 
        }

        /* 🚀 讓輸入框亮起來，不再黑漆漆 */
        .stTextInput input, .stNumberInput input {
            background-color: #0d1117 !important;
            border: 1px solid #444c56 !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }

        /* 側邊欄展開按鈕按鈕救援 */
        button[data-testid="stSidebarCollapse"] {
            background-color: #21262d !important;
            color: white !important;
            top: 10px !important; left: 10px !important; position: fixed !important; z-index: 9999;
        }

        /* 案例卡片與步驟樣式 */
        .step-content-box { color: #ffffff !important; background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; }
        .step-item { border-left: 5px solid #4CAF50; padding-left: 20px; margin-bottom: 30px; }
        .author-tag { font-size: 11px; border-radius: 12px; padding: 3px 12px; display: inline-block; margin-left: 10px; font-weight: bold; }
        .view-btn { display: inline-block; padding: 6px 16px; background-color: #238636; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
        
        /* 隱藏預設頂欄 */
        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)

def show_sleeping_mode():
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>😴 系統午睡中...</h1><p>Elena 正在維修齒輪</p></div>", unsafe_allow_html=True)
    st.stop()
