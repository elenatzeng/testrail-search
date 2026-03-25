import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* ✨ Elena 要的膠囊弧形發光標籤 (定義基礎結構) */
        .author-tag {
            font-size: 11px;
            font-weight: bold;
            border-radius: 20px !important; /* 💡 超圓角效果，膠囊狀 */
            padding: 2px 14px; /* 微調內距 */
            display: inline-flex;
            align-items: center;
            margin-left: 10px;
            vertical-align: middle;
            border: 2px solid !important; /* 💡 強制加粗紮線外框 */
            background-color: rgba(0, 0, 0, 0.2); /* 稍微深色背景讓框更明顯 */
        }

        /* 輸入框樣式 */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important; border: 1px solid #30363d !important;
            color: #ffffff !important; border-radius: 8px !important;
        }

        /* 按鈕基礎樣式 */
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

        /* 漂亮步驟容器 (不帶白色背景) */
        .step-content-box { 
            color: #c9d1d9 !important; background: #161b22; padding: 15px; 
            border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; white-space: pre-wrap; 
        }

        /* 測試步驟容器 */
        .step-item { border-left: 4px solid #2ea44f; padding-left: 20px; margin-bottom: 25px; }

        /* 🚀 活力橘回到頂端按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 30px; width: 48px; height: 48px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            text-decoration: none !important; transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center; font-size: 20px;
        }
        .scroll-to-top:hover { transform: translateY(-5px); background-color: #e67600; }

        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
