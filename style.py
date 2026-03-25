import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 輸入框樣式 */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important; border: 1px solid #30363d !important;
            color: #ffffff !important; border-radius: 8px !important; height: 45px !important;
        }

        /* 按鈕基礎樣式 */
        button[kind="secondary"] {
            height: 45px !important; width: 100% !important;
            background-color: #31333f !important; color: #ffffff !important; 
            border: 1px solid #444c56 !important; border-radius: 8px !important;
        }

        .case-path-text { font-size: 13px; color: #8b949e !important; margin-bottom: 8px; display: block; }
        .author-tag { font-size: 11px; border-radius: 12px; padding: 3px 12px; display: inline-block; margin-left: 10px; font-weight: bold; }
        
        .view-btn { 
            display: inline-block; padding: 8px 20px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; 
        }

        /* ✨ 漂亮步驟版本容器 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #161b22; padding: 20px; 
            border-radius: 10px; border: 1px solid #30363d; margin-top: 10px; white-space: pre-wrap;
            line-height: 1.8; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .expected-text { color: #f77f00; font-weight: bold; margin-top: 10px; display: block; border-top: 1px dashed #30363d; padding-top: 10px; }

        /* 🚀 活力橘回到頂端按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 75px; right: 25px; width: 46px; height: 46px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            text-decoration: none !important; transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center; font-size: 20px;
        }
        .scroll-to-top:hover { transform: translateY(-5px); background-color: #e67600; }

        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
