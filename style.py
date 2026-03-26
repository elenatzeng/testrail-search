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
        
        /* 🛡️ 封鎖系統白邊：隱藏選單與工具列，強制背景漆黑 */
        header, [data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden !important;
            height: 0 !important;
            background-color: #0b0e14 !important;
        }
        
        /* 🚀 名字標籤樣式 */
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

        /* 🚀 無文字內容提示 */
        .no-content-hint { 
            color: #8b949e !important; 
            font-size: 14px !important; 
            padding: 10px 0 10px 25px !important; 
            font-style: italic !important;
            display: block !important;
        }

        /* 🚀 火箭回到頂部按鈕 - 固定在右邊中間 */
        .scroll-to-top {
            position: fixed;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important;
            height: 42px !important;
            background-color: #f77f00 !important;
            color: white !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            font-size: 20px !important;
            text-decoration: none !important;
            z-index: 99999 !important;
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
            border: none !important;
        }

        /* ✨ 火箭提示氣泡 */
        .scroll-to-top::after {
            content: "回到最頂";
            position: absolute;
            right: 55px;
            top: 50%;
            transform: translateY(-50%);
            background-color: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 5px 10px;
            border-radius: 6px;
            font-size: 12px;
            white-space: nowrap;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            border: 1px solid #f77f00;
        }
        .scroll-to-top:hover::after { opacity: 1; }
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8) !important;
        }

        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        
        /* 🔥 去白鎖死補強：確保盒子內文字背景絕對透明 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        /* 精準鎖死所有子標籤背景，不准變白 */
        .content-box *, .inner-text, .inner-text * {
            background: transparent !important;
            background-color: transparent !important;
            color: #c9d1d9 !important;
        }
        
        /* 📸 圖片與破圖徹底消失 */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 🛠️ 側邊欄與輸入框鎖死深色 */
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #adb5bd !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
