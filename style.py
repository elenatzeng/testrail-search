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

        /* 🚀 【消滅紅框空隙】核心邏輯 */
        /* 當側邊欄收合時，讓主內容區域橫向撐開到 100% */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            width: 100vw !important;
            max-width: 100vw !important;
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        
        /* 內容容器置中邏輯 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 90% !important;
            margin: 0 auto !important;
            padding-top: 3rem !important; 
            transition: all 0.3s ease-in-out;
        }

        /* 🚀 【修正左上角奇怪按鈕】統一按鈕外觀 */
        /* 展開按鈕 (>>) */
        button[kind="header"] {
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 1000000 !important;
            width: 38px !important;
            height: 38px !important;
            background-color: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }

        /* 收合按鈕 (<<) */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            width: 38px !important;
            height: 38px !important;
        }

        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
        }

        /* 🛡️ 隱藏雜物與白條 */
        header, [data-testid="stHeader"] { visibility: hidden !important; background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度固定 */
        [data-testid="stSidebar"] { min-width: 300px !important; max-width: 300px !important; }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🔥 黑盒子鎖死 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * {
            background: transparent !important;
            color: #c9d1d9 !important;
        }
        
        /* 火箭回到頂部 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; text-decoration: none !important;
        }

        img { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
