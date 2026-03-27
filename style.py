import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 灵魂星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🎯 【核心修正：精準隱藏貓咪與選單】 */
        
        /* 1. 隱藏 GitHub 貓咪圖標 (最精準的選擇器) */
        .stHeader .stGithubIcon, 
        [data-testid="stHeader"] a[href*="github.com"] {
            display: none !important;
        }

        /* 2. 隱藏 Deploy 按鈕 (那個藍色的按鈕) */
        .stDeployButton {
            display: none !important;
        }

        /* 3. 隱藏右側三條線選單 (MainMenu) */
        #MainMenu {
            visibility: hidden !important;
        }

        /* 4. 讓 Header 變透明，防止有一條白/黑線擋住背景 */
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0) !important;
        }

        /* 🚀 主标题缩放 (32px) */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: white !important;
            padding-top: 10px !important;
            padding-bottom: 5px !important;
        }

        /* 🚀 作者标签、黑盒子、按钮样式 */
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
            color: white !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #ff4b4b !important; border-color: #ff4b4b !important; }
        
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

        /* 🚀 精制圆火箭 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important;
            height: 42px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 50% !important;
            z-index: 10000000 !important;
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }

        /* 🛡️ 確保側邊欄控制鈕（小箭頭）維持可見 */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            z-index: 10000001 !important;
        }

        footer { display: none !important; }
        .block-container { padding-top: 1rem !important; }
        </style>
    """, unsafe_allow_html=True)
