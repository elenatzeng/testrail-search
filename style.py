import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤 (純色邊框) */
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
        
        /* 🚀 靈魂綠線：左側連貫長線 */
        .step-wrapper {
            border-left: 4px solid #4CAF50 !important; 
            padding-left: 20px !important;
            margin-left: 2px !important;
            margin-bottom: 25px !important;
            display: block !important;
        }
        .step-label { color: #ffffff !important; font-weight: bold !important; font-size: 15px !important; margin-bottom: 8px; }
        
        /* 🚀 核心黑盒子：強烈支持斷行與階層 */
        .step-box { 
            background-color: #1c2128 !important; border: 1px solid #30363d !important; 
            border-radius: 12px !important; padding: 18px 22px !important; color: #c9d1d9 !important; 
            font-size: 14px !important; line-height: 1.8 !important; margin-bottom: 15px !important;
            /* 🔥 這是保留換行的關鍵 */
            white-space: pre-wrap !important; 
            display: block !important;
        }

        /* 🔥 處理清單階層的 CSS (對齊 image_7bc4e9 截圖) */
        .step-box ul, .step-box ol {
            margin-left: 20px !important;
            padding-left: 5px !important;
            margin-top: 5px !important;
            margin-bottom: 5px !important;
        }
        .step-box li {
            margin-bottom: 8px !important;
            list-style-position: outside !important;
        }
        /* 針對第二階層以後的縮排 */
        .step-box li > ul, .step-box li > ol {
            margin-left: 25px !important;
            list-style-type: circle !important; /* 第二階變空心圓 */
        }

        .no-content-hint { color: #666; font-size: 14px; margin-top: 10px; font-style: italic; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
