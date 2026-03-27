import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 灵魂星空背景 (保持妳的原樣) */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🎯 【精準絕殺】針對妳提供的按鈕結構進行隱藏 */
        
        /* 1. 隱藏整顆 Header 按鈕 (包含貓咪和 ... 更多選項) */
        button[data-testid="stBaseButton-header"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* 2. 隱藏右側選單 (MainMenu) */
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
        }

        /* 3. 🛡️ 【守護側邊欄控制鈕】 */
        /* 確保左邊那個「>」不會被上面誤殺，強制它顯示出來 */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
            pointer-events: auto !important;
            z-index: 999999 !important;
        }
        
        /* 讓小箭頭變白色，在星空裡才好找 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
        }

        /* 🚀 主标题 (保持妳的原樣) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
