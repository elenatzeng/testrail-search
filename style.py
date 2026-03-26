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

        /* 🚀 【核心修正：讓 >> 復活】不要隱藏整個 Header，改用透明度 */
        header[data-testid="stHeader"] {
            background: transparent !important;
            color: transparent !important;
        }
        /* 隱藏 Header 裡除了按鈕以外的雜物 (Deploy, Share, 1號按鈕) */
        header[data-testid="stHeader"] [data-testid="stToolbar"] {
            display: none !important;
        }

        /* 🚀 【救援 >> 按鈕】強制固定在左側中間，做成半圓形標籤 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0 !important;
            transform: translateY(-50%) !important;
            display: flex !important;
            visibility: visible !important;
            width: 40px !important;
            height: 80px !important;
            background-color: #2ea44f !important; /* 妳喜歡的綠色，更顯眼 */
            border-radius: 0 40px 40px 0 !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000000 !important;
            box-shadow: 4px 0 15px rgba(0,0,0,0.5) !important;
            cursor: pointer !important;
        }

        /* 讓 >> 圖示變白 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            color: white !important;
            width: 25px !important;
            height: 25px !important;
        }

        /* 🚀 展開後的收合鈕 (<<) 也要漂亮 */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 50% !important;
            border: 1px solid white !important;
        }

        /* 🚀 【修正：收起時靠左】內容完全吸附 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
            width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 90% !important;
            margin: 0 auto !important;
            padding-top: 3rem !important;
        }

        /* 🚀 【標題 20px & 綠色按鈕無底線】鎖死 */
        .view-btn, .view-btn:link, .view-btn:visited {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: bold !important;
        }
        .view-btn:hover { background-color: #3fb950 !important; text-decoration: none !important; }

        /* 🔥 黑盒子 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        
        /* 🚀 火箭位置：右側中間 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important; 
            right: 20px !important;
            transform: translateY(-50%) !important;
            width: 45px !important; 
            height: 45px !important;
            background-color: #f77f00 !important; 
            color: white !important;
            border-radius: 50% !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center; 
            z-index: 999999 !important;
            text-decoration: none !important;
        }

        #MainMenu, footer { display: none !important; }
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
