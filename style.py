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

        /* 🚀 【消滅紅框空隙】核心修正：收起時內容全螢幕吸附 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] [data-testid="stSidebar"] {
            margin-left: -300px !important;
            border: none !important;
            box-shadow: none !important;
        }
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
            width: 100vw !important;
        }

        /* 🚀 主內容區置中與動畫 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 3.5rem !important; 
            transition: all 0.3s ease-in-out !important;
        }

        /* 🚀 【綠色 Open Case 按鈕】鎖死樣式（無底線） */
        .view-btn {
            display: inline-block !important;
            padding: 8px 18px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            text-decoration: none !important;
            transform: scale(1.05);
        }

        /* 🚀 【救援按鈕】樣式統一：固定在左上角 */
        button[kind="header"] {
            position: fixed !important;
            left: 12px !important;
            top: 12px !important;
            z-index: 1000000 !important;
            width: 42px !important;
            height: 42px !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
        }
        [data-testid="stSidebarCollapseButton"] button {
            width: 42px !important;
            height: 42px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
        }

        /* 修正圖示顏色 */
        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
            width: 22px !important;
            height: 22px !important;
        }

        /* 🛡️ 隱藏系統白線與雜物 */
        hr, .stMarkdown hr { display: none !important; }
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度 */
        [data-testid="stSidebar"]:not([data-collapsed="true"]) {
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* 🚀 名字標籤與黑盒子 */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; z-index: 99999 !important; }
        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
