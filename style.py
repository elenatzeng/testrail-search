import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：純色邊框，無發光 */
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

        /* 🚀 (9) 測試步驟 Expander：完全透明化，只留標題文字 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stExpander summary { color: #8b949e !important; padding-left: 0 !important; }
        
        /* 🚀 步驟呈現方式：回歸截圖中的簡約感 */
        .step-container { 
            border-left: 3px solid #2ea44f; 
            padding-left: 15px; 
            margin: 15px 0; 
        }
        .step-label { color: #ffffff; font-weight: bold; font-size: 14px; margin-bottom: 4px; }
        .step-text { color: #c9d1d9; font-size: 15px; margin-bottom: 12px; white-space: pre-wrap; }

        .view-btn { 
            display: inline-block; padding: 7px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; 
            font-size: 14px; font-weight: bold; 
        }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
