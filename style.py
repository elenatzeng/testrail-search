import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 全域永夜背景鎖死 */
        .stApp, [data-testid="stSidebar"], .stAppViewContainer {
            background-color: #0d1117 !important;
        }
        
        /* 2. 隱藏右上角設定選單與 Deploy，防止手動切換 */
        header, #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        /* 3. 恢復漂亮的黑盒子與綠線 */
        .step-container {
            border-left: 4px solid #4CAF50;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 30px;
            display: block;
        }
        
        .content-box {
            background: #1c2128;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 18px 20px;
            color: #c9d1d9;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
        }

        /* 4. Expander 標題區美化 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            color: #c9d1d9 !important;
        }
        
        /* 5. 文字顏色修正 */
        h1, h2, h3, p, span, label {
            color: #adb5bd !important;
        }
        
        /* 6. 按鈕與輸入框深色美化 */
        .stTextInput>div>div>input, .stButton>button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        
        /* 7. 移除圖片產生的佔位空白 */
        img { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
