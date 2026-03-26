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

        /* 🚀 (8) 名字標籤：膠囊形狀、邊框加粗到 2px */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 500 !important; 
            border: 2px solid !important; /* 👈 【修改】從 1px 加粗到 2px */
            background: rgba(255,255,255,0.05) !important;
            vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：精緻感 */
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

        /* 🚀 (10) Open Case 按鈕：亮綠色、無底線 */
        .view-btn { 
            display: inline-block !important; 
            padding: 6px 14px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 13px !important; 
            font-weight: 600 !important; 
            transition: 0.3s;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            text-decoration: none !important;
            transform: translateY(-1px);
        }

        /* 🚀 調整側邊欄收合按鈕位置 */
        [data-testid="stSidebarCollapsedControl"] {
            top: 10px !important;
            left: 10px !important;
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 50% !important;
        }

        /* 🚀 隱藏 Streamlit 原生雜物 */
        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }
        
        /* 🚀 【修改】火箭按鈕：置左側中，做成半圓形標籤 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important; /* 垂直置中 */
            left: 0px !important;  /* 貼死左邊邊緣 */
            transform: translateY(-50%) !important; /* 完美對齊中心線 */
            width: 40px !important; /* 稍微縮小寬度 */
            height: 60px !important; /* 增加高度變成半橢圓 */
            background-color: #f77f00 !important; 
            color: white !important; 
            /* 圓角設定：右上、右下是圓的，左上、左下是直角，使其貼平邊緣 */
            border-radius: 0 30px 30px 0 !important; 
            z-index: 9999 !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center;
            text-decoration: none !important; 
            font-size: 22px !important; 
            box-shadow: 2px 0 10px rgba(0,0,0,0.4) !important;
            transition: 0.3s;
        }
        .scroll-to-top:hover {
            width: 45px !important; /* 懸停時稍微伸出來 */
            background-color: #ff9f43 !important;
        }
        </style>
    """, unsafe_allow_html=True)
