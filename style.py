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

        /* 🚀 主標題縮放 (32px) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; padding-top: 10px !important; padding-bottom: 5px !important; }

        /* 🚀 作者標籤、黑盒子、按鈕樣式 */
        .author-tag { font-size: 12px !important; border-radius: 20px !important; padding: 2px 12px !important; display: inline-flex !important; align-items: center; margin-left: 10px !important; font-weight: 600 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; color: white !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 15px 20px; color: #c9d1d9 !important; font-size: 14px !important; font-weight: 400 !important; line-height: 1.6; }
        .view-btn, .view-btn:link, .view-btn:visited { display: inline-block !important; padding: 6px 14px !important; background-color: #2ea44f !important; color: white !important; border-radius: 6px !important; text-decoration: none !important; font-size: 13px !important; font-weight: 600 !important; border: none !important; }

        /* 🚀 精制圓火箭 */
        .scroll-to-top {
            position: fixed !important; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important;
            width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; 
            border-radius: 50% !important; z-index: 10000000 !important; display: flex !important; align-items: center !important; justify-content: center !important;
            text-decoration: none !important; box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }

        /* 🚀 左側展開鈕：強制置頂 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important; top: 50% !important; left: 0px !important; transform: translateY(-50%) !important;
            width: 40px !important; height: 65px !important; background-color: rgba(255,255,255,0.1) !important; 
            border-radius: 0 35px 35px 0 !important; display: flex !important; justify-content: center !important; align-items: center !important;
            z-index: 10000001 !important; visibility: visible !important; 
        }
        [data-testid="stSidebarCollapsedControl"] svg { fill: white !important; color: white !important; width: 25px !important; height: 25px !important; }

        /* 🛡️ 隱藏雜物 */
        [data-testid="stHeader"] { background: transparent !important; }
        footer { display: none !important; }
        
        /* 🎯 精準刺殺：只隱藏那隻貓 (Deploy 按鈕) */
        .stDeployButton, [data-testid="stDeployButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 內容收合時吸附左側 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main { padding-left: 0 !important; margin-left: 0 !important; }
        .block-container { padding-top: 2.5rem !important; }
        </style>
    """, unsafe_allow_html=True)
