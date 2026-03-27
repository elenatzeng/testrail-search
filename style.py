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

        /* 🚀 作者標籤基礎樣式 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important; 
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
        }

        /* 🟢 在職 (Active)：綠字綠框 */
        .status-active { 
            color: #32CD32 !important; 
            border-color: #32CD32 !important; 
        }

        /* 🔴 離職 (Inactive)：強制紅字紅框紅底 (鎖死 Meh) */
        /* 使用屬性選擇器來提高權重，解決妳截圖中邊框不變紅的問題 */
        span[class*="status-inactive"] { 
            color: #FF4B4B !important; 
            border-color: #FF4B4B !important; 
            background: rgba(255, 75, 75, 0.2) !important; 
            box-shadow: 0 0 10px rgba(255, 75, 75, 0.5) !important;
        }

        /* 🚀 頂部導航固定 */
        [data-testid="stHeader"] {
            position: fixed !important;
            top: 0 !important;
            z-index: 1000001 !important;
            background: rgba(11, 14, 20, 0.8) !important;
            backdrop-filter: blur(12px) !important;
        }

        /* 隱藏雜物 */
        .stDeployButton, [data-testid="stDeployButton"], footer, #MainMenu { display: none !important; }
        .block-container { padding-top: 4rem !important; }
        </style>
    """, unsafe_allow_html=True)
