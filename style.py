import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 基礎背景與文字 */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 輸入框與側邊欄按鈕 */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important; border: 1px solid #30363d !important;
            color: #ffffff !important; border-radius: 8px !important;
        }
        div[data-testid="stSidebar"] .stButton button { 
            background-color: #31333f !important; color: #ffffff !important; 
            border: 1px solid #444c56 !important; border-radius: 8px !important; width: 100% !important;
        }

        /* 檔案路徑與功能按鈕 */
        .case-path-text { font-size: 13px; color: #8b949e !important; margin-bottom: 8px; display: block; }
        .view-btn { 
            display: inline-block; padding: 6px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; 
        }

        /* ✨ Elena 要的圓角發光標籤 (定義基礎結構) */
        .author-tag {
            font-size: 11px;
            font-weight: bold;
            border-radius: 12px; /* 超圓角效果 */
            padding: 2px 10px;
            display: inline-flex;
            align-items: center;
            margin-left: 10px;
            vertical-align: middle;
            background-color: rgba(0, 0, 0, 0.2); /* 稍微深色背景讓框更明顯 */
        }

        /* 測試步驟容器 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #161b22; padding: 15px; 
            border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; white-space: pre-wrap; 
        }
        .step-item { border-left: 4px solid #2ea44f; padding-left: 20px; margin-bottom: 25px; }

        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
