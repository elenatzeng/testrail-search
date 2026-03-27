import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 (維持原樣) */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🎯 【精準殺貓】針對妳提供的那顆 Button ID */
        button[data-testid="stBaseButton-header"], 
        button[kind="header"],
        [data-testid="stToolbarActionButtonIcon"],
        .stDeployButton,
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* 🛡️ 【守護左側箭頭 > 】 */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
            pointer-events: auto !important;
            z-index: 999999 !important;
        }

        /* 🚀 【火箭座標修正】維持在「左側中間」 */
        .scroll-to-top {
            position: fixed !important;
            
            /* 🎯 關鍵修正：將火箭移到「左側中間」 */
            top: 50% !important;        /* 螢幕高度的 50% */
            left: 5px !important;       /* 距離左邊 5 像素 */
            transform: translateY(-50%) !important; /* 向上平移 50%，達到真正的垂直置中 */
            
            width: 45px !important;
            height: 45px !important;
            background-color: #f77f00 !important; /* 橘色，方便辨識 */
            color: white !important; 
            border-radius: 50% !important;
            z-index: 10000000 !important; /* 超高層級，保證浮在最上面 */
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
            transition: transform 0.2s, box-shadow 0.2s !important;
        }
        
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 6px 20px rgba(0,0,0,0.8) !important;
        }

        /* 移除頂部白線與多餘間距 */
        header[data-testid="stHeader"] { background: transparent !important; }
        .block-container { padding-top: 1.5rem !important; }
        footer { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
