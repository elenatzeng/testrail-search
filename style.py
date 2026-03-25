import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤：膠囊形狀、純色邊框 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 🚀 (9) Expander 透明化 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .stExpander summary { color: #8b949e !important; padding: 10px 0 !important; }
        
        /* 🚀 核心修正：這是一個大容器，裝著所有 Step */
        .steps-group-container {
            position: relative;
            padding-left: 25px; /* 給左邊線條留空間 */
            margin-top: 15px;
            margin-left: 5px;
        }

        /* 🚀 霛魂連貫綠線：利用偽元素做出從頭到尾的一條長線 */
        .steps-group-container::before {
            content: "";
            position: absolute;
            left: 0;
            top: 5px;
            bottom: 5px;
            width: 4px;
            background-color: #4CAF50;
            border-radius: 2px;
            /* 💡 加入發光效果，讓它看起來更有質感 */
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.7);
            z-index: 1;
        }

        .step-label { 
            color: #ffffff; 
            font-weight: bold; 
            font-size: 16px; 
            margin-bottom: 8px; 
            margin-top: 10px;
        }

        /* 🚀 黑盒子：移除左邊邊框，讓它單純靠在那條連貫綠線旁邊 */
        .step-box { 
            background-color: #1c2128 !important; 
            border: 1px solid #30363d; 
            border-radius: 12px; 
            padding: 18px 22px; 
            color: #c9d1d9; 
            font-size: 15px; 
            line-height: 1.6;
            margin-bottom: 20px;
            white-space: pre-wrap;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
        }

        .no-content-hint { color: #666; font-size: 14px; margin-top: 10px; font-style: italic; }
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        .scroll-to-top { position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px; background-color: #f77f00; color: white !important; border-radius: 50%; z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 26px; }
        </style>
    """, unsafe_allow_html=True)
