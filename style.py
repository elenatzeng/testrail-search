import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* 🌌 靈魂星空背景 */
        .stApp, [data-testid="stSidebar"], [data-testid="stAppViewContainer"] {
            background-color: #0b0e14 !important;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 3px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 2px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 3px) !important;
            background-size: 550px 550px, 350px 350px, 250px 250px !important;
            background-position: 0 0, 40px 60px, 130px 270px !important;
        }

        /* 🎯 【精準絕殺貓咪】 */
        button[data-testid="stBaseButton-header"], 
        button[kind="header"],
        [data-testid="stToolbarActionButtonIcon"],
        .stDeployButton,
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* 🛡️ 【守護左側箭頭 > 】 */
        [data-testid="stSidebarCollapsedControl"] {
            visibility: visible !important;
            display: flex !important;
            pointer-events: auto !important;
            z-index: 999999 !important;
        }

        /* 🚀 【火箭座標修正】固定在「右側中間」 */
        .scroll-to-top {
            position: fixed !important;
            top: 50% !important;
            right: 15px !important;
            transform: translateY(-50%) !important;
            width: 45px !important;
            height: 45px !important;
            background
