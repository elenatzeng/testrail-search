import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🚀 強制統一按鈕大小與樣式 (《 與 》) */
        [data-testid="stSidebarCollapseButton"] button, 
        button[kind="header"] {
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
        }

        /* 鼠標懸停效果 */
        [data-testid="stSidebarCollapseButton"] button:hover, 
        button[kind="header"]:hover {
            background-color: rgba(255, 255, 255, 0.2) !important;
            transform: scale(1.1);
        }

        /* 修正圖示顏色 */
        [data-testid="stSidebarCollapseButton"] svg, 
        button[kind="header"] svg {
            fill: white !important;
            color: white !important;
            width: 20px !important;
            height: 20px !important;
        }

        /* 🛡️ 隱藏頂部其餘雜物 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄與內容區間距 */
        [data-testid="stSidebar"] { min-width: 300px !important; max-width: 300px !important; }
        [data-testid="stAppViewContainer"] > .main { padding-left: 0.5rem !important; }
        [data-testid="stAppViewContainer"] .block-container { max-width: 98% !important; padding-top: 2rem !important; }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; vertical-align: middle; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; }
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
