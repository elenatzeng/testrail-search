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

        /* 🚀 縮小左側邊欄與主內容的間距，讓排版更緊湊 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 96% !important;
            padding-top: 2rem !important; 
        }

        /* 🛡️ 隱藏原生 Header (避免白條出現)，但保留側欄按鈕功能 */
        header, [data-testid="stHeader"] {
            visibility: hidden !important;
            height: 0 !important;
        }

        /* 🚀 側邊欄寬度鎖死 300px */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* 🚀 名字標籤樣式 (螢光綠) */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }

        /* 🔥 黑盒子內容去白底補強 */
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

        /* 🚀 火箭回到頂部按鈕 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important;
            align-items: center; justify-content: center;
            font-size: 20px !important; text-decoration: none !important;
            z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
        }
        
        /* 📸 隱藏所有圖片 */
        img, [data-testid="stImage"] { display: none !important; }
        
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
