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

        /* 🛡️ 封鎖系統白條，騰出按鈕空間 */
        header, [data-testid="stHeader"], #MainMenu, footer {
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 🛠️ 【絕對顯影：收合按鈕】強制出現在畫面上 */
        [data-testid="stSidebarCollapseButton"] {
            position: fixed !important;
            top: 20px !important;     /* 距離頂部 20px */
            left: 20px !important;    /* 距離左側 20px */
            display: flex !important; /* 強制顯示 */
            z-index: 10000000 !important;
            background-color: #f77f00 !important; /* 橘色，讓妳一眼看到 */
            color: white !important;
            border-radius: 8px !important;
            width: 40px !important;
            height: 40px !important;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 15px rgba(247, 127, 0, 0.7) !important;
            border: 2px solid white !important;
        }
        
        [data-testid="stSidebarCollapseButton"]:hover {
            transform: scale(1.1) !important;
            background-color: #ff9f1c !important;
        }

        /* 🚀 究極縮小主內容間距 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 0.5rem !important;
            max-width: 98% !important;
            padding-top: 5rem !important; /* 給左上角按鈕留點空間 */
        }

        /* 🚀 標籤與按鈕樣式鎖死 */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; font-weight: bold; }
        
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        /* 🚀 回到頂部火箭 */
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; }
        
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
