import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 背景設定 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px) !important;
            background-size: 550px 550px, 350px 350px !important;
        }

        /* 🎯 隱藏右上角 (貓咪、選單) */
        button[data-testid="stBaseButton-header"], 
        [data-testid="stToolbarActionButtonIcon"],
        .stDeployButton,
        #MainMenu {
            display: none !important;
        }

        /* 🛡️ 守護左側箭頭 > */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
        }

        /* 🚀 火箭固定在右側中間 */
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
            z-index: 9999999 !important;
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
        }

        /* 🟢🔴 作者膠囊框框 (加大版) */
        .author-tag { 
            font-size: 15px !important; 
            border-radius: 25px !important; 
            padding: 5px 18px !important; 
            display: inline-flex !important; 
            align-items: center !important; 
            margin-left: 12px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.6) !important; 
            line-height: 1.2 !important;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #ff4b4b !important; border-color: #ff4b4b !important; }

        /* 🚀 Open Case 按鈕 (去底線) */
        .view-btn, .view-btn:link, .view-btn:visited, .view-btn:hover {
            display: inline-block !important;
            padding: 7px 16px !important;
            background-color: #2ea44f !important; 
            color: white !important;           
            border-radius: 6px !important;    
            text-decoration: none !important;   
            font-size: 14px !important;
            font-weight: 600 !important;
        }

        /* 內容區與標題 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; padding: 15px 20px; 
            color: #c9d1d9 !important; 
            white-space: pre-wrap !important; /* 👈 這行配合斷行修復 */
        }
        h1 { font-size: 32px !important; color: white !important; }
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
