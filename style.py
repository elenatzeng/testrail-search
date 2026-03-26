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

        /* 🚀 【核心修正】消滅重疊的白色按鈕，讓內容吸附左側 */
        /* 當側邊欄收合時 (data-collapsed="true") */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
            max-width: 100vw !important; /* 強制寬度填滿 */
        }
        
        [data-testid="stAppViewContainer"] .main {
            transition: all 0.3s ease-in-out !important; /* 讓內容滑動順滑 */
        }

        /* 讓內容區塊在任何狀態下都保持漂亮置中，但不鎖死左邊 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 90% !important;
            padding-top: 3.5rem !important; /* 為左上角按鈕騰出空間 */
            margin: 0 auto !important; /* 負責水平置中 */
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        /* 🚀 【自定義 >> 按鈕】定位在左上角，消滅白色頭像按鈕 */
        button[kind="header"] {
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 999999 !important; /* 確保在最上層 */
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
        }

        /* 將原本的白色頭像按鈕藏掉 */
        .sc-fqkvSm.CAsgW { display: none !important; }

        /* 當側邊欄展開時 (<<按鈕) 樣式統一 */
        [data-testid="stSidebarCollapseButton"] button {
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }

        /* 按鈕內部的圖示顏色 (<< 和 >> 都變成白色) */
        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
            width: 22px !important;
            height: 22px !important;
        }

        /* 🛡️ 隱藏雜物 */
        header, [data-testid="stHeader"] { background: transparent !important; }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度設定 */
        [data-testid="stSidebar"] {
            min-width: 300px !important;
            max-width: 300px !important;
        }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; vertical-align: middle; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 18px 20px; }
        .content-box *, .inner-text, .inner-text * { background: transparent !important; color: #c9d1d9 !important; }
        
        /* 🔥 鎖死黑盒子，清除不漆黑 */
        #search_box_no_content, .no-content-hint {
            color: transparent !important; background: transparent !important; border: none !important; box-shadow: none !important; padding: 0 !important; height: 0 !important; overflow: hidden !important;
        }

        /* 火箭回到頂部 (修正位置) */
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
            z-index: 99999 !important;
        }

        img, [data-testid="stImage"] { display: none !important; }
        .stTextInput input { background-color: #161b22 !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; }
        </style>
    """, unsafe_allow_html=True)
