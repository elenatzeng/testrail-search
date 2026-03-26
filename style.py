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

        /* 🚀 【修正：收起時靠左】 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 2rem !important; 
        }

        /* 🚀 【核心修正：讓 >> 復活並出現在左側置中】 */
        /* 不要 display:none 掉 header，否則按鈕會死掉 */
        header, [data-testid="stHeader"] {
            background-color: transparent !important;
            height: 0 !important; /* 讓它不佔位，但裡面的按鈕還活著 */
        }

        /* 強制捕獲收合後的控制區塊 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;   /* 垂直置中 */
            left: 15px !important;  /* 貼近左邊 */
            transform: translateY(-50%) !important;
            display: flex !important;
            visibility: visible !important;
            width: 55px !important;
            height: 55px !important;
            background-color: rgba(255, 255, 255, 0.3) !important; /* 更亮的白圓圈 */
            border: 2px solid rgba(255, 255, 255, 0.6) !important;
            border-radius: 50% !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 9999999 !important; /* 開到最高層級 */
            box-shadow: 0 0 20px rgba(0,0,0,0.7) !important;
            cursor: pointer !important;
        }
        
        /* 讓按鈕內的 >> 圖示變得超級明顯 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            color: white !important;
            width: 35px !important;
            height: 35px !important;
        }

        /* 🚀 展開時的收合鈕 (<<) 樣式同步 */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            width: 45px !important;
            height: 45px !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
        }

        /* 🚀 【綠色按鈕】鎖死樣式 */
        .view-btn, .view-btn:link, .view-btn:visited {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: bold !important;
        }

        /* 🛡️ 隱藏 Deploy, Share 等干擾項 (改用 visibility 避免影響 >>) */
        [data-testid="stToolbar"] { visibility: hidden !important; }
        #MainMenu, footer { display: none !important; }

        /* 🔥 黑盒子 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        
        /* 🚀 火箭位置：右側中間 (與 >> 對稱) */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important; 
            right: 20px !important;
            transform: translateY(-50%) !important;
            width: 55px !important; 
            height: 55px !important;
            background-color: #f77f00 !important; 
            color: white !important;
            border-radius: 50% !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center; 
            z-index: 999999 !important;
            text-decoration: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }

        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
