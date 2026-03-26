import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 🌌 全域永夜鎖死 */
        .stApp, [data-testid="stSidebar"], .stAppViewContainer {
            background-color: #0b0e14 !important;
        }
        
        /* 2. 🛡️ 隱藏所有選單與工具列 */
        header, #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        /* 3. 🟢 恢復完美的綠線與黑盒子結構 ( image_15.png 指示) */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 25px;
            display: block;
        }
        
        .content-box {
            background: #1c2128 !important; # 鎖死黑盒子深灰
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 15px 20px;
            color: #c9d1d9 !important;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
            display: block;
            width: 100%;
        }

        /* 🔥 文字絕對去白與層次顏色鎖死 */
        .inner-text div {
            background-color: transparent !important; # 徹底蒸發所有可能的白底
            background: transparent !important;
            line-height: 1.6;
            margin-bottom: 5px;
        }
        
        /* ✨ 階層文字顏色 (藍白) */
        .list-item { color: #e6edf3 !important; }
        
        /* 普通文字顏色 (灰白) */
        .normal-item { color: #adb5bd !important; }

        /* 4. Expander 標題區美化 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            color: #adb5bd !important;
        }
        
        /* 5. UI 元件顏色修正 */
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #adb5bd !important;
        }
        .stTextInput>div>div>input, .stButton>button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
        }
        
        /* 6. 📸 圖片与破圖彻底消失術 */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 7. 其他按鈕 */
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 0 10px 25px !important; font-style: italic !important; display: block !important; }
        .stExpander { border: none !important; background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)
