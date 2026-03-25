import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* (這裡保留妳原本 style.py 裡其他的 CSS 樣式，如 stApp, author-tag, expander, step-box, green-line 等) */
        
        /* ... 其他樣式 ... */

        /* 🚀 (修正) 火箭回到頂部按鈕 - 妹妹專屬精緻瘦身版 + 固定居右中 */
        .scroll-to-top {
            position: fixed;
            top: 50%; /* 🔥 固定在畫面的垂直中間 */
            right: 15px; /* 🔥 固定在最右邊，離邊緣 15px */
            transform: translateY(-50%); /* 🔥 完美置中補正 */
            width: 45px; /* 大瘦身：精緻小巧 */
            height: 45px; /* 大瘦身：精緻小巧 */
            background-color: #f77f00; /* 亮橘色不變 */
            color: white !important;
            border-radius: 50%; /* 完美的圓圈 */
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px; /* 火箭圖示縮小，保持比例 */
            text-decoration: none !important;
            z-index: 9999; /* 確保它在最上層 */
            transition: all 0.3s ease; /* 飛行的平滑動畫 */
            box-shadow: 0 0 10px rgba(247, 127, 0, 0.5); /* 溫和的發光 */
            
            /* 🔥 移除底部的白線：確保 border-bottom 為 none */
            border: none !important;
            border-bottom: none !important;
        }
        
        /* 懸停時的精緻飛行動畫 (改為向左飛，因為在右邊) */
        .scroll-to-top:hover {
            transform: translate(-5px, -50%); /* 輕輕向左飛，不影響置中 */
            box-shadow: 0 0 20px rgba(247, 127, 0, 0.8); /* 懸停時稍微加強發光 */
        }
        </style>
    """, unsafe_allow_html=True)
