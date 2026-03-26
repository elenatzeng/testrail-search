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

        /* 🚀 【消滅 1 號按鈕】徹底隱藏頂部 Deploy/Share 工具列 */
        [data-testid="stHeader"] { display: none !important; }
        header { display: none !important; }

        /* 🚀 【修正內容靠左】當側欄收起時，內容吸附到最左邊 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 95% !important;
            padding-top: 3.5rem !important; 
            margin: 0 auto !important;
        }

        /* 🚀 【展開/收合按鈕樣式】固定在左上角 */
        button[kind="header"] {
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 999999 !important;
            width: 42px !important;
            height: 42px !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
        }
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
        }
        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
        }

        /* 🚀 【修正 3 號按鈕】強力鎖死綠色 Open Case (無底線) */
        /* 使用 a 標籤全域攔截，確保不變回藍色 */
        .view-btn, .view-btn:link, .view-btn:visited, .view-btn:active {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important; /* 紮實綠色 */
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important; /* 🔥 絕對禁止底線 */
            font-size: 14px !important;
            font-weight: bold !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            text-decoration: none !important;
            transform: scale(1.05);
        }

        /* 🛡️ 隱藏雜物與白線 */
        hr, .stMarkdown hr { display: none !important; }
        #MainMenu, footer { display: none !important; }

        /* 🔥 黑盒子 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        /* 火箭回到頂部 (水平置中於右側) */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 20px !important;
            transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important;
            border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; z-index: 99999 !important;
        }

        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        img, [data-testid="stImage"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
