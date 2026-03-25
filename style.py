import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：純色邊框，無發光 */
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
        .stExpander summary { color: #8b949e !important; padding: 10px 0 !important; margin-left: 0px !important; }
        
        /* 🚀 靈魂綠線：左側垂直長線 (對齊 image_14 和 image_19) */
        .step-container { 
            border-left: 4px solid #4CAF50 !important; /* 亮綠色垂直長線 */
            padding-left: 20px !important; 
            margin-left: 2px !important;
            margin-bottom: 25px !important; 
            position: relative;
        }
        .step-label { 
            color: #ffffff !important; 
            font-weight: bold !important; 
            font-size: 15px !important; 
            margin-bottom: 8px !important; 
        }

        /* 🚀 核心黑盒子：斷行鎖死 (修正 Expected 沒斷行問題) */
        .step-box { 
            background-color: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px !important; 
            padding: 18px 22px !important; 
            color: #c9d1d9 !important; 
            font-size: 14px !important; 
            line-height: 1.8 !important;
            margin-bottom: 15px !important;
            /* 🔥 強制保留斷行文字 */
            white-space: pre-wrap !important; 
            /* 🔥 🔥 超重要：對付 Expected 這種沒空格超長文字的終極換行 */
            overflow-wrap: anywhere !important; 
            word-break: break-all !important;
            display: block !important;
        }

        /* 🔥 🔥 將黑盒子裡的 Markdown 清單 (如 1.) 的左邊距推回去左邊對齊綠線 */
        .step-box p, .step-box ul, .step-box ol {
            margin-left: 0 !important;
            padding-left: 0 !important;
        }
        .step-box ul, .step-box ol {
            margin-left: 20px !important; /* 保留基礎縮排供清單層次用 */
            list-style-position: outside !important;
        }
        
        .no-content-hint { color: #666; font-size: 14px; margin-top: 10px; font-style: italic; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
