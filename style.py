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

        /* 🚀 【關鍵修正】讓內容在側欄收起時自動靠左並置中 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 90% !important; /* 稍微縮小寬度，置中感會更明顯 */
            padding-top: 2rem !important; 
            margin: 0 auto !important; /* 這行負責置中 */
        }

        /* 🚀 【按鈕樣式對稱】統一 《 與 》 的外觀 */
        button[kind="header"], [data-testid="stSidebarCollapseButton"] button {
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }

        button[kind="header"] { left: 10px !important; top: 10px !important; }

        /* 圖示顏色與大小 */
        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
            width: 20px !important;
            height: 20px !important;
        }

        /* 🛡️ 隱藏其餘雜物 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄固定寬度 */
        [data-testid="stSidebar"] { min-width: 300px !important; max-width: 300px !important; }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; vertical-align: middle; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🔥 黑盒子內容去白底 */
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; }
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
