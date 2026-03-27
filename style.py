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

        /* 🚀 主标题缩放 (精致化 32px) */
        h1 {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: white !important;
            padding-top: 10px !important;
            padding-bottom: 5px !important;
        }

        /* 🚀 作者标签：2px 扎实边框 */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important; 
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; 
            color: white !important; 
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }

        /* 🚀 核心黑盒子：内文 14px */
        .content-box { 
            background: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            border-radius: 12px; 
            padding: 15px 20px; 
            color: #c9d1d9 !important; 
            font-size: 14px !important; 
            font-weight: 400 !important; 
            line-height: 1.6; 
        }

        /* 🚀 Open Case 按钮：绿色无底线 */
        .view-btn, .view-btn:link, .view-btn:visited { 
            display: inline-block !important; 
            padding: 6px 14px !important; 
            background-color: #2ea44f !important; 
            color: white !important; 
            border-radius: 6px !important; 
            text-decoration: none !important; 
            font-size: 13px !important; 
            font-weight: 600 !important; 
            border: none !important; 
        }

        /* 🚀 【精制圆火箭】固定在右侧中间 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important;
            height: 42px !important;
            background-color: #f77f00 !important; 
            color: white !important; 
            border-radius: 50% !important;
            z-index: 10000000 !important;
            display: flex !important; 
            align-items: center !important; 
            justify-content: center !important;
            text-decoration: none !important; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
            transition: all 0.3s ease;
            cursor: pointer !important;
        }
        .scroll-to-top:hover { 
            background-color: #ff9f43 !important; 
            transform: translateY(-50%) scale(1.1) !important;
        }

        /* 🚀 【左侧侧边栏按钮微调】保持与火箭对称 */
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 50% !important;
            left: 0px !important;
            transform: translateY(-50%) !important;
            width: 40px !important;
            height: 65px !important;
            background-color: rgba(255,255,255,0.1) !important; 
            border-radius: 0 35px 35px 0 !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            z-index: 10000001 !important;
        }
        [data-testid="stSidebarCollapsedControl"] svg { fill: white !important; color: white !important; width: 25px !important; height: 25px !important; }

        /* 🛡️ 【彻底隐藏杂物：精准爆破右上角菜单】 */
        /* 隐藏右侧工具栏（包含三条杠、设置、Dark Mode 切换） */
        [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }
        
        /* 隐藏旧版菜单 ID 与 页脚 */
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }

        /* 确保 Header 本身不遮挡点击，但保留左侧按钮可见 */
        [data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* 强制让左侧收合按钮 (>> 或 <<) 重新显示并置顶 */
        [data-testid="stHeader"] button:first-child,
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            z-index: 10000002 !important;
        }

        /* 移除顶部多余的白边 padding，让标题更靠上 */
        .block-container { padding-top: 2.5rem !important; }
        
        /* 内容收合时吸附左侧，最大化阅读空间 */
        [data-testid="stAppViewContainer"][data-collapsed="true"] .main { 
            padding-left: 0 !important; 
            margin-left: 0 !important; 
        }
        </style>
    """, unsafe_allow_html=True)
