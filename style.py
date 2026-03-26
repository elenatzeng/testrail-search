import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 - 妳的最愛原封不動 */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🛡️ 鎖死永夜：隱藏右上角選單與抹除系統白邊 */
        header, [data-testid="stHeader"], #MainMenu, footer { display: none !important; }

        /* 🚀 名字標籤樣式 - 保留妳的設計 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 🚀 火箭回到頂部按鈕 - 保留妳的所有參數與特效 */
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
        .scroll-to-top::after {
            content: "回到最頂"; position: absolute; right: 55px; top: 50%;
            transform: translateY(-50%); background-color: rgba(0, 0, 0, 0.8);
            color: white; padding: 5px 10px; border-radius: 6px;
            font-size: 12px; white-space: nowrap; opacity: 0;
            transition: opacity 0.3s ease; pointer-events: none;
            border: 1px solid #f77f00;
        }
        .scroll-to-top:hover::after { opacity: 1; }
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8) !important;
        }

        /* 🟢 靈魂綠線容器 */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px; margin-left: 5px; margin-bottom: 30px;
        }

        /* 🔥 關鍵：絕對去白修正 - 讓盒子內部文字背景透明 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
            color: #c9d1d9 !important;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
        }

        /* 強制 content-box 下面所有標籤（div, p, span）背景都消失 */
        .content-box * {
            background-color: transparent !important;
            background: transparent !important;
        }

        /* 🚀 其他按鈕與提示 */
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 0 10px 25px !important; font-style: italic !important; display: block !important; }
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        
        /* 📸 圖片與破圖標籤 - 徹底消失術 */
        img, [data-testid="stImage"] { display: none !important; }

        /* 側邊欄與輸入框文字顏色 */
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p { color: #adb5bd !important; }
        input { background-color: #161b22 !important; color: white !important; }
        </style>
    """, unsafe_allow_html=True)
