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

        /* 🛡️ 徹底隱藏原生那個找不到的按鈕與 Header */
        header, [data-testid="stHeader"], [data-testid="stSidebarCollapseButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 🚀 究極縮小主內容間距 */
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 0.5rem !important;
        }
        [data-testid="stAppViewContainer"] .block-container {
            padding-left: 0.5rem !important;
            max-width: 98% !important;
            padding-top: 4rem !important; 
        }

        /* 🚀 名字標籤樣式 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; 
            display: inline-flex !important; align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🔥 黑盒子去白底 */
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
        
        /* 📸 隱藏圖片 */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 🛠️ 輸入框鎖死深色 */
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; }
        </style>
    """, unsafe_allow_html=True)
