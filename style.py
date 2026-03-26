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
        
        /* 2. 🛡️ 隱藏選單與工具列，防止手動切換 */
        header, #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        /* 3. 🔥 核心修正：究極縮小左側與右側的間距 ( image_14.png 指示) */
        /* 把側邊欄寬度縮小，並把右側區域的 padding 移除 */
        [data-testid="stSidebar"] {
            width: 280px !important; # 縮小側邊欄寬度
        }
        [data-testid="stAppViewContainer"] > .main {
            padding-left: 20px !important; # 縮小左側 padding
            padding-right: 20px !important;
        }
        /* 縮小 columns 之間的 gap */
        div[data-testid="stVerticalBlock"] > div > div[data-testid="stHorizontalBlock"] {
            gap: 10px !important;
        }

        /* 4. 🟢 恢復漂亮的黑盒子與靈魂綠線 */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 25px;
            display: block;
        }
        
        /* 🔥 文字絕對去白鎖死樣式 */
        .content-box {
            background: #1c2128 !important; # 鎖死黑盒子深灰
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 15px 20px;
            color: #c9d1d9 !important;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
        }
        /* 精準地毯式去白：content-box 下的所有文字容器 */
        .content-box div, .content-box p, .content-box span {
            background-color: #1c2128 !important; # 強制鎖死背景色，不讓 st.markdown 亂加白底
            background: #1c2128 !important;
            color: #c9d1d9 !important; # 鎖死文字顏色
        }

        /* 5. Expander 標題區美化與鎖死深色 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            color: #adb5bd !important;
        }
        
        /* 6. 文字顏色修正 */
        h1, h2, h3, p, span, label {
            color: #adb5bd !important;
        }
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #adb5bd !important;
        }
        
        /* 7. 按鈕與輸入框深色美化 (💾, 🔄 按鈕回歸) */
        .stTextInput>div>div>input, .stButton>button, .stNumberInput input {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        
        /* 8. 📸 圖片与破圖徹底消失術 ( image_4.png 指示) */
        img, [data-testid="stImage"] { display: none !important; }
        
        /* 其他 UI 元件 */
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 0 10px 25px !important; font-style: italic !important; display: block !important; }
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)
