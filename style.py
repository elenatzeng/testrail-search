import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 - 鎖死所有區塊 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🛡️ 徹底隱藏頂部白條與「所有」收合按鈕，讓它無法被關閉 */
        header, [data-testid="stHeader"], [data-testid="stSidebarCollapseButton"], button[kind="header"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 🚀 調整主內容間距，確保側邊欄固定時排版完美 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
            padding-right: 1rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 98% !important;
            padding-top: 2rem !important; 
        }

        /* 🚀 固定側邊欄寬度，防止它左右抖動 */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* 🚀 名字標籤樣式 (Elena 螢光綠) */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; 
            display: inline-flex !important; align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🔥 黑盒子去白底鎖死 */
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
        
        /* 📸 隱藏圖片與破圖 */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 🛠️ 輸入框與側邊欄文字顏色調整 */
        [data-testid="stSidebar"] .stMarkdown p { color: #adb5bd !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        
        /* 🚀 回到頂部火箭 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center;
            z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
            text-decoration: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
