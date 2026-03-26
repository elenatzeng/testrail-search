import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 妳最愛的靈魂星空背景 - 鎖死 */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🛡️ 隱藏選單，防止手動切換 Light Mode */
        header, #MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }

        /* 🚀 火箭回到頂部按鈕 - 妳原本的樣式鎖死 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important;
            align-items: center; justify-content: center;
            font-size: 20px !important; text-decoration: none !important;
            z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
            border: none !important;
        }
        .scroll-to-top:hover { transform: translateY(-50%) scale(1.1) !important; }

        /* 🟢 靈魂綠線容器 */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px; margin-left: 5px; margin-bottom: 30px;
        }

        /* 🔥 核心去白：精準打擊 content-box 內部的所有 div 背景 */
        .content-box {
            background: #1c2128 !important; /* 妳指定的盒子深灰底 */
            border: 1px solid #30363d !important;
            border-radius: 12px; padding: 18px 20px;
        }

        /* 🚀 這一句是消滅白底的關鍵，且不影響妳原本的邏輯 */
        .content-box div, .inner-text div {
            background: transparent !important;
            background-color: transparent !important;
            color: #c9d1d9 !important;
        }

        /* 🚀 名字標籤、按鈕等樣式維持妳原本的樣子 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; 
            display: inline-flex !important; align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; font-weight: bold; }
        
        /* 📸 圖片蒸發 */
        img { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
