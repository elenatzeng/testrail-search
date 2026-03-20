import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 整體背景與文字 */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 🚀 修正側邊欄開關按鈕位置 */
        button[data-testid="stSidebarCollapse"] {
            background-color: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            top: 10px !important; left: 10px !important; position: fixed !important; z-index: 999999 !important;
        }

        /* 隱藏頂部裝飾條 */
        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }

        /* 還原按鈕樣式 (對齊文件標記 1, 2) */
        div[data-testid="stSidebar"] .stButton button { 
            background-color: #31333f !important; 
            color: #ffffff !important; 
            border: 1px solid #444c56 !important;
            width: 100% !important; 
            font-weight: 600 !important; 
            border-radius: 8px !important;
        }
        
        /* 案例卡片與步驟樣式 (對齊標記 4, 5) */
        .step-content-box { color: #ffffff !important; background: #1c2128; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; }
        .step-item { border-left: 5px solid #4CAF50; padding-left: 20px; margin-bottom: 30px; }
        
        /* 作者標籤與 Open Case 按鈕 (對齊標記 6, 7) */
        .author-tag { font-size: 11px; border-radius: 12px; padding: 3px 12px; display: inline-block; margin-left: 10px; font-weight: bold; }
        .view-btn { display: inline-block; padding: 6px 16px; background-color: #4CAF50; color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; }
        
        /* 輸入框顏色 */
        .stTextInput input { background-color: #161b22 !important; color: white !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
