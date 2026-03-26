import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 🌌 核心全域鎖死：地毯式抹除所有白色背景 */
        html, body, .stApp, 
        [data-testid="stAppViewContainer"], 
        [data-testid="stHeader"], 
        [data-testid="stSidebar"], 
        [data-testid="stSidebarContent"],
        [data-testid="stToolbar"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
            color: #c9d1d9 !important;
        }

        /* 2. 🛡️ 隱藏所有系統級 UI，防止白邊閃爍 */
        header, [data-testid="stHeader"], #MainMenu, footer {
            display: none !important;
        }
        
        /* 3. 🚀 火箭回到頂部按鈕 - 樣式與發光鎖死 */
        .scroll-to-top {
            position: fixed;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important;
            height: 42px !important;
            background-color: #f77f00 !important;
            color: white !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            font-size: 20px !important;
            text-decoration: none !important;
            z-index: 999999 !important;
            box-shadow: 0 0 15px rgba(247, 127, 0, 0.6) !important;
        }
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 0 25px rgba(247, 127, 0, 0.9) !important;
        }

        /* 4. 🚀 名字標籤樣式 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.6) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 5. 🟢 靈魂綠線與黑盒子 (顏值守護) */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 30px;
            display: block;
        }
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
            color: #c9d1d9 !important;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
        }

        /* 6. Expander 與輸入框強制去白 */
        .streamlit-expanderHeader, .stTextInput>div>div>input, .stButton>button {
            background-color: #161b22 !important;
            color: #adb5bd !important;
            border: 1px solid #30363d !important;
        }
        .stExpander { border: none !important; background: transparent !important; }

        /* 7. 📸 圖片與破圖標籤 - 徹底消失術 */
        img, [data-testid="stImage"] {
            display: none !important;
        }

        /* 8. 修正側邊欄內的文字與標籤 */
        [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
            color: #8b949e !important;
        }
        </style>
    """, unsafe_allow_html=True)
