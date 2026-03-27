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

        /* 🎯 隱藏右上角雜物 (貓咪、Deploy、選單) */
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
            box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
        }

        /* 🟢🔴 框框樣式基礎 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; 
            padding: 4px 14px !important; 
            display: inline-flex !important; 
            align-items: center !important; 
            margin-left: 12px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.6) !important; 
            line-height: 1 !important;
            box-sizing: border-box !important;
            white-space: nowrap !important;
        }

        /* 在職 (綠框) */
        .status-active { 
            color: #32CD32 !important; 
            border-color: #32CD32 !important; 
            box-shadow: 0 0 8px rgba(50, 205, 50, 0.3) !important;
        }

        /* 離職 (紅框) */
        .status-inactive { 
            color: #ff4b4b !important; 
            border-color: #ff4b4b !important; 
            box-shadow: 0 0 8px rgba(255, 75, 75, 0.3) !important;
        }

        /* 主標題 */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        header[data-testid="stHeader"] { background: transparent !important; }
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
