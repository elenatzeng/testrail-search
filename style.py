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

        /* 🚀 (8) 名字標籤：邊框 2px 扎實感、名字強力加粗 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 3px 14px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 700 !important; /* 👈 名字強力加粗 */
            border: 2px solid !important; /* 👈 邊框 2px */
            background: rgba(0,0,0,0.6) !important;
            vertical-align: middle;
            color: white !important;
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

        /* 🚀 (10) Open Case 按鈕：亮綠色、無底線 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 7px 16px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 13px !important; 
            font-weight: 600 !important; 
            border: none !important;
        }
        .view-btn:hover { background-color: #3fb950 !important; text-decoration: none !important; }

        /* 🚀 【修正：大字體文字版火箭按鈕】 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 0px !important;
            transform: translateY(-50%) !important;
            width: auto !important;
            min-width: 130px !important; /* 增加寬度容納大字體 */
            height: 48px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 24px 0 0 24px !important; /* 左圓角膠囊 */
            z-index: 10000000 !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            padding: 0 20px !important;
            box-shadow: -4px 0 15px rgba(0,0,0,0.6) !important;
            transition: all 0.3s ease;
        }
        .scroll-to-top span {
            font-size: 16px !important; /* 👈 字體變大 16px */
            font-weight: 700 !important; /* 👈 字體加粗 */
            margin-left: 10px !important;
            white-space: nowrap !important;
            color: white !important;
        }
        .scroll-to-top:hover { 
            background-color: #ff9f43 !important; 
            transform: translateY(-50%) scale(1.05) !important; 
        }

        /* 🚀 【左側展開鈕】 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0px !important;
            transform: translateY(-50%) !important;
            width: 40px !important;
            height: 65px !important;
            background-color: #2ea44f !important; 
            border-radius: 0 35px 35px 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000001 !important;
            box-shadow: 4px 0 15px rgba(0,0,0,0.6) !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important; color: white !important; width: 28px !important; height: 28px !important;
        }

        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }

        /* 收合時內容吸附 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
