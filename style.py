import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 🌌 靈魂星空背景 - 強制鎖死深色 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
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
        
        /* 3. 🚀 火箭回到頂部按鈕 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important;
            color: white !important; border-radius: 50% !important;
            display: flex !important; align-items: center; justify-content: center;
            font-size: 20px !important; text-decoration: none !important;
            z-index: 999999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
        }

        /* 4. 🟢 靈魂綠線與「絕對去白」黑盒子 */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px; margin-left: 5px; margin-bottom: 30px; display: block;
        }
        
        /* 🔥 關鍵修正：強制抹除 content-box 內所有元素的背景色 */
        .content-box, .content-box div, .content-box p, .content-box span {
            background: #1c2128 !important; /* 統一使用黑盒子深灰色 */
            background-color: #1c2128 !important;
            color: #c9d1d9 !important;
            border: none !important;
        }

        .content-box {
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
            display: block;
            width: 100%;
        }

        /* 5. 🚀 名字標籤樣式 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.6) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 6. Expander 與按鈕鎖死深色 */
        .streamlit-expanderHeader, .stTextInput>div>div>input, .stButton>button {
            background-color: #161b22 !important;
            color: #adb5bd !important;
            border: 1px solid #30363d !important;
        }
        
        /* 7. 📸 圖片彻底蒸發 */
        img, [data-testid="stImage"] {
            display: none !important;
        }

        /* 8. 其他 UI 文字色彩修正 */
        label, .stMarkdown p { color: #8b949e !important; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
