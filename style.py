import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 修正紅框處：讓展開器跟上方標題拉開距離，不再黏住名字標籤 */
        .stExpander {
            margin-top: 18px !important; 
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
        }

        /* 🚀 名字標籤 (25px 弧形 + 距離拉開) */
        .author-tag { 
            font-size: 13px !important; 
            border-radius: 25px !important; 
            padding: 2px 15px !important; 
            display: inline-flex !important;
            align-items: center; 
            margin-left: 18px !important; 
            font-weight: 800 !important; 
            border: 2px solid !important; 
            background: rgba(0,0,0,0.3) !important;
        }
        
        /* 🚀 路徑樣式 (圓圈 6) */
        .case-path-box {
            font-size: 15px !important;
            font-weight: 700 !important;
            color: #e6edf3 !important;
            margin-bottom: 8px;
            margin-top: 32px;
            letter-spacing: 0.5px;
        }

        /* 步驟方塊內容 */
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; 
            padding: 18px; border-radius: 10px; border: 1px solid #30363d; 
            margin-top: 8px; font-size: 15px; line-height: 1.7;
            white-space: pre-wrap !important;
        }

        .step-container { border-left: 4px solid #2ea44f; padding-left: 20px; margin-bottom: 25px; }

        .view-btn { 
            display: inline-block; padding: 7px 18px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; font-size: 14px; font-weight: bold; 
        }

        .scroll-to-top {
            position: fixed; bottom: 85px; right: 35px; width: 50px; height: 50px;
            background-color: #f77f00; color: white !important; border-radius: 50%;
            z-index: 9999; display: flex; align-items: center; justify-content: center; font-size: 22px;
        }
        </style>
    """, unsafe_allow_html=True)
