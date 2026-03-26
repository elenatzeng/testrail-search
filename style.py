import streamlit as st

def apply_custom_style():
    # 🔥 終極黑科技：強制注入全域變數，徹底封鎖 Light Mode
    st.markdown("""
        <style>
        /* 1. 隱藏右上角選單與工具列，防止被手動切換模式 */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* 2. 強制鎖死全域背景與文字顏色 (加上 !important 確保最高優先級) */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
        }

        /* 3. 針對 Expander 與黑盒子鎖死深色 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #c9d1d9 !important;
        }
        .streamlit-expanderContent {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
        }
        
        /* 4. 輸入框與按鈕鎖死 */
        input, .stTextInput>div>div>input {
            background-color: #161b22 !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
        }
        
        button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
        }

        /* 5. 修正文字標籤顏色 */
        label, .stMarkdown p, span {
            color: #adb5bd !important;
        }
        
        /* 6. 靈魂綠線樣式加強 */
        [style*="border-left:4px solid #4CAF50"] {
            margin-top: 5px !important;
            border-left-color: #4CAF50 !important;
        }
        </style>
    """, unsafe_allow_html=True)
