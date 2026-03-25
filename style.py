import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 (8) 名字標籤基礎樣式 (胖胖感、膠囊圓角) */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 20px !important; 
            padding: 4px 14px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 15px !important; 
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.5) !important;
            vertical-align: middle;
        }

        /* 🟢 在職 (無發光純色版) */
        .status-active {
            color: #32CD32 !important;
            border-color: #32CD32 !important;
        }

        /* 🔴 離職 (無發光純色版) */
        .status-inactive {
            color: #FF4B4B !important;
            border-color: #FF4B4B !important;
        }
        
        /* 🚀 (9) 優化 Expander：還原單一連續灰色盒子感 */
        .stExpander {
            border: none !important;
            box-shadow: none !important;
            background-color: transparent !important;
            padding: 0 !important;
        }

        /* Expander 標題區塊 */
        .stExpander summary {
            border: 1px solid #30363d !important;
            background-color: #1c2128 !important; /* 灰色背景 */
            border-radius: 10px !important;
            padding: 10px 15px !important;
            color: #8b949e !important;
            font-size: 14px !important;
        }
        
        /* 當 Expander 展開時的標題區塊：維持連續性 */
        .stExpander[open] summary {
            border-bottom: none !important;
            border-radius: 10px 10px 0 0 !important;
            margin-bottom: 0 !important;
        }

        /* Expander 下方內容區塊：與標題無縫連接 */
        .stExpander[open] > div {
            border: 1px solid #30363d !important;
            border-top: none !important;
            background-color: #1c2128 !important; /* 灰色背景 */
            border-radius: 0 0 10px 10px !important;
            padding: 15px !important;
            margin-top: 0 !important;
        }

        /* 測試步驟內容盒子 (白字) */
        .step-content-box { 
            color: #c9d1d9 !important; 
            background: transparent; 
            padding: 0 !important;
            font-size: 15px; 
            line-height: 1.8;
            white-space: pre-wrap !important;
        }

        /* 🚀 步驟容器修復：綠線移到這裡，維持 Step 1/Step 2 的結構 */
        .step-container { 
            border-left: 4px solid #2ea44f; 
            padding-left: 18px; 
            margin-bottom: 25px; 
        }

        /* (10) 按鈕 */
        .view-btn { 
            display: inline-block; padding: 7px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; 
            font-size: 14px; font-weight: bold; 
        }

        /* 火箭按鈕 */
        .scroll-to-top {
            position: fixed; bottom: 85px; right: 25px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center;
            text-decoration: none !important; font-size: 26px; box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        }
        </style>
    """, unsafe_allow_html=True)
