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

        /* 🎯 【驅貓專用】精準打擊 GitHub 圖標 */
        /* 透過網址屬性強制隱藏，這招通常最管用 */
        a[href*="github.com"] {
            display: none !important;
        }
        
        /* 隱藏可能包裹貓咪的容器 */
        .stHeader div:has(> a[href*="github.com"]) {
            display: none !important;
        }

        /* 隱藏 Deploy 按鈕 */
        .stDeployButton {
            display: none !important;
        }

        /* 隱藏右側三條線選單 */
        #MainMenu {
            visibility: hidden !important;
        }

        /* 讓 Header 變透明，但不刪除它 (保留左側展開鈕) */
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

        /* 🚀 作者标签样式 */
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
        }

        /* 🛡️ 確保左側側邊欄控制鈕（>）依然存在 */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
        }

        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
