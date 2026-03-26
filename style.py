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

        /* 🚀 【消滅左側空隙】當側邊欄收合時，主內容橫向撐開 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            width: 100vw !important;
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        
        /* 內容容器置中設定 */
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            margin: 0 auto !important;
            padding-top: 3.5rem !important; 
            transition: all 0.3s ease-in-out;
        }

        /* 🚀 【救援按鈕復活】強制顯示展開按鈕 (>>) */
        /* 定位在左上角，確保不會消失 */
        button[kind="header"] {
            display: flex !important;
            visibility: visible !important;
            position: fixed !important;
            left: 15px !important;
            top: 15px !important;
            z-index: 999999 !important;
            width: 40px !important;
            height: 40px !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 50% !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.5) !important;
        }

        /* 收合按鈕 (<<) 樣式統一 */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
        }

        button[kind="header"] svg, [data-testid="stSidebarCollapseButton"] svg {
            fill: white !important;
            color: white !important;
        }

        /* 🛡️ 隱藏雜物，但保留 header 按鈕的可見度 */
        header, [data-testid="stHeader"] { 
            background: transparent !important;
        }
        #MainMenu, footer { display: none !important; }

        /* 🚀 側邊欄寬度固定 */
        [data-testid="stSidebar"] { min-width: 300px !important; max-width: 300px !important; }

        /* 🚀 標題與標籤 (15px / 13px) */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🔥 黑盒子鎖死 */
        .content-box {
            background: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px;
            padding: 18px 20px;
        }
        .content-box *, .inner-text, .inner-text * {
            background: transparent !important;
            color: #c9d1d9 !important;
        }
        
        .scroll-to-top {
            position: fixed; top: 50% !important; right:
