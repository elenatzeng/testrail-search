import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 - 找回來了！ */
        .stApp {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }
        
        /* 🚀 名字標籤 */
        .author-tag { 
            font-size: 13px !important; border-radius: 20px !important; 
            padding: 4px 14px !important; display: inline-flex !important;
            align-items: center; margin-left: 15px !important; 
            font-weight: 800 !important; border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important; vertical-align: middle;
        }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }

        /* 🚀 Expander 透明化 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }

        /* 🚀 無文字內容的提示文字 - 亮灰色顯現 */
        .no-content-hint { 
            color: #8b949e !important; 
            font-size: 14px !important; 
            padding: 10px 0 10px 25px !important; 
            font-style: italic !important;
            display: block !important;
        }

        /* 🚀 火箭回到頂部按鈕 - 縮小 + 固定在右邊中間 (無白線) */
        .scroll-to-top {
            position: fixed;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 42px !important;
            height: 42px !important;
            background-color: #f77f00 !important;
            color: white !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center;
            justify-content: center;
            font-size: 20px !important;
            text-decoration: none !important;
            z-index: 99999 !important;
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.5) !important;
            border: none !important;
            border-bottom: none !important;
        }
        .scroll-to-top:hover {
            transform: translateY(-50%) scale(1.1) !important;
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8) !important;
        }

        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
