import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 */
        .stApp {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
        }
        
        /* 胶囊形作者標籤 (對齊 image_3) */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-block !important;
            vertical-align: middle; margin-left: 10px !important; font-weight: bold;
        }
        .status-active { background-color: #2ea44f !important; color: white !important; }
        .status-inactive { background-color: #d73a49 !important; color: white !important; }

        /* Expander 透明化 (對齊 image_11) */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stExpander [data-testid="stExpanderToggleIcon"] { color: #8b949e !important; }
        
        /* 🚀 黑盒子內文字斷行鎖死 (修正斷行消失問題) */
        .step-box { 
            background-color: #161b22 !important; border: 1px solid #30363d; 
            border-radius: 6px; padding: 15px; color: #c9d1d9; font-size: 14px;
            /* 🔥 強制保留換行語法 */
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
            margin-bottom: 10px;
        }

        /* 🚀 靈魂綠線：連貫且從標題開始 */
        .step-container { 
            border-left: 4px solid #2ea44f; 
            padding-left: 15px; 
            margin-bottom: 20px; 
            margin-left: 5px;
        }
        .step-label { color: #ffffff; font-weight: bold; margin-bottom: 5px; font-size: 15px; }
        
        /* 捲動到頂部按鈕與作者標籤 */
        .view-btn { display: inline-block; padding: 5px 10px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold; }
        
        /* 🚀 回到頂部火箭按鈕 - 整個圈圈大瘦身 */
        .scroll-to-top {
            position: fixed;
            bottom: 40px; /* 往下移一點點 */
            right: 25px; /* 往右移一點點 */
            width: 50px; /* 瘦身 1/6 */
            height: 50px; /* 瘦身 1/6 */
            background-color: #f77f00; /* 亮橘色 */
            color: white !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px; /* 火箭縮小一點點 */
            text-decoration: none !important;
            z-index: 9999;
            transition: all 0.3s ease;
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.6); /* 溫和發光 */
        }
        .scroll-to-top:hover {
            transform: translateY(-8px); /* 輕輕飛 */
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.9); /* ✨ 更強發光 */
        }
        </style>
    """, unsafe_allow_html=True)
