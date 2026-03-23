import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 背景與文字基礎 */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 側邊欄輸入框與按鈕 (標記 2, 3) */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        div[data-testid="stSidebar"] .stButton button { 
            background-color: #31333f !important; 
            color: #ffffff !important; 
            border: 1px solid #444c56 !important;
            border-radius: 8px !important;
            width: 100% !important;
        }

        /* 🚀 標記 6: 案例路徑 (淺灰色小字) */
        .case-path-text { 
            font-size: 13px; 
            color: #a1a1a1 !important; 
            margin-bottom: 8px; 
            display: block;
        }

        /* 標記 7, 8: 標題與作者標籤 */
        .author-tag { font-size: 11px; border-radius: 12px; padding: 3px 12px; display: inline-block; margin-left: 10px; font-weight: bold; }
        
        /* 標記 10: Open Case 綠色按鈕 */
        .view-btn { 
            display: inline-block; 
            padding: 6px 16px; 
            background-color: #4CAF50; 
            color: white !important; 
            border-radius: 6px; 
            text-decoration: none; 
            font-size: 13px; 
            font-weight: bold; 
        }

        /* 標記 9: 步驟容器 (帶左側綠線) */
        .step-content-box { color: #ffffff !important; background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; white-space: pre-wrap; }
        .step-item { border-left: 5px solid #4CAF50; padding-left: 20px; margin-bottom: 25px; }

        /* 修正頂部與按鈕 */
        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        button[data-testid="stSidebarCollapse"] { background-color: rgba(255, 255, 255, 0.1) !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)
