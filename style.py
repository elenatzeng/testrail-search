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

        /* 🚀 (8) 名字標籤：邊框加粗到 2px 扎實感 */
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

        /* 🚀 (9) 核心黑盒子 */
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

        /* 🚀 (10) Open Case 按鈕：強力消滅底線 */
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

        /* 🚀 【核心修正：火箭絕對置中】貼在左邊緣 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;   /* 👈 垂直絕對置中 */
            left: 0px !important;   /* 👈 貼死左側邊緣 */
            transform: translateY(-50%) !important; /* 👈 補償自身高度達到完美置中 */
            width: 45px !important;
            height: 65px !important;
            background-color: #f77f00 !important;
            color: white !important;
            border-radius: 0 35px 35px 0 !important; /* 右半圓拉環狀 */
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 9999999 !important; 
            text-decoration: none !important;
            font-size: 24px !important;
            box-shadow: 4px 0 15px rgba(0,0,0,0.6) !important;
            transition: all 0.3s ease;
        }
        .scroll-to-top:hover {
            width: 55px !important;
            background-color: #ff9f43 !important;
        }

        /* 🚀 側邊欄展開鈕：稍微移開避開火箭，同樣貼左 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 40% !important; /* 👈 放在中間偏上 */
            left: 0px !important;
            width: 45px !important;
            height: 55px !important;
            background-color: rgba(255,255,255,0.15) !important;
            border-radius: 0 25px 25px 0 !important;
            z-index: 10000000 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
