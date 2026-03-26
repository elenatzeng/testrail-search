import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 🌌 星空背景鎖死 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 2. 🛡️ 抹除所有系統殘留白邊 */
        header, [data-testid="stHeader"], #MainMenu, footer { display: none !important; }

        /* 3. 🟢 靈魂綠線容器 */
        .step-container {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px; margin-left: 5px; margin-bottom: 30px;
        }
        
        /* 4. 🔥 核心修正：黑盒子與內部文字強制去白 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
            display: block; width: 100%;
        }

        /* 這裡是最強悍的去白指令：強制盒子內所有東西背景透明 */
        .content-box *, .inner-text, .inner-text * {
            background: transparent !important;
            background-color: transparent !important;
            color: #c9d1d9 !important;
        }

        /* 5. 🚀 火箭回到頂部 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important;
            color: white !important; border-radius: 50% !important;
            display: flex !important; align-items: center; justify-content: center;
            z-index: 999999 !important; box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
        }

        /* 6. 其他 UI 元件 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #adb5bd !important;
        }
        img { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
