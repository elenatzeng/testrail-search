import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* ... 你原本的其他樣式 ... */

        /* 🚀 活力橘回到頂端按鈕 */
        .scroll-to-top {
            position: fixed;
            bottom: 30px; /* 距離底部距離 */
            right: 30px;  /* 距離右側距離 */
            width: 50px;
            height: 50px;
            background-color: #f77f00 !important; /* 活力橘 */
            color: white !important;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none !important;
            font-size: 24px;
            font-weight: bold;
            z-index: 9999;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        }
        .scroll-to-top:hover {
            transform: translateY(-5px);
            background-color: #ff9500 !important;
            box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        }
        </style>
    """, unsafe_allow_html=True)
