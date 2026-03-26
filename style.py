import streamlit as st

def apply_custom_style():
    # 🔥 黑科技：鎖死 Dark 模式，不讓它變白
    st.markdown("""
        <style>
        /* 核心介面鎖死黑星空 */
        .stApp, [data-testid="stSidebar"], .stTextInput input, .stNumberInput input, div[role="listbox"] {
            background-color: #0d1117 !important;
            color: #c9d1d9 !important;
        }
        
        /* 文字顏色鎖死灰白 */
        h1, h2, h3, h4, h5, p, span, li, label, .stMarkdown, .no-content-hint {
            color: #adb5bd !important;
        }
        
        /* 側邊欄標題與文字鎖死 */
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #adb5bd !important;
        }

        /* Expander (步驟區塊) 強制 Dark */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-color: #30363d !important;
        }
        .streamlit-expanderHeader:hover {
            background-color: #1f242c !important;
        }
        .streamlit-expanderContent {
            background-color: #0d1117 !important;
            border-color: #30363d !important;
        }
        
        /* 搜尋框框顏色鎖死 */
        .stTextInput>div>div>input {
            border: 1px solid #30363d !important;
            background-color: #161b22 !important;
        }
        
        /* 功能按鈕樣式回歸 */
        div.stButton > button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
        }
        div.stButton > button:hover {
            background-color: #30363d !important;
            border-color: #adb5bd !important;
        }
        
        /* 綠線與黑盒子 (這裡直接在 HTML 裡寫死，但 CSS 也保險一下) */
        [style*="border-left:4px solid #4CAF50"] {
            margin-top: 10px !important;
        }

        /* 分隔線鎖死 */
        hr {
            border-color: #30363d !important;
        }

        /* 下載與 Deploy 按鈕隱藏 ( image_18.png 指示) */
        div[data-testid="stToolbarDownloads"] { display: none !important; }
        div[data-testid="stToolbarDeploy"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
