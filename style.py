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

        /* 🚀 (8) 名字標籤：2px 邊框扎實感 */
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
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：14px 不粗體 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important;
            font-weight: 400 !important; 
            line-height: 1.6;
        }

        /* 🚀 (10) Open Case 按鈕：亮綠色、無底線 */
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

        /* 🚀 【精緻火箭：靠右垂直置中】 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important; /* 👈 稍微離開邊緣更有呼吸感 */
            transform: translateY(-50%) !important;
            width: 42px !important;  /* 👈 縮小圓圈 */
            height: 42px !important; /* 👈 縮小圓圈 */
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 50% !important; /* 正圓形 */
            z-index: 9999999 !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            font-size: 18px !important; /* 👈 讓火箭縮小在中間 */
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
            transition: all 0.3s ease;
        }
        .scroll-to-top:hover { 
            background-color: #ff9f43 !important; 
            transform: translateY(-50%) scale(1.1) !important; 
        }

        /* 🚀 【左側展開鈕：綠色半圓】 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0px !important;
            transform: translateY(-50%) !important;
            width: 40px !important;
            height: 60px !important;
            background-color: #2ea44f !important; 
            border-radius: 0 30px 30px 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000001 !important;
        }

        /* 🛡️ 隱藏系統雜物 */
        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }
        
        /* 讓內容收合時完全吸附 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
