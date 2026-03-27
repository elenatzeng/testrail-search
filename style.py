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

        /* 🎯 【核心修正：不給點、不給看】 */
        
        /* 針對妳提供的貓咪圖標容器：禁止點擊並隱藏 */
        [data-testid="stToolbarActionButtonIcon"], 
        .st-emotion-cache-q16mip {
            display: none !important;      /* 先嘗試隱藏 */
            pointer-events: none !important; /* 萬一冒出來也點不到 */
            cursor: default !important;
        }

        /* 針對整個右側工具欄按鈕 (GitHub 連結) */
        [data-testid="stHeader"] a {
            pointer-events: none !important; /* 徹底禁止點擊跳轉 */
            visibility: hidden !important;   /* 隱藏但保留空間（防止 UI 移位） */
        }

        /* 隱藏右側三條線選單，且不給點 */
        #MainMenu {
            pointer-events: none !important;
            visibility: hidden !important;
        }

        /* 🛡️ 確保左側側邊欄控制鈕（>）「可以點」 */
        /* 因為上面禁用了 Header 裡的 a，我們要確保 button 類型的展開鈕是正常的 */
        [data-testid="stSidebarCollapsedControl"] {
            pointer-events: auto !important;
            visibility: visible !important;
            display: flex !important;
            z-index: 10000001 !important;
        }

        /* 🚀 主标题 (保持妳的原樣) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
