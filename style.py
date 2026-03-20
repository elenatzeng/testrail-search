import streamlit as st

def apply_style():
    st.markdown("""
        <style>
        /* 整體背景改為深灰藍，增加層次 */
        .stApp { background-color: #0d1117 !important; }
        
        /* 側邊欄改為稍淺的灰色，讓輸入框跳出來 */
        [data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d; }
        
        /* 讓輸入框有亮色邊框 */
        .stTextInput input, .stNumberInput input {
            background-color: #0d1117 !important;
            border: 1px solid #444c56 !important;
            color: #c9d1d9 !important;
        }
        
        /* 按鈕視覺強化 */
        div[data-testid="stSidebar"] .stButton button {
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%) !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* 側邊欄展開按鈕固定 */
        button[data-testid="stSidebarCollapse"] {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            top: 10px !important; left: 10px !important; position: fixed !important; z-index: 999;
        }
        </style>
    """, unsafe_allow_html=True)