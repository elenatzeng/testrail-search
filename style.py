import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 還原標籤高級感：增加 Padding, 圓角, 以及發光邊框 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; /* 圓潤感 */
            padding: 3px 12px !important; /* 撐開上下左右 */
            display: inline-flex !important;
            align-items: center; 
            margin-left: 12px !important; 
            font-weight: bold !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.4) !important;
            vertical-align: middle;
            /* 🚀 加上妳最喜歡的發光特效 */
            transition: all 0.3s ease;
        }
        
        /* 🚀 測試步驟盒子 (維持穩定) */
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; 
            padding: 16px 20px; border-radius: 10px; border: 1px solid #30363d; 
            margin-top: 8px; font-size: 15px; line-height: 1.8;
            white-space: pre-wrap !important;
        }

        .step-container { border-left: 4px solid #2ea44f; padding-left: 18px; margin-bottom: 25px; }

        /* 🚀 Open Case 按鈕 */
        .view-btn { 
            display: inline-block; padding: 7px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; 
            font-size: 14px; font-weight: bold; 
        }

        /* 🚀 火箭按鈕位置 */
        .scroll-to-top {
            position: fixed; bottom: 80px; right: 25px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; font-size: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        </style>
    """, unsafe_allow_html=True)
