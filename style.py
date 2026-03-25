import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* (這裡保留妳原本 style.py 裡其他的 CSS 樣式，如 stApp, author-tag, expander, step-box, green-line 等) */
        
        /* ... 其他樣式 ... */

        /* 🚀 (修正) 火箭回到頂部按鈕 - 妹妹專屬精緻瘦身版 */
        .scroll-to-top {
            position: fixed;
            bottom: 30px; /* 往下移，離邊緣更近 */
            right: 20px;  /* 往右移，離邊緣更近 */
            width: 45px;  /* 大瘦身：寬度從原本的巨大尺寸縮小到 45px */
            height: 45px; /* 大瘦身：高度從原本的巨大尺寸縮小到 45px */
            background-color: #f77f00; /* 亮橘色不變 */
            color: white !important;
            border-radius: 50%; /* 依然是完美的圓圈 */
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px; /* 火箭圖示也跟著縮小，保持比例 */
            text-decoration: none !important;
            z-index: 9999; /* 確保它在最上層 */
            transition: all 0.3s ease; /* 飛行的平滑動畫 */
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.5); /* 溫和的發光，不刺眼 */
        }
        
        /* 懸停時的精緻飛行動畫 */
        .scroll-to-top:hover {
            transform: translateY(-8px); /* 輕輕飛，不飛太高 */
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8); /* 懸停時稍微加強發光 */
        }
        </style>
    """, unsafe_allow_html=True)
