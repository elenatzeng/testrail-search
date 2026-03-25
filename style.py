import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：膠囊形狀、發光感 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; 
            padding: 4px 14px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 15px !important; 
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
            vertical-align: middle;
            transition: all 0.3s ease;
        }
        
        /* 🚀 (9) 測試步驟盒子 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; 
            padding: 16px 20px; border-radius: 10px; border: 1px solid #30363d; 
            margin-top: 8px; font-size: 15px; line-height: 1.8;
            white-space: pre-wrap !important;
        }
        .step-container { border-left: 4px solid #2ea44f; padding-left: 18px; margin-bottom: 25px; }

        /* 🚀 (10) Open Case 按鈕 */
        .view-btn { 
            display: inline-block; padding: 7px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; 
            font-size: 14px; font-weight: bold; 
        }

        /* 🚀 火箭按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; font-size: 26px; box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        }
        </style>
    """, unsafe_allow_html=True)
