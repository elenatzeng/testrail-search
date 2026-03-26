import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 背景與基本設定 */
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 500 !important; 
            border: 1px solid !important; 
            background: rgba(255,255,255,0.05) !important;
            vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：內文 14px、取消粗體 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important; /* 👈 內文 14px */
            font-weight: 400 !important; /* 👈 徹底取消粗體 */
            line-height: 1.7;
            margin-bottom: 10px;
        }

        /* 🚀 列表縮進排版 (123. 與 •) */
        .list-item {
            display: block;
            padding-left: 22px; /* 👈 讓數字或點點有空間 */
            text-indent: -22px; /* 👈 讓第二行縮回來對齊 */
            margin-bottom: 4px;
        }

        /* 🚀 (10) Open Case 按鈕 */
        .view-btn { 
            display: inline-block !important; 
            padding: 7px 16px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 14px !important; 
            font-weight: 600 !important; 
        }

        /* 🚀 火箭按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 30px; right: 25px; width: 45px; height: 45px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; font-size: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }

        /* 側邊欄控制鈕 */
        [data-testid="stSidebarCollapsedControl"] {
            top: 15px !important; left: 15px !important;
            background-color: rgba(255,255,255,0.1) !important; border-radius: 50% !important;
        }
        </style>
    """, unsafe_allow_html=True)
