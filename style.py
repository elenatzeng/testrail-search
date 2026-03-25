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
        
        .author-tag { font-size: 13px !important; border-radius: 20px !important; padding: 4px 14px !important; display: inline-flex !important; align-items: center; margin-left: 15px !important; font-weight: 800 !important; border: 2px solid !important; background: rgba(0,0,0,0.5) !important; vertical-align: middle; }
        .status-active { color: #32CD32 !important; border-color: #32CD32 !important; }
        .status-inactive { color: #FF4B4B !important; border-color: #FF4B4B !important; }
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }

        /* 🚀 靈魂綠線容器 (恢復獨立結構) */
        .green-line-box {
            border-left: 4px solid #4CAF50 !important;
            padding-left: 20px !important;
            margin-left: 5px !important;
            margin-bottom: 30px !important;
            display: block !important;
        }

        /* 🚀 內容黑盒子 */
        .black-content-box {
            background-color: #1c2128 !important;
            border: 1px solid #30363d !important;
            border-radius: 12px !important;
            padding: 15px 20px !important;
            color: #c9d1d9 !important;
            font-size: 14px !important;
            line-height: 1.8 !important;
            margin-bottom: 15px !important;
            white-space: pre-wrap !important;
        }

        .step-label { color: white !important; font-weight: bold !important; margin-bottom: 8px !important; display: block !important; }
        .no-content-hint { color: #8b949e !important; font-size: 14px !important; padding: 10px 25px; font-style: italic; }

        /* 🚀 火箭回到頂部 */
        .scroll-to-top { position: fixed; top: 50% !important; right: 15px !important; transform: translateY(-50%) !important; width: 42px !important; height: 42px !important; background-color: #f77f00 !important; color: white !important; border-radius: 50% !important; display: flex !important; align-items: center; justify-content: center; font-size: 20px !important; text-decoration: none !important; z-index: 99999 !important; }
        .scroll-to-top::after { content: "回到最頂"; position: absolute; right: 55px; top: 50%; transform: translateY(-50%); background-color: rgba(0,0,0,0.8); color: white; padding: 5px 10px; border-radius: 6px; font-size: 12px; opacity: 0; transition: opacity 0.3s; pointer-events: none; border: 1px solid #f77f00; }
        .scroll-to-top:hover::after { opacity: 1; }
        
        .view-btn { display: inline-block; padding: 7px 16px; background-color: #2ea44f; color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
