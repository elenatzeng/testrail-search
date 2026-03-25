import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：膠囊形狀、純色邊框 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 🚀 (9) Expander 透明化 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stExpander summary { color: #8b949e !important; padding: 10px 0 !important; }
        
        /* 🚀 靈魂綠線：左側垂直長線 */
        .step-wrapper {
            border-left: 4px solid #4CAF50; 
            padding-left: 20px;
            margin-left: 2px;
            margin-bottom: 25px;
            box-shadow: -5px 0 10px rgba(76, 175, 80, 0.2); /* 微發光 */
        }
        .step-label { color: #ffffff; font-weight: bold; font-size: 15px; margin-bottom: 6px; }
        
        /* 🚀 斷行修復：強制保留原始換行文字 */
        .step-box { 
            background-color: #1c2128 !important; border: 1px solid #30363d; 
            border-radius: 12px; padding: 18px 22px; color: #c9d1d9; 
            font-size: 14px; line-height: 1.6; margin-bottom: 15px;
            white-space: pre-wrap !important; /* 🔥 這是保留換行的關鍵 */
            word-wrap: break-word !important;
        }
        .no-content-hint { color: #666; font-size: 14px; margin-top: 10px; font-style: italic; }

        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
