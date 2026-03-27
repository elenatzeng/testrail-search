import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px) !important;
            background-size: 550px 550px, 350px 350px !important;
        }

        /* 🎯 殺掉貓咪與選單 (最暴力版) */
        [data-testid="stHeader"] [data-testid="stBaseButton-header"],
        [data-testid="stHeader"] .stDeployButton,
        [data-testid="stHeader"] #MainMenu {
            display: none !important;
        }

        /* 🟢🔴 框框回歸 (Elena & 離職同事) */
        /* 增加強制寬度與邊界，確保它看起來像膠囊 */
        .author-tag { 
            display: inline-flex !important; 
            border: 2px solid !important;
            border-radius: 20px !important;
            padding: 2px 12px !important;
            margin-left: 10px !important;
            background: rgba(0,0,0,0.5) !important;
            font-weight: 600 !important;
            font-size: 13px !important;
            line-height: 1.5 !important;
            text-decoration: none !important;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #ff4b4b !important; border-color: #ff4b4b !important; }

        /* 🚀 Open Case 按鈕 (去底線、綠底) */
        /* 針對所有可能是按鈕的標籤進行強制去底線 */
        a[class*="view-btn"], .view-btn {
            background-color: #2ea44f !important;
            color: white !important;
            text-decoration: none !important; /* 絕對不要底線 */
            border-radius: 6px !important;
            padding: 6px 14px !important;
            display: inline-block !important;
            font-weight: 600 !important;
            box-shadow: none !important;
        }
        
        /* 預防已訪問過的連結變色或出底線 */
        a[class*="view-btn"]:visited, a[class*="view-btn"]:hover {
            color: white !important;
            text-decoration: none !important;
        }

        /* 🚀 火箭在右中 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            z-index: 99999 !important;
            background: #f77f00 !important;
            width: 45px !important;
            height: 45px !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-decoration: none !important;
        }

        footer { display: none !important; }
        header { background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)
