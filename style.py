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

        /* 🚀 【消滅隱形牆】收起時內容完全靠左 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 2rem !important; 
        }

        /* 🚀 【右上角 >> 懸浮按鈕】強制捕獲 */
        /* 使用 fixed 定位，脫離原本的 header 限制 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            right: 25px !important; 
            top: 25px !important;   
            background-color: #ffffff22 !important; /* 透明白 */
            border: 2px solid #ffffff44 !important;
            border-radius: 50% !important;
            width: 50px !important;
            height: 50px !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 9999999 !important; /* 最高層級 */
            cursor: pointer !important;
            box-shadow: 0 0 15px rgba(255,255,255,0.2) !important;
            visibility: visible !important;
        }

        /* 讓 >> 圖示變白變大 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            color: white !important;
            width: 28px !important;
            height: 28px !important;
        }

        /* 🚀 展開時的收合按鈕 (<<) 也要變圓漂亮 */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: #ffffff22 !important;
            border-radius: 50% !important;
            width: 42px !important;
            height: 42px !important;
            border: 1px solid #ffffff44 !important;
        }

        /* 🚀 【綠色按鈕】鎖死無底線 */
        .view-btn, .view-btn:link, .view-btn:visited {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }

        /* 🛡️ 隱藏 Deploy, Share 等干擾項 */
        header, [data-testid="stHeader"] { 
            background: transparent !important;
            height: 0 !important;
            overflow: visible !important;
        }
        [data-testid="stToolbar"] { display: none !important; }
        #MainMenu, footer { display: none !important; }

        /* 🔥 黑盒子 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        
        /* 🚀 火箭位置：右下角 */
        .scroll-to-top {
            position: fixed; 
            bottom: 30px !important; 
            right: 25px !important;
            width: 45px !important; 
            height: 45px !important;
            background-color: #f77f00 !important; 
            color: white !important;
            border-radius: 50% !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center; 
            z-index: 99999 !important;
            text-decoration: none !important;
        }

        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
