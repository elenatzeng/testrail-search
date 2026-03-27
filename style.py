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

        /* 🎯 【精準屏蔽】只針對右側工具欄 */
        
        # 1. 把貓咪和選單變不見 (但不要動到整個 Header)
        [data-testid="stToolbar"], 
        .stGithubIcon, 
        #MainMenu, 
        .stDeployButton {
            display: none !important;
            visibility: hidden !important;
        }

        /* 2. 🛡️ 【防禦罩】在右上方放一個透明層，讓滑鼠點不到下面的東西 */
        /* 寬度設為 150px 剛好蓋住貓咪和選單，但不會碰到左邊的小箭頭 */
        [data-testid="stHeader"]::after {
            content: "";
            position: absolute;
            right: 0;
            top: 0;
            width: 150px; 
            height: 60px;
            z-index: 999999;
            background: rgba(0,0,0,0); /* 透明的 */
            pointer-events: auto;      /* 它可以攔截滑鼠 */
            cursor: default;           /* 讓滑鼠變成普通的箭頭，不是手指 */
        }

        /* 3. ✅ 【保證存活】強制側邊欄控制鈕 (>) 置頂且可點擊 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            left: 5px !important;
            top: 10px !important;
            z-index: 1000001 !important;
            visibility: visible !important;
            display: flex !important;
            pointer-events: auto !important;
        }

        /* 🚀 主標題 (32px) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
