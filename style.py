import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 全域永夜背景鎖死：確保背景深色，不論系統設定為何 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0d1117 !important;
        }
        
        /* 2. 隱藏選單與工具列：防止手動切換到 Light Mode 破壞美感 */
        header, #MainMenu, footer, [data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        /* 3. 恢復漂亮的黑盒子與靈魂綠線結構 */
        .step-container {
            border-left: 4px solid #4CAF50;
            padding-left: 20px;
            margin-left: 5px;
            margin-bottom: 30px;
            display: block;
        }
        
        .content-box {
            background: #1c2128;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 18px 20px;
            color: #c9d1d9;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
        }

        /* 4. Expander 標題區美化：與深色主題融為一體 */
        .streamlit-expanderHeader {
            background-color: #161b22 !important;
            border-radius: 8px !important;
            border: 1px solid #30363d !important;
            color: #c9d1d9 !important;
        }
        
        /* 5. 全域文字顏色修正：確保在深色背景下清晰可見 */
        h1, h2, h3, p, span, label {
            color: #adb5bd !important;
        }
        
        /* 6. 按鈕與輸入框深色美化 */
        .stTextInput>div>div>input, .stButton>button {
            background-color: #21262d !important;
            color: #c9d1d9 !important;
            border: 1px solid #30363d !important;
            border-radius: 6px !important;
        }
        
        /* 7. 徹底消滅圖片殘渣：確保不出現小破圖圖示 */
        img { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
