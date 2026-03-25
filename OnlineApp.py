import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄 (1)-(3)
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid = st.number_input("Project ID", value=int(get_val("pid")) if get_val("pid") else 10)
    sid = st.number_input("Suite ID", value=int(get_val("sid")) if get_val("sid") else 10)
    if st.button("💾 儲存資訊", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
    if st.button("🔄 刷新", use_container_width=True): st.cache_data.clear(); st.rerun()

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.title("🧪 TestRail 智能檢索中心")
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # (5) 搜尋區
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        q_input = col_s.text_input("● 搜尋內容:", value=st.session_state.get("q_text", ""))
        st.session_state.q_text = q_input
        if col_c.button("🗑️ 清除", use_container_width=True): st.session_state.q_text = ""; st.rerun()
        if col_r.button("🔎 查詢", use_container_width=True): st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            
            for c in all_cases:
                title = str(c.get('title', ''))
                if not title: continue
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                
                is_match = True; score = 0
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    f_t = any(w in title.lower() for w in exp)
                    f_p = any(w in f_path.lower() for w in exp)
                    f_i = any(w == cid for w in exp)
                    if not (f_t or f_p or f_i):
                        is_match = False; break
                    if f_t: score += 10000 # 標題匹配權重最高
                
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((score + u.get("weight", 0), c, u))

            results.sort(key=lambda x: x[0], reverse=True) # 🚀 找回排序
            st.markdown(f"### 🎯 找到 {len(results)} 個案例")

            for _, item, u in results:
                cid = str(item.get('id'))
                status_class = "status-active" if u.get("is_active") else "status-inactive"
                status_emoji = "🟢" if u.get("is_active") else "🔴"
                
                # (6) 路徑
                st.markdown(f'<div style="font-size:14px; color:#adb5bd; margin-top:25px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_html = f'<span class="author-tag {status_class}">{status_emoji} {u["name"]}</span>'
                c1.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # 🚀 (9) 步驟渲染：過濾圖片附件語法
                with st.expander("查閱測試步驟", expanded=False):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    def is_image_only(text): # 🚀 檢查是否為純圖片附件語法
                        return bool(re.match(r'^!\[\]\(index\.php\?/attachments/get/\d+\)$', str(text).strip()))

                    if isinstance(steps, list):
                        for i, s in enumerate(steps, 1):
                            content = s.get('content', '').strip()
                            expected = s.get('expected', '').strip()
                            
                            # 🚀 如果 content 或 expected 是圖片，就不顯示該部分
                            if content or expected:
                                st.markdown('<div class="step-container">', unsafe_allow_html=True)
                                if content and not is_image_only(content):
                                    st.markdown(f'<div class="step-label">Step {i}:</div><div class="step-text">{content}</div>', unsafe_allow_html=True)
                                if expected and not is_image_only(expected):
                                    st.markdown(f'<div class="step-label">Expected:</div><div class="step-text">{expected}</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    elif steps and not is_image_only(steps):
                        st.markdown(f'<div class="step-container"><div class="step-text">{steps}</div></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="color:#666; font-size:14px; margin-left:15px;">(無文字內容或僅包含圖片附件)</div>', unsafe_allow_html=True)
                st.markdown("---")
