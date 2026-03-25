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
        
        /* 胶囊形作者標籤 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-block !important;
            vertical-align: middle; margin-left: 10px !important; font-weight: bold;
        }
        .status-active { background-color: #2ea44f !important; color: white !important; }
        .status-inactive { background-color: #d73a49 !important; color: white !important; }

        /* Expander 樣式修正 */
        .stExpander { border: none !important; box-shadow: none !important; }
        .stExpander [data-testid="stExpanderToggleIcon"] { color: #8b949e !important; }
        
        /* 🚀 (6)(7)(8) 黑盒子內文字斷行鎖死 */
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
        
        /* 其他按鈕與捲動樣式 */
        .view-btn { display: inline-block; padding: 5px 10px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold; }
        
        /* 🚀 火箭回到頂部按鈕 (移除白線，加入發光) */
        .scroll-to-top {
            position: fixed;
            bottom: 60px;
            right: 30px;
            width: 60px;
            height: 60px;
            background-color: #f77f00; /* 亮橘色 */
            color: white !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            text-decoration: none !important;
            z-index: 9999;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(247, 127, 0, 0.7); /* ✨ 橘色發光 */
        }
        .scroll-to-top:hover {
            transform: translateY(-10px); /* 懸停時往上飛 */
            box-shadow: 0 0 30px rgba(247, 127, 0, 1); /* ✨ 更強發光 */
        }
        </style>
    """, unsafe_allow_html=True)
