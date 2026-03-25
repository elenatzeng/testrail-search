import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：去發光，保留純色邊框 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; 
            padding: 4px 14px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 15px !important; 
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.3) !important;
            vertical-align: middle;
        }

        /* 🟢 在職 (無發光版) */
        .status-active {
            color: #32CD32 !important;
            border-color: #32CD32 !important;
        }

        /* 🔴 離職 (無發光版) */
        .status-inactive {
            color: #FF4B4B !important;
            border-color: #FF4B4B !important;
        }
        
        /* 🚀 (9) 測試步驟 Expander：維持單一灰色盒子感 */
        .stExpander { border: none !important; }
        .stExpander summary {
            background-color: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 10px !important;
            padding: 10px 15px !important;
            color: #8b949e !important;
        }
        .stExpander[open] summary { border-radius: 10px 10px 0 0 !important; }
        .stExpander[open] > div {
            background-color: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
        }

        .step-content-box { color: #c9d1d9 !important; line-height: 1.8; white-space: pre-wrap !important; }
        .step-container { border-left: 4px solid #2ea44f; padding-left: 18px; margin-bottom: 20px; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
