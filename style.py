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

        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }

        /* 🚀 (核心修正) 黑盒子帶綠線版 */
        .step-container {
            margin-bottom: 25px !important;
            padding-left: 5px !important;
        }

        .black-box-with-line { 
            background-color: #1c2128 !important; 
            border: 1px solid #30363d !important; 
            /* 🔥 綠線直接長在盒子左邊 */
            border-left: 5px solid #4CAF50 !important; 
            border-radius: 8px !important; 
            padding: 18px 22px !important; 
            color: #c9d1d9 !important; 
            font-size: 14px !important; 
            line-height: 1.8 !important;
            margin-bottom: 15px !important;
            white-space: pre-wrap !important;
        }

        .step-label {
            color: white !important;
            font-weight: bold !important;
            margin-bottom: 8px !important;
            display: block !important;
        }

        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 25px; font-style: italic; }

        /* 🚀 火箭按鈕 */
        .scroll-to-top {
            position: fixed; top: 50% !important; right: 15px !important;
            transform: translateY(-50%) !important; width: 42px !important; height: 42px !important;
            background-color: #f77f00 !important; color: white !important; border-radius: 50% !important;
            display: flex !important; align-items: center; justify-content: center;
            font-size: 20px !important; text-decoration: none !important; z-index: 99999 !important;
        }
        .scroll-to-top::after {
            content: "回到最頂"; position: absolute; right: 55px; top: 50%; transform: translateY(-50%);
            background-color: rgba(0,0,0,0.8); color: white; padding: 5px 10px; border-radius: 6px;
            font-size: 12px; opacity: 0; transition: opacity 0.3s; pointer-events: none; border: 1px solid #f77f00;
        }
        .scroll-to-top:hover::after { opacity: 1; }
        </style>
    """, unsafe_allow_html=True)
