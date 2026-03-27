import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 整體背景與字體 */
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
        }
        
        /* 2. 標題與文字顏色 */
        h1, h2, h3, h4, h5, h6 {
            color: #f0f6fc !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        
        /* 3. 輸入框樣式 */
        .stTextInput > div > div > input {
            background-color: #161b22 !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        
        /* 4. 按鈕樣式 (查詢、重置等) */
        .stButton > button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
            transition: 0.2s;
            font-weight: 600;
        }
        .stButton > button:hover {
            background-color: #30363d !important;
            border-color: #8b949e !important;
        }
        
        /* 5. Open Case 按鈕 (藍色連結感) */
        .view-btn {
            display: inline-block;
            padding: 5px 15px;
            background-color: #238636;
            color: white !important;
            text-decoration: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            transition: 0.2s;
        }
        .view-btn:hover {
            background-color: #2ea44f;
            box-shadow: 0 0 10px rgba(46, 164, 79, 0.4);
        }

        /* 6. 作者標籤 (Status Tags) */
        .author-tag {
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 12px;
            border: 1px solid transparent;
        }
        .status-active {
            color: #32CD32 !important;
            border-color: #32CD32 !important;
            background: rgba(50, 205, 50, 0.1);
        }
        .status-inactive {
            color: #FF4B4B !important;
            border-color: #FF4B4B !important;
            background: rgba(255, 75, 75, 0.1);
        }

        /* 7. 步驟內容框 (Content Box) */
        .content-box {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            margin-bottom: 10px;
            color: #c9d1d9;
            line-height: 1.6;
        }
        
        /* 8. 側邊欄樣式 */
        section[data-testid="stSidebar"] {
            background-color: #010409 !important;
            border-right: 1px solid #30363d;
        }

        /* 9. 🚀 小火箭回到頂端按鈕 */
        .scroll-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #21262d;
            border: 1px solid #30363d;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none !important;
            z-index: 999;
            transition: 0.3s;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        .scroll-to-top:hover {
            background: #30363d;
            transform: translateY(-5px);
            border-color: #8b949e;
        }

        /* 10. Expander 樣式修正 */
        .streamlit-expanderHeader {
            background-color: transparent !important;
            color: #8b949e !important;
            border-bottom: 1px solid #30363d !important;
        }
        </style>
    """, unsafe_allow_html=True)
