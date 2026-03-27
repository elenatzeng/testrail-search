import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(
    page_title="TestRail AI Search", 
    layout="wide", 
    page_icon="🧪", 
    initial_sidebar_state="expanded"
)
apply_custom_style()

# ✨ 【停機坪】
st.markdown('<div id="top-anchor" style="position:absolute; top:0;"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄守護 (連線設定)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v, sid_v = get_val("pid"), get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        if "q_text" not in st.session_state:
            st.session_state.q_text = ""
        if "search_key" not in st.session_state:
            st.session_state.search_key = 0

        # 搜尋列佈局
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input(
                "", 
                value=st.session_state.q_text, 
                placeholder="輸入關鍵字 (例如: 充值 CNY)，多關鍵字以空格隔開", 
                label_visibility="collapsed",
                key=f"search_input_{st.session_state.search_key}"
            )
            st.session_state.q_text = q_input
            
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): 
                st.session_state.q_text = "" 
                st.session_state.search_key += 1 
                st.rerun() 
        with col_r:
            if st.button("🔎 查詢", use_container_width=True): 
                st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_kill_pattern = r'(!\[.*?\]\(.*?\))|(<img.*?>)'

            for c in all_cases:
                title, cid = str(c.get('title', '')).lower(), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "").lower()
                steps_raw = c.get('custom_steps') or c.get('custom_steps_separated') or []
                steps_str = str(steps_raw).lower()
                
                # --- 🧠 核心：搜尋計分與過濾 (AND 邏輯) ---
                match_count = 0
                temp_match_score = 0
                
                for t in terms:
                    # 💡 幣種保護：長度 <= 4 (CNY) 不進字典同義詞，避免抓到 THB
                    exp = [t] if len(t) <= 4 else multi_lang_search(t, SEARCH_DICTIONARY)
                    
                    t_m = any(w in title for w in exp) or (t == cid)
                    p_m = any(w in f_path for w in exp)
                    c_m = any(w in steps_str for w in exp)
                    
                    if t_m or p_m or c_m:
                        match_count += 1
                        if t_m: temp_match_score += 5000 # 標題命中給予極高基礎分
                        elif p_m: temp_match_score += 100
                
                # 🛡️ 物理鎖死：只有當「所有關鍵字」都命中時，才計入結果
                if match_count == len(terms):
                    u_info = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    
                    # 💡 內容品質：計算「步驟數量」，每一步給予 2000 分加成
                    step_count = len(steps_raw) if isinstance(steps_raw, list) else 0
                    quality_bonus = step_count * 2000 

                    # 總分 = 搜尋分 + 品質分 + 人員權重
                    total_final_score = temp_match_score + quality_bonus + u_info.get("weight", 0)
                    
                    # 排序：(總分, 路徑字母)
                    results.append((total_final_score, f_path, c, u_info))

            # 執行排序 (大到小)
            results.sort(key=lambda x: (-x[0], x[1]))

            # --- ✨ 搜尋統計條 ---
            res_count = len(results)
            st.markdown(f'''
                <div style="background: rgba(46, 164, 79, 0.1); border-left: 5px solid #2ea44f; padding: 12px 20px; margin: 20px 0; border-radius: 4px;">
                    <span style="color: #adb5bd; font-size: 14px;">搜尋結果：</span>
                    <span style="color: #2ea44f; font-size: 18px; font-weight: bold;">{res_count}</span>
                    <span style="color: #adb5bd; font-size: 14px;"> 筆完全符合條件之測試案例</span>
                </div>
            ''', unsafe_allow_html=True)

            if res_count == 0:
                st.info(f"🚫 找不到同時符合這 {len(terms)} 個關鍵字的測試案例。")
            else:
                for _, path, item, u in results:
                    cid = str(item.get('id'))
                    is_active = u.get("is_active", True)
                    
                    # 🔴 樣式暴力鎖死：保證紅標顯示
                    color = "#32CD32" if is_active else "#FF4B4B"
                    bg = "rgba(50, 205, 50, 0.1)" if is_active else "rgba(255, 75, 75, 0.15)"
                    tag_html = f'''
                        <span style="color:{color} !important; border:1px solid {color} !important; background:{bg} !important; 
                        padding:2px 12px; border-radius:20px; font-size:12px; font-weight:bold; margin-left:10px; 
                        display:inline-flex; align-items:center;">
                        {'🟢' if is_active else '🔴'} {u["name"]}
                        </span>
                    '''
                    
                    st.markdown(f'<div style="font-size:13px; color:#adb5bd; margin-top:20px; margin-bottom:5px;">📁 {path}</div>', unsafe_allow_html=True)
                    
                    c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                    c1.markdown(f'<div style="display:flex; align-items:center; margin-bottom:15px;"><span style="font-size:20px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                    c2.markdown(f'''<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>''', unsafe_allow_html=True)
                    
                    with st.expander("查閱測試步驟", expanded=False):
                        steps_data = item.get('custom_steps') or item.get('custom_steps_separated')
                        def final_render(text):
                            if not text: return "(無內容)"
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
                    st.markdown("---")
        else:
            st.markdown('<div style="color:#DDDDDD; margin-top:50px; text-align:center; font-style: italic;">請輸入關鍵字開始檢索...</div>', unsafe_allow_html=True)
else:
    st.info("👈 請先在左側完成連線設定。")

st.markdown('<a href="#top-anchor" class="scroll-to-top" title="回到頂端"><span style="font-size: 24px;">🚀</span></a>', unsafe_allow_html=True)
