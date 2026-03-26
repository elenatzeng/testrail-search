import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 背景 */
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 作者標籤：恢復扎實感 */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; 
            padding: 3px 14px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 12px !important; 
            font-weight: 700 !important; /* 👈 加粗一點，不再虛虛的 */
            border: 2px solid !important; /* 👈 線條加粗到 2px */
            background: rgba(0,0,0,0.6) !important;
            vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：強化邊框亮度 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1.5px solid #444c56 !important; /* 👈 邊框顏色調亮，線條加粗 */
            border-radius: 10px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important;
            font-weight: 400 !important; /* 👈 內文保持細體，視覺才乾淨 */
            line-height: 1.7;
            margin-bottom: 10px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3); /* 👈 增加陰影更有份量 */
        }

        /* 🚀 列表縮進排版 */
        .list-item {
            display: block;
            padding-left: 24px;
            text-indent: -24px;
            margin-bottom: 4px;
        }

        /* 🚀 (10) Open Case 按鈕：強力鎖死無底線 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 8px 18px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; /* 🔥 絕對禁止底線 */
            font-size: 14px !important; 
            font-weight: 600 !important; 
            border: none !important;
        }

        /* 🚀 【修正：火箭左側置中】 */
        .scroll-to-top {
            position: fixed !important;
            top: 60% !important; /* 👈 放在中間偏下一點，避開展開鈕 */
            left: 15px !important; /* 👈 移到左邊 */
            width: 45px !important; 
            height: 45px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 50% !important;
            z-index: 99999 !important; 
            display: flex !important; 
            align-items: center; 
            justify-content: center;
            text-decoration: none !important; 
            font-size: 22px !important; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        }

        /* 側邊欄控制鈕 (>>) */
        [data-testid="stSidebarCollapsedControl"] {
            top: 45% !important; /* 👈 放在中間偏上一點 */
            left: 15px !important;
            position: fixed !important;
            background-color: rgba(255,255,255,0.2) !important;
            border-radius: 50% !important;
            z-index: 100000 !important;
        }
        </style>
    """, unsafe_allow_html=True)
