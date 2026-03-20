import streamlit as st
from style import apply_style
from utils import clean_html, fetch_tr_data
from keywords import SEARCH_DICTIONARY
from users import USER_CONFIG

apply_style() # 呼叫亮起來的樣式

with st.sidebar:
    st.header("🔐 連線設定")
    # ... 放置妳的 text_input 邏輯 ...

st.title("🧪 TestRail 智能檢索中心")
# ... 搜尋與結果顯示邏輯 ...
