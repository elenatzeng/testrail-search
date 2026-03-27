import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 */
        .stApp { background-color: #0b0e14 !important; }

        /* 🚀 作者標籤基礎樣式 (所有標籤共用) */
        .author-tag { 
            font-size: 12px !important; 
            border-radius: 20px !important; 
            padding: 2px 12px !important; 
            display: inline-flex !important; 
            align-items: center; 
            margin-left: 10px !important; 
            font-weight: 600 !important; 
            border: 2px solid !important; /* 👈 這是關鍵：先給出邊框線 */
            background: rgba(0,0,0,0.5) !important;
        }

        /* 🟢 在職設定 */
        .status-active { 
            color: #32CD32 !important; 
            border-color: #32CD32 !important; 
        }

        /* 🔴 離職設定 */
        .status-inactive { 
            color: #FF4B4B !important; 
            border-color: #FF4B4B !important; 
            background: rgba(255, 75, 75, 0.2) !important; 
        }

        /* 🚀 頂部固定與隱藏 */
        [data-testid="stHeader"] { background: transparent !important; }
        footer { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
