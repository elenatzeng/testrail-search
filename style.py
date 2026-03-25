import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤 (純色邊框版) */
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
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 🚀 (9) Expander 透明化 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stExpander summary { color: #8b949e !important; padding: 10px 0 !important; }
        
        /* 🚀 高級黑盒子佈局 (對照截圖) */
        .step-container { 
            border-left: 4px solid #4CAF50; /* 靈魂綠線 */
            padding-left: 20px; 
            margin-bottom: 30px; 
            position: relative;
        }
        .step-label { 
            color: #ffffff; 
            font-weight: bold; 
            font-size: 16px; 
            margin-bottom: 8px; 
            margin-top: 10px;
        }
        .step-box { 
            background-color: #1c2128 !important; /* 核心黑盒子顏色 */
            border: 1px solid #30363d; 
            border-radius: 12px; 
            padding: 18px 22px; 
            color: #c9d1d9; 
            font-size: 15px; 
            line-height: 1.6;
            margin-bottom: 15px;
            white-space: pre-wrap;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        }

        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
