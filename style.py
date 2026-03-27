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

        /* 🚀 頂部工具欄玻璃效果 */
        [data-testid="stHeader"] {
            position: fixed !important;
            top: 0 !important;
            z-index: 1000001 !important;
            background: rgba(11, 14, 20, 0.8) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        }

        /* 🎯 隱藏 Deploy 按鈕 */
        .stDeployButton { display: none !important; }

        /* 🚀 作者標籤基礎樣式 */
        .author-tag { 
            font-size: 12px !important; border-radius: 20px !important; padding: 2px 12px !important; 
            display: inline-flex !important; align-items: center; margin-left: 10px !important; 
            font-weight: 600 !important; border: 2px solid !important; 
        }

        /* 🟢 在職 (Active)：綠字綠框 */
        .status-active { 
            color: #32CD32 !important; border-color: #32CD32 !important; 
            background: rgba(0,0,0,0.5) !important;
        }

        /* 🔴 離職 (Inactive)：物理鎖死紅區 (解決白框問題) */
        span.author-tag.status-inactive { 
            color: #FF4B4B !important; 
            border-color: #FF4B4B !important; 
            background: rgba(255, 75, 75, 0.2) !important; 
            box-shadow: 0 0 8px rgba(255, 75, 75, 0.4) !important;
        }

        /* 🚀 內容盒與火箭 */
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 15px 20px; color: #c9d1d9 !important; }
        .view-btn { display: inline-block; padding: 6px 14px; background-color: #2ea44f; color: white; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: 600; }
        .scroll-to-top { position: fixed; top: 50%; right: 15px; transform: translateY(-50%); width: 42px; height: 42px; background-color: #f77f00; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; text-decoration: none; z-index: 10000000; }
        
        footer, #MainMenu { visibility: hidden !important; }
        .block-container { padding-top: 4rem !important; }
        </style>
    """, unsafe_allow_html=True)
