import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 🌌 全域永夜星空背景鎖死 */
        .stApp, [data-testid="stSidebar"], .stAppViewContainer {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }
        
        /* 2. 🛡️ 隱藏選單與工具列 */
        header, #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }
        
        /* 3. 🔥 核心修正：抹除黑盒子裡所有文字容器的白底 ( image_16.png 指示) */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 25px;
            display: block;
        }
        
        .content-box {
            background: #1c2128 !important; # 黑盒子基礎深灰
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
            color: #c9d1d9 !important;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
            display: block;
            width: 100%;
        }

        /* 🚀 終極文字去白核彈：強制 content-box 下所有文字容器背景變透明 */
        .content-box div, .content-box p, .content-box span, .content-box pre, .content-box code {
            background-color: transparent !important; # 徹底抹除白底
            background: transparent !important;
            color: #c9d1d9 !important; # 鎖死文字顏色
        }

        /* 4. Expander 標題區美化 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            color: #adb5bd !important;
        }
        
        /* 5. 文字顏色修正 */
        h1, h2, h3, p, span, label {
            color: #adb5bd !important;
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #adb5bd !important;
        }
        
        /* 6. 按鈕與輸入框深色美化 (💾, 🔄 按鈕回歸) */
        .stTextInput>div>div>input, .stButton>button, .stNumberInput input {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        
        /* 7. 📸 圖片彻底蒸發 ( image_4.png 指示) */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 其他 UI 元件 */
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 0 10px 25px !important; font-style: italic !important; display: block !important; }
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)
