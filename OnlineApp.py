import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 页面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)
# 套用妳辛苦調好的 style.py (包含殺貓、火箭、大膠囊、綠按鈕)
apply_custom_style()

# ✨ 【停机坪】在最顶端放置锚点
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 侧边栏守护 (连线设定)
with st.sidebar:
    st.header("🔐 连线设定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("账号 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 储存资讯至网址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已储存")
    if st.button("🔄 强制刷新数据", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能检索中心")

# 3. 核心数据逻辑
if tr_url and tr_user and tr_pw:
    # 增加讀取動畫，讓同事知道有在跑
    with st.spinner("🚀 正在從 TestRail 同步數據..."):
        all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        # ✨ 显示 Project 资讯
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 搜寻列布局
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        if "q_text" not in st.session_state:
            st.session_state.q_text = ""
        if "search_key" not in st.session_state:
            st.session_state.search_key = 0

        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜寻内容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                "", 
                value=st.session_state.q_text, 
                placeholder="请输入关键字查詢 (例如: CNY 充值)", 
                label_visibility="collapsed",
                key=f"search_input_{st.session_state.search_key}"
            )
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除条件", use_container_width=True): 
                st.session_state.q_text = "" 
                st.session_state.search_key += 1 
                st.rerun() 
        with col_r:
            if st.button("🔎 查询", use_container_width=True): 
                st.rerun()

        if st.session_state.q_text:
            # 🎯 統一轉小寫處理輸入詞 (這段對搜尋 CNY 非常重要)
            terms = [t.lower().strip() for t in st.session_state.q_text.split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title_low = str(c.get('title', '')).lower()
                cid_str = str(c.get('id'))
                path_low = str(path_map.get(c.get('section_id'), "")).lower()
                
                match_score = 0
                is_match = True
                for t in terms:
                    # 取得聯想詞 (字典)
                    expanded = multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    # 暴力包含比對：標題、路徑或 ID 只要有中就過
                    term_hit = any(w.lower() in title_low or w.lower() in path_low or w.lower() == cid_str for w in expanded)
                    
                    if term_hit:
                        if any(w.lower() in title_low for w in expanded): match_score += 10
                        elif any(w.lower() in path_low for w in expanded): match_score += 1
                    else:
                        is_match = False; break
                
                if is_match:
                    user_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or ""
                    quality_weight = 10000 if len(str(steps_raw)) > 10 else 0
                    results.append((match_score + quality_weight, path_low, c, user_info))

            results.sort(key=lambda x: (-x[0], x[1]))

            if not results:
                st.markdown('<div style="color:#8b949e; margin-top:20px; padding-left:5px;">🚫 找不到符合的测试案例。</div>', unsafe_allow_html=True)
            else:
                for _, _, item, u in results:
                    curr_cid = str(item.get('id'))
                    disp_path = path_map.get(item.get('section_id'), "")
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {disp_path}</div>', unsafe_allow_html=True)
                    
                    # 膠囊標籤 ( Elena 綠框 / 離職同事 紅框 )
                    tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{curr_cid})</span>{tag}</div>', unsafe_allow_html=True)
                    
                    # Open Case 綠色按鈕
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{curr_cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    
                    with st.expander("查阅测试步骤", expanded=False):
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        
                        def final_render(text):
                            if not text: return "(无内容)"
                            # 清除圖片標記與整理格式
                            text = clean_html(text)
                            text = re.sub(img_kill_pattern, '', str(text), flags=re.IGNORECASE).strip()
                            lines = text.splitlines()
                            html_out = '<div class="inner-text" style="font-weight: 400;">' 
                            for line in lines:
                                s = line.strip()
                                if not s: continue
                                is_list = re.match(r'^([•\-\*]|\d+\.)', s)
                                style = "margin-bottom:4px; display:block; font-size:14px;"
                                if is_list: style += "padding-left:18px;"
                                html_out += f'<div style="{style}">{s}</div>'
                            html_out += '</div>'
                            return html_out

                        if isinstance(steps_data, list) and len(steps_data) > 0:
                            for s_idx, s in enumerate(steps_data, 1):
                                c_html = final_render(s.get('content', ''))
                                e_html = final_render(s.get('expected', ''))
                                st.markdown(f'''
                                    <div style="border-left:4px solid #2ea44f; padding-left:20px; margin-left:5px; margin-bottom:30px; display:block;">
                                        <div style="color:#8b949e; font-weight:500; margin-bottom:10px; font-size:13px;">Step {s_idx}:</div>
                                        <div class="content-box">{c_html}</div>
                                        <div style="color:#8b949e; font-weight:500; margin-top:20px; margin-bottom:10px; font-size:13px;">Expected:</div>
                                        <div class="content-box">{e_html}</div>
                                    </div>
                                ''', unsafe_allow_html=True)
                        else:
                            # 處理非分步格式的 Case
                            st.markdown(f'<div class="content-box">{final_render(steps_data)}</div>', unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">请输入关键字开始检索...</div>', unsafe_allow_html=True)
    else:
        # 當抓不到資料時的提示
        st.error("❌ 無法取得數據。請確認左側 Project ID 與 API 設定是否正確，或嘗試點擊「強制刷新」。")
else:
    st.info("👈 請先在左側完成連線設定，搜尋框才會出現喔！")

# ✨ 【右中火箭】
st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到顶端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
