import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 背景與文字基礎 */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { background-color: #0b0e14 !important; }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { color: #ffffff !important; }

        /* 側邊欄輸入框與按鈕 */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        div[data-testid="stSidebar"] .stButton button { 
            background-color: #31333f !important; 
            color: #ffffff !important; 
            border: 1px solid #444c56 !important;
            border-radius: 8px !important;
            width: 100% !important;
        }

        /* 📂 淺灰色路徑字體 */
        .case-path-text { 
            font-size: 13px; 
            color: #a1a1a1 !important; 
            margin-bottom: 8px; 
            display: block;
        }

        /* 🚦 作者標籤與燈號 */
        .author-tag { 
            font-size: 11px; 
            border-radius: 12px; 
            padding: 3px 12px; 
            display: inline-block; 
            margin-left: 10px; 
            font-weight: bold; 
        }
        
        /* 📖 Open Case 綠色按鈕 */
        .view-btn { 
            display: inline-block; 
            padding: 6px 16px; 
            background-color: #4CAF50; 
            color: white !important; 
            border-radius: 6px; 
            text-decoration: none; 
            font-size: 13px; 
            font-weight: bold; 
        }

        /* ✨ 步驟美化容器 */
        .step-content-box { 
            color: #ffffff !important; 
            background: #1c2128; 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid #30363d; 
            margin-top: 5px; 
            white-space: pre-wrap; 
        }
        .step-item { 
            border-left: 5px solid #4CAF50; 
            padding-left: 20px; 
            margin-bottom: 25px; 
        }

        /* 🚀 回到頂端懸浮按鈕 (Fixed Position) */
        .scroll-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 45px;
            height: 45px;
            background-color: #4CAF50;
            color: white !important;
            border-radius: 50%;
            text-align: center;
            line-height: 42px;
            font-size: 20px;
            cursor: pointer;
            z-index: 99999;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            text-decoration: none !important;
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.2);
        }
        .scroll-to-top:hover {
            transform: translateY(-5px);
            background-color: #45a049;
            box-shadow: 0 6px 20px rgba(76,175,80,0.4);
        }

        /* 隱藏 Streamlit 預設裝飾 */
        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
