import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 名字膠囊發光標籤 (對齊箭頭 1) */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 25px !important; 
            padding: 2px 15px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 15px !important; /* 👈 拉開與標題距離 */
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.3) !important;
            vertical-align: middle;
        }
        
        /* 🚀 步驟方塊與換行設定 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; 
            padding: 20px; border-radius: 10px; border: 1px solid #30363d; 
            margin-top: 8px; font-size: 15px; line-height: 1.8;
            white-space: pre-wrap !important; /* 👈 保留換行 */
            word-wrap: break-word;
        }

        .step-container { border-left: 4.0px solid #2ea44f; padding-left: 20px; margin-bottom: 25px; }
        .step-label { font-weight: bold; font-size: 14px; margin-top: 15px; display: block; }

        .view-btn { 
            display: inline-block; padding: 7px 18px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; 
        }

        .scroll-to-top {
            position: fixed; bottom: 85px; right: 35px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            text-decoration: none !important; display: flex; align-items: center; justify-content: center;
            font-size: 22px;
        }
        </style>
    """, unsafe_allow_html=True)
