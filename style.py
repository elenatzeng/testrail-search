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

        /* 🚀 (8) 名字標籤：邊框 2px 扎實感 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
            vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：內文 14px 不粗體 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important;
            font-weight: 400 !important; 
            line-height: 1.6;
            margin-bottom: 10px;
        }

        /* 🚀 (10) Open Case 按鈕：亮綠色、絕對無底線 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 6px 14px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 13px !important; 
            font-weight: 600 !important; 
            border: none !important;
        }
        .view-btn:hover { background-color: #3fb950 !important; text-decoration: none !important; }

        /* 🚀 【修正：火箭靠右置中】橘色半圓標籤 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;   /* 垂直置中 */
            right: 0px !important;  /* 👈 貼死右邊邊緣 */
            transform: translateY(-50%) !important;
            width: 45px !important;
            height: 70px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 35px 0 0 35px !important; /* 左半圓形 */
            z-index: 10000000 !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            font-size: 24px !important; 
            box-shadow: -4px 0 15px rgba(0,0,0,0.6) !important;
            transition: all 0.3s ease;
        }
        .scroll-to-top:hover { width: 55px !important; background-color: #ff9f43 !important; }

        /* 🚀 【左側展開鈕 >> 】綠色半圓標籤 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;   /* 垂直置中 */
            left: 0px !important;   /* 貼死左邊邊緣 */
            transform: translateY(-50%) !important;
            width: 45px !important;
            height: 70px !important;
            background-color: #2ea44f !important; 
            border-radius: 0 35px 35px 0 !important; /* 右半圓形 */
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000001 !important;
            box-shadow: 4px 0 15px rgba(0,0,0,0.6) !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important; color: white !important; width: 28px !important; height: 28px !important;
        }

        /* 🛡️ 隱藏雜物 */
        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
