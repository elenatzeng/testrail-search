import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🚀 【消滅白線與空隙】側欄收起時內容完全吸附 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] [data-testid="stSidebar"] {
            margin-left: -300px !important;
            border: none !important;
        }
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
            width: 100vw !important;
        }

        /* 🚀 主內容區置中 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 3.5rem !important; 
            transition: all 0.3s ease-in-out !important;
        }

        /* 🚀 【綠色 Open Case 按鈕】鎖死樣式 */
        .view-btn {
            display: inline-block !important;
            padding: 8px 18px !important;
            background-color: #2ea44f !important; /* 紮實的綠色 */
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important; /* 🔥 徹底消滅底線 */
            font-size: 14px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
            transition: transform 0.2s, background-color 0.2s !important;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            transform: scale(1.05) !important;
            text-decoration: none !important; /* 懸停也不准有底線 */
        }

        /* 🚀 【救援按鈕】樣式統一 */
        button[kind="header"], [data-testid="stSidebarCollapseButton"] button {
            width: 42px !important;
            height: 42px !important;
            background-color: rgba(255, 255, 255, 0.15) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
        }
        button[kind="header"] { position: fixed !important; left: 12px !important; top: 12px !important; z-index: 1000000 !important; }

        /* 🛡️ 隱藏所有白線分隔與系統雜物 */
        hr, .stMarkdown hr { display: none !important; } /* 🔥 消滅白線 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🔥 黑盒子鎖死 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }

        /* 標籤 */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
