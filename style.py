import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 灵魂星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🚀 主标题 (32px) */
        h1 { font-size: 32px !important; font-weight: 700 !important; color: white !important; }

        /* 🚀 作者标签、黑盒子、按钮样式保留 */
        .author-tag { font-size: 12px !important; border-radius: 20px !important; padding: 2px 12px !important; display: inline-flex !important; align-items: center; margin-left: 10px !important; font-weight: 600 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; color: white !important; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .content-box { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 12px; padding: 15px 20px; color: #c9d1d9 !important; font-size: 14px !important; font-weight: 400 !important; line-height: 1.6; }
        .view-btn, .view-btn:link, .view-btn:visited { display: inline-block !important; padding: 6px 14px !important; background-color: #2ea44f !important; color: white !important; border-radius: 6px !important; text-decoration: none !important; font-size: 13px !important; font-weight: 600 !important; border: none !important; }

        /* 🚀 精制圆火箭 */
        .scroll-to-top {
            position: fixed !important; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important; width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important; border-radius: 50% !important;
            z-index: 999999 !important; display: flex !important; align-items: center !important; justify-content: center !important;
            text-decoration: none !important; box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        }

        /* 🛡️ 核心修复逻辑：针对闪烁消失的解决办法 */
        
        /* 1. 隐藏右上角菜单，但绝不使用 display:none */
        [data-testid="stHeader"] [data-testid="stToolbar"] {
            opacity: 0 !important;
            pointer-events: none !important;
        }

        /* 2. 让整个 Header 变成透明的，但位置留着 */
        [data-testid="stHeader"] {
            background: transparent !important;
            color: transparent !important;
        }

        /* 3. 强制把侧边栏开关按钮（那个 >>）变色，并拉到屏幕中间 */
        [data-testid="stHeader"] button:first-child, 
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0 !important;
            transform: translateY(-50%) !important;
            width: 50px !important;
            height: 80px !important;
            background-color: rgba(255,255,255,0.2) !important; /* 淡淡的白色拉环 */
            border-radius: 0 40px 40px 0 !important;
            z-index: 1000000 !important;
            visibility: visible !important;
            display: flex !important;
            opacity: 1 !important;
            color: white !important; /* 强制按钮内的图标变白 */
        }
        
        /* 确保按钮里面的图标不会跟着变透明 */
        [data-testid="stHeader"] button:first-child svg,
        [data-testid="stSidebarCollapsedControl"] svg {
            fill: white !important;
            width: 30px !important;
            height: 30px !important;
        }

        /* 隐藏页脚 */
        footer { display: none !important; }

        /* 内容吸附 */
        .block-container { padding-top: 2.5rem !important; }
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main { padding-left: 0 !important; margin-left: 0 !important; }
        </style>
    """, unsafe_allow_html=True)
