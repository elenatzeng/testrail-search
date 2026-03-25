import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 1. 全局背景與文字基礎 (GitHub Dark 風格) */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div { 
            background-color: #0b0e14 !important; 
        }
        h1, h2, h3, h4, h5, p, span, label, small, .stMarkdown { 
            color: #ffffff !important; 
        }

        /* 2. 側邊欄輸入框與按鈕美化 */
        .stTextInput input, .stNumberInput input {
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        div[data-testid="stSidebar"] .stButton button { 
            background-color: #31333f !important; 
            color: #ffffff !important; 
            border: 1px solid #444c56 !important;
            border-radius: 8px !important;
            width: 100% !important;
            transition: 0.2s;
        }
        div[data-testid="stSidebar"] .stButton button:hover {
            border-color: #8b949e !important;
            background-color: #444c56 !important;
        }

        /* 3. 📂 案例路徑字體 (淺灰色小字) */
        .case-path-text { 
            font-size: 13px; 
            color: #8b949e !important; 
            margin-bottom: 8px; 
            display: block;
            font-family: sans-serif;
        }

        /* 4. 🚦 作者標籤與紅綠燈號 */
        .author-tag { 
            font-size: 11px; 
            border-radius: 12px; 
            padding: 3px 12px; 
            display: inline-block; 
            margin-left: 10px; 
            font-weight: bold; 
            text-transform: uppercase;
        }
        
        /* 5. 📖 Open Case 按鈕 (綠色亮眼) */
        .view-btn { 
            display: inline-block; 
            padding: 6px 16px; 
            background-color: #2ea44f; 
            color: white !important; 
            border-radius: 6px; 
            text-decoration: none; 
            font-size: 13px; 
            font-weight: bold; 
            transition: 0.2s;
        }
        .view-btn:hover {
            background-color: #2c974b;
            box-shadow: 0 0 10px rgba(46,164,79,0.4);
        }

        /* 6. ✨ 測試步驟容器 (深色卡片感) */
        .step-content-box { 
            color: #c9d1d9 !important; 
            background: #161b22; 
            padding: 15px; 
            border-radius: 10px; 
            border: 1px solid #30363d; 
            margin-top: 5px; 
            white-space: pre-wrap; 
            font-size: 14px;
            line-height: 1.6;
        }
        .step-item { 
            border-left: 4px solid #2ea44f; 
            padding-left: 20px; 
            margin-bottom: 25px; 
        }

        /* 7. 🚀 回到頂端懸浮按鈕 (修正版：避開 Manage App 工具列) */
        .scroll-to-top {
            position: fixed;
            bottom: 75px; /* 💡 向上提至 75px，確保不會被 Manage app 擋住 */
            right: 25px;  
            width: 46px;
            height: 46px;
            background-color: #2ea44f;
            color: white !important;
            border-radius: 50%;
            text-align: center;
            line-height: 42px; /* 垂直居中微調 */
            font-size: 20px;
            cursor: pointer;
            z-index: 999999; /* 確保在最上層 */
            box-shadow: 0 4px 12px rgba(0,0,0,0.6);
            text-decoration: none !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid rgba(255,255,255,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .scroll-to-top:hover {
            transform: translateY(-5px);
            background-color: #2c974b;
            box-shadow: 0 6px 20px rgba(46,164,79,0.5);
        }

        /* 8. 隱藏 Streamlit 頂部預設白色橫條 */
        header[data-testid="stHeader"] { background: transparent !important; }
        [data-testid="stTopBar"] { display: none !important; }

        /* 調整 Expander 樣式使更符合暗色主題 */
        .stExpander {
            border: 1px solid #30363d !important;
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
