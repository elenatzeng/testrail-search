import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 膠囊弧形標籤：加粗、發光、對齊修正 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 25px !important; 
            padding: 2px 15px !important; 
            display: inline-flex !important;
            align-items: center;
            margin-left: 10px; 
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.3) !important;
            vertical-align: middle;
            line-height: 1;
        }
        
        /* 🚀 測試步驟方塊：比例調整與強制換行 */
        .step-content-box { 
            color: #c9d1d9 !important; 
            background: #1c2128; 
            padding: 18px 22px; /* 增加內距讓比例更厚實 */
            border-radius: 10px; 
            border: 1px solid #30363d; 
            margin-top: 8px; 
            font-size: 15px;
            line-height: 1.7;
            white-space: pre-line !important; /* 👈 關鍵：強制保留換行 */
            word-wrap: break-word;
            max-width: 95%; /* 避免方塊太寬看起來太扁 */
        }

        .step-label {
            font-weight: bold; 
            font-size: 14px; 
            color: #8b949e; 
            margin-top: 15px;
            display: block;
        }

        /* 側邊綠條 */
        .step-container {
            border-left: 4px solid #2ea44f; 
            padding-left: 20px; 
            margin-bottom: 30px;
        }

        /* 活力橘按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 35px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            text-decoration: none !important; display: flex; align-items: center; justify-content: center;
            font-size: 22px;
        }
        
        .view-btn { 
            display: inline-block; padding: 7px 18px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; 
        }
        </style>
    """, unsafe_allow_html=True)
