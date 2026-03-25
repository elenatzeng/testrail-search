import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 🚀 名字框框加粗、弧形與發光感修正 */
        .author-tag { 
            font-size: 11px; 
            border-radius: 25px; /* 更圓潤的弧形 */
            padding: 2px 14px; 
            display: inline-block; 
            margin-left: 10px; 
            font-weight: bold; 
            border: 2px solid !important; /* 👈 加粗邊框 */
            background: rgba(0,0,0,0.3) !important;
            box-shadow: 0 0 5px rgba(0,0,0,0.5); /* 增加一點點立體深度 */
        }
        
        .view-btn { 
            display: inline-block; padding: 6px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 13px; font-weight: bold; 
        }

        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; padding: 15px; 
            border-radius: 10px; border: 1px solid #30363d; margin-top: 5px; 
            white-space: pre-wrap; line-height: 1.6;
        }

        /* 🚀 活力橘按鈕位置 (確保不被擋住) */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 30px; width: 48px; height: 48px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 999999; box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            text-decoration: none !important; display: flex; align-items: center; justify-content: center;
            font-size: 20px; transition: 0.3s;
        }
        .scroll-to-top:hover { transform: translateY(-5px); background-color: #e67600; }

        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
