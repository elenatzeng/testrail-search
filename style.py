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

        /* 🚀 (8) 名字標籤：膠囊形狀、不再使用超粗字體 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 500 !important; /* 👈 取消超粗體，改為中等粗度 */
            border: 1px solid !important; 
            background: rgba(255,255,255,0.05) !important;
            vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 (9) 核心黑盒子：妳喜歡的精緻感 */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important;
            font-size: 14px !important;
            font-weight: 400 !important; /* 👈 內文不使用粗體 */
            line-height: 1.6;
            margin-bottom: 10px;
        }

        /* 🚀 (10) Open Case 按鈕：亮綠色、無底線 */
        .view-btn { 
            display: inline-block !important; 
            padding: 6px 14px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; /* 👈 徹底消滅底線 */
            font-size: 13px !important; 
            font-weight: 600 !important; 
            transition: 0.3s;
        }
        .view-btn:hover {
            background-color: #3fb950 !important;
            text-decoration: none !important;
            transform: translateY(-1px);
        }

        /* 🚀 調整側邊欄收合按鈕位置，避免擋到內容 */
        [data-testid="stSidebarCollapsedControl"] {
            top: 10px !important;
            left: 10px !important;
            background-color: rgba(255,255,255,0.1) !important;
            border-radius: 50% !important;
        }

        /* 🚀 隱藏 Streamlit 原生雜物 */
        [data-testid="stHeader"], header { background: transparent !important; }
        footer { display: none !important; }
        
        /* 火箭按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 30px; right: 25px; width: 45px; height: 45px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; font-size: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        </style>
    """, unsafe_allow_html=True)
