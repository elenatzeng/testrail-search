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

        /* 🚀 縮小側邊欄與內容的大空隙 ( image_d3134c 修正 ) */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
            padding-right: 1rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            max-width: 98% !important;
            padding-top: 2rem !important;
        }

        /* 🛠️ 【極簡收合鈕】修正收起來後找不到的問題 */
        [data-testid="stSidebarCollapseButton"] {
            background-color: transparent !important;
            color: #8b949e !important; /* 預設灰色 */
            border: none !important;
            box-shadow: none !important;
            transition: all 0.3s ease !important;
        }
        
        /* 當妳滑鼠靠近或是按鈕出現時，給它一點點螢光綠感 */
        [data-testid="stSidebarCollapseButton"]:hover {
            color: #32CD32 !important; /* 螢光綠，跟 Elena 標籤一樣 */
            background-color: rgba(50, 205, 50, 0.1) !important;
            transform: scale(1.2);
        }

        /* 🛡️ 封鎖系統白邊 */
        header, [data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden !important;
            height: 0 !important;
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

        /* 🚀 火箭回到頂部按鈕 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important;
            align-items: center; justify-content: center;
            z-index: 99999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
        }

        /* 🔥 黑盒子去白底 */
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
        
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 🛠️ 輸入框鎖死深色 */
        [data-testid="stSidebar"] label { color: #adb5bd !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
