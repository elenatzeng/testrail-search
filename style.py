import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 - 鎖死深色底層 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🛡️ 封鎖系統白邊 */
        header, [data-testid="stHeader"], #MainMenu, footer {
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 🛠️ 【絕對導航星】收合按鈕強化 - 讓妳在收起來後一眼看到它 */
        [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            background-color: rgba(0, 0, 0, 0.7) !important; /* 深黑色背景，襯托螢光綠 */
            color: #32CD32 !important;                       /* 螢光綠箭頭 */
            border: 2px solid #32CD32 !important;            /* 螢光綠邊框 */
            border-radius: 8px !important;
            top: 25px !important;    /* 往下挪 25px */
            left: 25px !important;   /* 往左挪 25px */
            z-index: 1000002 !important;
            width: 35px !important;
            height: 35px !important;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease-in-out !important;
            box-shadow: 0 0 10px rgba(50, 205, 50, 0.5) !important; /* 帶一點螢光綠光暈 */
        }
        
        /* 滑鼠移過去變更亮 */
        [data-testid="stSidebarCollapseButton"]:hover {
            background-color: #32CD32 !important;
            color: black !important;
            box-shadow: 0 0 20px rgba(50, 205, 50, 0.8) !important;
            transform: scale(1.15);
        }

        /* 🚀 究極縮小主內容間距 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
            padding-right: 1rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 98% !important;
        }

        /* 🚀 名字標籤、火箭、黑盒子樣式 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; 
            display: inline-flex !important; align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * {
            background: transparent !important;
            background-color: transparent !important;
            color: #c9d1d9 !important;
        }
        
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center;
            z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
        }
        
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
