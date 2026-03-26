import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 初始化與樣式套用
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key): 
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 🚀 (1) 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v = get_val("pid"); sid_v = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True): # (2)
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True): # (3)
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        # (4) 專案資訊
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # (5) (11) (12) 搜尋區
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容 (輸入關鍵字查詢；支援繁簡體與英文):</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="請輸入查詢關鍵字，若有多個請空格格開", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): # (11)
                st.session_state.q_text = ""; st.rerun()
        with col_r:
            if st.button("🔎 重新查詢", use_container_width=True): # (12)
                st.rerun()

        if st.session_state.q_text:
            st.caption(f"⚡ 最後同步：{sync_time}")
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_pattern = r'!\[\]\(index\.php\?/attachments/get/\d+\)'

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
                    if f_t: score += 10000 # 標題權重

                if is_match:
                    # 🚀 排序邏輯：檢查是否有實質文字內容
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated')
                    # 移除圖片語法後計算剩餘長度
                    clean_content = re.sub(img_pattern, '', str(steps_raw)).strip()
                    has_real_text = len(clean_content) > 5
                    
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    # 內容空空或只有圖片，扣除 50 萬分，確保排在最後
                    final_score = (score + u.get("weight", 0)) if has_real_text else (score - 500000)
                    results.append((final_score, c, u))

            results.sort(key=lambda x: x[0], reverse=True) 
            st.markdown(f"### 🎯 找到 {len(results)} 個案例")

            for _, item, u in results:
                cid = str(item.get('id'))
                status_class = "status-active" if u.get("is_active") else "status-inactive"
                status_emoji = "🟢" if u.get("is_active") else "🔴"
                
                # (6) 路徑
                st.markdown(f'<div style="font-size:14px; color:#adb5bd; margin-top:25px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_html = f'<span class="author-tag {status_class}">{status_emoji} {u["name"]}</span>'
                # (7)(8) 標題 (#ID)
                c1.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                # (10) Open Case
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                # (9) 查閱測試步驟 (高級黑盒子 + 靈魂綠線)
                with st.expander("查閱測試步驟", expanded=False):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    if isinstance(steps, list):
                        has_any_text = False
                        for i, s in enumerate(steps, 1):
                            content = re.sub(img_pattern, '', s.get('content', '')).strip()
                            expected = re.sub(img_pattern, '', s.get('expected', '')).strip()
                            
                            if content or expected:
                                has_any_text = True
                                st.markdown('<div class="step-wrapper">', unsafe_allow_html=True)
                                if content:
                                    st.markdown(f'<div class="step-label">Step {i}:</div><div class="step-box">{content}</div>', unsafe_allow_html=True)
                                if expected:
                                    st.markdown(f'<div class="step-label">Expected:</div><div class="step-box">{expected}</div>', unsafe_allow_html=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                        if not has_any_text:
                            st.markdown('<div class="no-content-hint">(無文字內容或僅包含圖片附件)</div>', unsafe_allow_html=True)
                    elif steps:
                        clean_steps = re.sub(img_pattern, '', steps).strip()
                        if clean_steps:
                            st.markdown(f'<div class="step-wrapper"><div class="step-box">{clean_steps}</div></div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="no-content-hint">(無文字內容或僅包含圖片附件)</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="no-content-hint">(無文字內容或僅包含圖片附件)</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
