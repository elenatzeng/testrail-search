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

        /* 🎯 【精準狙擊】隱藏貓咪 (GitHub Icon) */
        /* 直接針對妳提供的 data-testid 進行隱藏 */
        [data-testid="stToolbarActionButtonIcon"] {
            display: none !important;
        }
        
        /* 雙重保險：隱藏所有在 Toolbar 裡的按鈕連結 */
        [data-testid="stHeader"] a {
            display: none !important;
        }

        /* 🛡️ 重要：保留左側側邊欄控制鈕 (>) */
        /* 雖然我們隱藏了 a 標籤，但這個控制鈕通常是 button，所以要確保它可見 */
        [data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
        }

        /* 隱藏右側三條線選單 */
        #MainMenu {
            visibility: hidden !important;
        }

        /* 🚀 主标题缩放 (32px) */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: white !important;
            padding-top: 10px !important;
            padding-bottom: 5px !important;
        }

        /* 🚀 作者标签、黑盒子样式 */
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
        
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important; 
        }

        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
