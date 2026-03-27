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

        /* 🎯 【禁區設定】徹底禁止右側所有點擊 */
        
        /* 1. 抓取整個頂部工具欄容器，直接禁止所有滑鼠事件 */
        [data-testid="stHeader"] {
            pointer-events: none !important;
            background: rgba(0,0,0,0) !important; /* 保持透明 */
        }

        /* 2. 針對貓咪、選單、Deploy 按鈕全部隱形化 */
        [data-testid="stToolbar"], 
        #MainMenu, 
        .stDeployButton, 
        .stGithubIcon,
        a[href*="github.com"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 3. 🛡️ 【唯一活口】強行開啟左側展開鈕的點擊權限 */
        /* 因為 Header 禁用了點擊，我們要單獨幫側邊欄按鈕開路 */
        [data-testid="stSidebarCollapsedControl"] {
            pointer-events: auto !important; /* 恢復點擊 */
            cursor: pointer !important;
            visibility: visible !important;
            display: flex !important;
            z-index: 99999999 !important; /* 確保它在最上層 */
        }

        /* 🚀 主标题 (保持妳的原樣) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }
        
        footer { display: none !important; }
        .block-container { padding-top: 1.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
