import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 🚀 名字弧形外框：在職綠/離職紅由 OnlineApp 帶入顏色 */
        .author-tag { 
            font-size: 11px; 
            border-radius: 25px; 
            padding: 2px 14px; 
            display: inline-block; 
            margin-left: 10px; 
            font-weight: bold; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.3) !important;
            vertical-align: middle;
        }
        
        /* 測試步驟深色方塊與換行 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; padding: 15px; 
            border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; 
            white-space: pre-wrap; line-height: 1.6;
        }

        /* 🚀 活力橘回到頂端按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 30px; width: 48px; height: 48px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            text-decoration: none !important; display: flex; align-items: center; justify-content: center;
            font-size: 20px; transition: 0.3s;
        }
        .scroll-to-top:hover { transform: translateY(-5px); background-color: #e67600; }

        .view-btn { 
            display: inline-block; padding: 6px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; 
        }

        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
