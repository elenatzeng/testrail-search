import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 - 全域鎖定 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🚀 頂部工具欄固定 (Glassmorphism 毛玻璃效果) */
        [data-testid="stHeader"] {
            position: fixed !important;
            top: 0 !important;
            z-index: 1000001 !important;
            background: rgba(11, 14, 20, 0.8) !important;
            backdrop-filter: blur(12px) !important;
            border-bottom: 1px solid rgba(255,255,255,0.1) !important;
        }

        /* 🎯 精準刺殺：隱藏 Deploy 按鈕 (GitHub 貓咪) */
        .stDeployButton, [data-testid="stDeployButton"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* 🚀 主標題縮放 (32px) */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: white !important;
            padding-top: 10px !important;
            padding-bottom: 5px !important;
        }

        /* 🚀 作者標籤基礎樣式 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important; 
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
        }

        /* 🟢 在職 (Active)：綠字綠框 */
        .status-active { 
            color: #32CD32 !important; 
            border-color: #32CD32 !important; 
            background: rgba(0,0,0,0.5) !important;
        }

        /* 🔴 離職 (Inactive)：紅字、紅框、紅底 (鎖死雷包視覺) */
        /* 使用更高階選擇器確保覆蓋妳之前看到的白色邊框 */
        span.author-tag.status-inactive { 
            color: #FF4B4B !important; 
            border-color: #FF4B4B !important; 
            background: rgba(255, 75, 75, 0.2) !important; 
            box-shadow: 0 0 8px rgba(255, 75, 75, 0.4) !important;
        }

        /* 🚀 內容盒與步驟樣式 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important; 
            font-size: 14px !important; 
            line-height: 1.6; 
        }

        /* 📖 Open Case 按鈕樣式 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 6px 14px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 13px !important; 
            font
