import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 1. 頁面初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 2. 側邊欄與按鈕 (守護妳所有的功能)
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
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

# 3. 核心數據邏輯
if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 搜尋功能區
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.get("q_text", ""), placeholder="輸入關鍵字查詢...", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): 
                st.session_state.q_text = ""; st.rerun()
        with col_r:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_pattern = r'!\[\]\(index\.php\?/attachments/get/\d+\)'

            for c in all_cases:
                title, cid = str(c.get('title', '')), str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                is_match = True
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title.lower() + f_path.lower()) for w in exp) or any(w == cid for w in exp)):
                        is_match = False; break
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((100, c, u))

            for _, item, u in results:
                cid = str(item.get('id'))
                st.markdown(f'<div style="font-size:14px; color:#adb5bd; margin-top:25px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                c1.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("查閱測試步驟", expanded=False):
                    steps_data = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    # 🔥 終極像素還原器：每一行都強行佔領 100% 寬度，絕不妥協
                    def ultimate_pixel_fix(text):
                        if not text: return ""
                        text = re.sub(img_pattern, ' [🖼️ 圖片附件] ', str(text)).strip()
                        # 全面捕捉換行
                        lines = text.splitlines()
                        processed_html = ""
                        for l in lines:
                            s = l.strip()
                            if not s or re.fullmatch(r'[\.\-\*•1]+', s): continue
                            # 關鍵：display: block + width: 100% 強制斷行
                            processed_html += f'<div style="display:block; width:100%; clear:both; margin-bottom:10px; line-height:1.6;">{s}</div>'
                        return processed_html

                    if isinstance(steps_data, list) and len(steps_data) > 0:
                        for s_idx, s in enumerate(steps_data, 1):
                            c_html = ultimate_pixel_fix(s.get('content', ''))
                            e_html = ultimate_pixel_fix(s.get('expected', ''))
                            if not c_html and not e_html: continue
                            
                            # 🟢 靈魂綠線絕對鎖死：CSS 結構包圍
                            green_line_box = "border-left:4px solid #4CAF50; padding-left:20px; margin-left:5px; margin-bottom:25px; display:block; overflow:hidden;"
                            box_style = "background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:18px 20px; color:#c9d1d9; font-size:14px;"
                            
                            st.markdown(f'''
                                <div style="{green_line_box}">
                                    <div style="color:white; font-weight:bold; margin-bottom:10px; font-size:16px; width:100%;">Step {s_idx}:</div>
                                    <div style="{box_style}">{c_html if c_html else "(無內容)"}</div>
                                    <div style="color:white; font-weight:bold; margin-top:20px; margin-bottom:10px; font-size:16px; width:100%;">Expected:</div>
                                    <div style="{box_style}">{e_html if e_html else "(無內容)"}</div>
                                </div>
                            ''', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="no-content-hint">💡 (此案例無文字步驟內容)</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
