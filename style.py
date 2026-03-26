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

        /* 🚀 【修正 1：右上角 >> 展開鈕】強制捕獲並置頂 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            right: 25px !important; /* 靠右 */
            top: 25px !important;   /* 靠上 */
            left: auto !important;
            display: flex !important;
            visibility: visible !important;
            width: 45px !important;
            height: 45px !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 50% !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000000 !important; /* 開到最高層級 */
            box-shadow: 0 0 15px rgba(255,255,255,0.3) !important;
            cursor: pointer !important;
        }
        
        /* 讓 >> 圖示變亮白色 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            color: white !important;
            width: 26px !important;
            height: 26px !important;
        }

        /* 🚀 【修正 2：火箭回到右側中間】 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important; /* 垂直置中 */
            right: 20px !important;
            transform: translateY(-50%) !important;
            width: 45px !important;
            height: 45px !important;
            background-color: #f77f00 !important;
            color: white !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            z-index: 999999 !important;
            text-decoration: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5) !important;
        }

        /* 🚀 【內容靠左吸附】當側欄收起時 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 2rem !important;
        }

        /* 🚀 【綠色按鈕無底線】強力鎖死 */
        .view-btn, .view-btn:link, .view-btn:visited {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important; /* 絕對無底線 */
            font-size: 14px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }
        .view-btn:hover { background-color: #3fb950 !important; text-decoration: none !important; }

        /* 🛡️ 隱藏雜物 */
        [data-testid="stHeader"], header { display: none !important; }
        hr, .stMarkdown hr { display: none !important; }
        #MainMenu, footer { display: none !important; }

        /* 🔥 黑盒子內容鎖死 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
