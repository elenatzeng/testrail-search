import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        
        /* 🚀 靈魂綠線容器 */
        .custom-step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px !important;
            margin: 10px 0 30px 5px !important;
            display: block !important;
        }

        .custom-label { color: #ffffff !important; font-weight: bold !important; font-size: 15px !important; margin-bottom: 8px; display: block; }

        /* 🚀 核心黑盒子 */
        .custom-box { 
            background-color: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px !important; 
            padding: 18px 22px !important; 
            color: #c9d1d9 !important; 
            font-size: 14px !important; 
            line-height: 1.8 !important;
            margin-bottom: 15px !important;
            white-space: pre-wrap !important; 
            word-break: break-all !important;
            display: block !important;
        }

        /* 🚀 (修正) 無文字內容的提示文字 - 讓它顯現出來 */
        .no-content-hint { 
            color: #8b949e !important; 
            font-size: 14px !important; 
            padding: 15px 0 15px 25px !important; 
            font-style: italic !important;
            display: block !important;
        }

        /* 🚀 (修正) 火箭按鈕 - 縮小 + 固定在右邊中間 */
        .scroll-to-top {
            position: fixed;
            top: 50% !important; /* 垂直中間 */
            right: 15px !important; /* 貼齊右邊 */
            transform: translateY(-50%) !important;
            width: 42px !important; /* 精緻瘦身 */
            height: 42px !important; 
            background-color: #f77f00 !important; 
            color: white !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            font-size: 20px !important; /* 火箭也縮小 */
            text-decoration: none !important;
            z-index: 99999 !important;
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
            border: none !important;
        }
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8) !important;
        }

        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
