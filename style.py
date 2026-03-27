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

        /* 🎯 隱藏右上角雜物 */
        button[data-testid="stBaseButton-header"], 
        button[kind="header"],
        [data-testid="stToolbarActionButtonIcon"],
        .stDeployButton,
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* 🛡️ 守護左側箭頭 > */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
            pointer-events: auto !important;
            z-index: 999999 !important;
        }

        /* 🚀 火箭固定在「右側中間」 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 45px !important;
            height: 45px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 50% !important;
            z-index: 10000000 !important;
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
        }

        /* 🟢🔴 【尺寸升級】作者膠囊框框樣式 */
        .author-tag { 
            font-size: 15px !important;       /* ✨ 字體稍微變大 (原本 13px) */
            border-radius: 25px !important;   /* ✨ 圓角隨之加大 */
            padding: 5px 18px !important;     /* ✨ 內距加寬加高，讓框框更飽滿 */
            display: inline-flex !important; 
            align-items: center !important; 
            margin-left: 12px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.6) !important; 
            line-height: 1.2 !important;
            white-space: nowrap !important;
            box-sizing: border-box !important;
        }

        /* 在職 (綠框) */
        .status-active { 
            color: #32CD32 !important; 
            border-color: #32CD32 !important; 
            box-shadow: 0 0 10px rgba(50, 205, 50, 0.2) !important;
        }

        /* 離職 (紅框) */
        .status-inactive { 
            color: #ff4b4b !important; 
            border-color: #ff4b4b !important; 
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.2) !important;
        }

        /* 🚀 Open Case 按鈕：保持綠底白字、無底線 */
        .view-btn, .view-btn:link, .view-btn:visited, .view-btn:hover, .view-btn:active {
            display: inline-block !important;
            padding: 7px 16px !important;     /* ✨ 按鈕也同步稍微大一點點 */
            background-color: #2ea44f !important; 
            color: white !important;           
            border-radius: 6px !important;    
            text-decoration: none !important;   
            font-size: 14px !important;
            font-weight: 600 !important;
            border: none !important;
            cursor: pointer !important;
        }
        
        .view-btn:hover {
            background-color: #2c974b !important;
            text-decoration: none !important;
        }

        /* 主標題樣式 */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        header[data-testid="stHeader"] { background: transparent !important; }
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
