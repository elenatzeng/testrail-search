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

        /* 🚀 【關鍵修正】消滅左側空隙：讓內容隨側欄狀態自動滑動 */
        /* 當側欄收合時 (data-collapsed="true")，強制寬度填滿並取消邊距 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }

        /* 主內容區平滑過渡 */
        [data-testid="stAppViewContainer"] .main {
            transition: all 0.3s ease-in-out !important;
        }

        /* 🚀 調整內部容器：在全螢幕下也能漂亮置中 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 95% !important;
            padding-top: 3.5rem !important; /* 留一點空間給左上角按鈕 */
            margin: 0 auto !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 🚀 強制統一按鈕樣式 (《 與 》) */
        /* 展開按鈕 (>>)：固定在左上角，確保不會消失 */
        button[kind="header"] {
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 999999 !important;
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            visibility: visible !important;
        }

        /* 收合按鈕 (<<) */
        [data-testid="stSidebarCollapseButton"] button {
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }

        /* 修正圖示 */
        [data-testid="stSidebarCollapseButton"] svg, button[kind="header"] svg {
            fill: white !important;
            color: white !important;
            width: 20px !important;
            height: 20px !important;
        }

        /* 🛡️ 隱藏其餘雜物 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度設定 (拿掉原本可能的鎖死限制) */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
        }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; vertical-align: middle; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important; }
        
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
