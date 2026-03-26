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

        /* 🚀 【關鍵修正】消滅紅框空隙：當側欄收合時，讓主內容區域橫向撐開 */
        /* [data-collapsed="true"] 是側欄收起時的狀態 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }

        /* 🚀 讓內容置中，但在全螢幕下會自動填滿 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            padding-top: 3.5rem !important; 
            margin: 0 auto !important; /* 水平置中 */
            transition: all 0.3s ease-in-out !important;
        }

        /* 🚀 【按鈕外觀統一】解決奇怪白點問題 */
        button[kind="header"], [data-testid="stSidebarCollapseButton"] button {
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
            color: white !important;
        }
        
        /* 展開按鈕固定在左上角 */
        button[kind="header"] {
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 999999 !important;
        }

        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            width: 20px !important;
            height: 20px !important;
        }

        /* 🛡️ 隱藏雜物 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度：只有在展開時才固定 300px */
        [data-testid="stSidebar"]:not([data-collapsed="true"]) {
            min-width: 300px !important;
            max-width: 300px !important;
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
