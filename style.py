import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14 !important; }
        
        /* 🚀 基礎標籤樣式 (胖胖、圓角、膠囊感) */
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

        /* 🟢 在職/True：綠燈綠字亮綠框 + 發光感 */
        .status-active {
            color: #32CD32 !important;
            border-color: #32CD32 !important;
            box-shadow: 0 0 12px rgba(50, 205, 50, 0.5) !important;
        }

        /* 🔴 離職/False：紅燈紅字亮紅框 + 發光感 */
        .status-inactive {
            color: #FF4B4B !important;
            border-color: #FF4B4B !important;
            box-shadow: 0 0 12px rgba(255, 75, 75, 0.5) !important;
        }
        
        /* 🚀 (9) 測試步驟 Expander 優化 */
        .stExpander { border: none !important; box-shadow: none !important; background: transparent !important; }
        .step-content-box { 
            color: #c9d1d9 !important; background: #1c2128; 
            padding: 16px 20px; border-radius: 10px; border: 1px solid #30363d; 
            margin-top: 8px; font-size: 15px; line-height: 1.8;
            white-space: pre-wrap !important;
        }
        .view-btn { 
            display: inline-block; padding: 7px 16px; background-color: #2ea44f; 
            color: white !important; border-radius: 6px; text-decoration: none; 
            font-size: 14px; font-weight: bold; 
        }
        </style>
    """, unsafe_allow_html=True)
