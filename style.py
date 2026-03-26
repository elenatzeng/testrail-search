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

        /* 🚀 【核心修正】讓內容收起時完全靠左 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main {
            padding-left: 0 !important;
            margin-left: 0 !important;
        }
        
        [data-testid="stAppViewContainer"] .block-container {
            max-width: 92% !important;
            padding-top: 2rem !important; 
            margin: 0 auto !important;
        }

        /* 🚀 【懸浮 >> 按鈕】永遠靠右上 */
        /* 當側邊欄收合時，Streamlit 的控制項會被搬移到這裡 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            right: 20px !important; /* 靠右 */
            top: 20px !important;   /* 靠上 */
            left: auto !important;  /* 取消左邊定位 */
            display: flex !important;
            visibility: visible !important;
            width: 45px !important;
            height: 45px !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border-radius: 50% !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 1000001 !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6) !important;
            cursor: pointer !important;
        }
        
        /* 讓 >> 圖示變亮白色 */
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            color: white !important;
            width: 24px !important;
            height: 24px !important;
        }

        /* 🚀 展開時的收合按鈕 (<<) 樣式統一 */
        [data-testid="stSidebarCollapseButton"] button {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
        }

        /* 🚀 【綠色按鈕】鎖死無底線 */
        .view-btn, .view-btn:link, .view-btn:visited {
            display: inline-block !important;
            padding: 10px 22px !important;
            background-color: #2ea44f !important;
            color: white !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-size: 14px !important;
            font-weight: bold !important;
            border: none !important;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            text-decoration: none !important;
            transform: scale(1.05);
        }

        /* 🛡️ 隱藏系統雜物 */
        [data-testid="stHeader"], header { display: none !important; }
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
        
        /* 🚀 火箭位置微調：移到右下角，避免撞到右上按鈕 */
        .scroll-to-top {
            position: fixed; 
            bottom: 30px !important; /* 放到右下角 */
            right: 25px !important;
            width: 45px !important; 
            height: 45px !important;
            background-color: #f77f00 !important; 
            color: white !important;
            border-radius: 50% !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center;
