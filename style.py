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

        /* 🛡️ 封鎖系統白條，但保留一點操作空間 */
        header, [data-testid="stHeader"], #MainMenu, footer {
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 🛠️ 【絕對顯影按鈕】讓妳收起來後一定找得到它 */
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            background-color: rgba(0, 0, 0, 0.8) !important; /* 深黑底，不透光 */
            color: #32CD32 !important;                       /* 螢光綠箭頭 */
            border: 2px solid #32CD32 !important;            /* 螢光綠粗邊框 */
            border-radius: 10px !important;
            position: fixed !important;
            top: 60px !important;    /* 往下挪 60px，避開死角 */
            left: 20px !important;   /* 離左邊 20px */
            z-index: 9999999 !important;
            width: 45px !important;
            height: 45px !important;
            box-shadow: 0 0 15px rgba(50, 205, 50, 0.6) !important; /* 螢光綠光暈 */
        }
        
        /* 💡 懸停效果：亮到妳受不了 */
        [data-testid="stSidebarCollapseButton"]:hover {
            background-color: #32CD32 !important;
            color: black !important;
            box-shadow: 0 0 25px rgba(50, 205, 50, 1) !important;
            transform: scale(1.1);
        }

        /* 🚀 究極縮小主內容間距 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 0.5rem !important;
            max-width: 98% !important;
            padding-top: 5rem !important; /* 避免標題撞到收合按鈕 */
        }

        /* 🚀 其他樣式鎖死 */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; font-weight: bold; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important; }
        
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
