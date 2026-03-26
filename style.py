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

        /* 🚀 (8) 作者標籤：邊框 2px 扎實感、名字強力加粗 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 3px 14px !important; /* 稍微增加內距 */
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 700 !important; /* 👈 【修改】名字強力加粗，不再虛虛的 */
            border: 2px solid !important; /* 👈 邊框鎖死 2px */
            background: rgba(0,0,0,0.6) !important;
            vertical-align: middle;
            color: white !important; /* 確保文字夠亮 */
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：內文 14px 不粗體 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important;
            font-weight: 400 !important; /* 👈 內文絕對不粗體，視覺才乾淨 */
            line-height: 1.6;
            margin-bottom: 10px;
        }

        /* 🚀 (10) Open Case 按鈕：亮綠色、絕對無底線 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 7px 16px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; /* 🔥 徹底消滅底線 */
            font-size: 13px !important; 
            font-weight: 600 !important; 
            border: none !important;
        }
        .view-btn:hover { background-color: #3fb950 !important; text-decoration: none !important; }

        /* 🚀 【修正：大字體文字版火箭按鈕】 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;   /* 垂直置中 */
            right: 0px !important;  /* 貼齊右邊邊緣 */
            transform: translateY(-50%) !important;
            width: auto !important;     /* 👈 寬度自適應文字 */
            min-width: 120px !important; /* 👈 設定最小寬度以容納文字 */
            height: 46px !important;    /* 稍微加高 */
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 23px 0 0 23px !important; /* 左半圓膠囊感 */
            z-index: 10000000 !important; 
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            padding: 0 20px !important;
            box-shadow: -4px 0 15px rgba(0,0,0,0.5) !important;
            transition: all 0.3s ease;
        }
        /* 按鈕內的文字樣式 */
        .scroll-to-top span {
            font-size: 16px !important; /* 👈 【修改】字體變大到 16px */
            font-weight: 700 !important; /* 👈 加粗 */
            margin-left: 10px !important;
            white-space: nowrap !important;
            color: white !important;
        }
        .scroll-to-top:hover { 
            background-color: #ff9f43 !important; 
            transform: translateY(-50%) scale(1.05) !important; 
        }

        /* 🚀 【左側展開鈕】同樣置中且半圓 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0px !important;
            transform: translateY(-50%) !important;
            width: 40px !important;
            height: 65px !important;
            background-color: #2ea44f !important; 
            border-radius: 0 35px 35px 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000001 !important;
            box-shadow: 4px 0 15px rgba(0,0
