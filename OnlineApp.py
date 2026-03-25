import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

# 初始化
st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key): 
    return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 🚀 (1)-(3) 側邊欄設定
with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    pid_v = get_val("pid"); sid_v = get_val("sid")
    pid = st.number_input("Project ID", value=int(pid_v) if pid_v else 10)
    sid = st.number_input("Suite ID", value=int(sid_v) if sid_v else 10)
    
    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=pid, sid=sid)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear(); st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, pid, sid)
    
    if all_cases:
        st.markdown(f"📍 Project：<span style='color:white; font-weight:bold;'>{p_name}</span> | Suite：<span style='color:white; font-weight:bold;'>#{sid}</span>", unsafe_allow_html=True)
        
        # 搜尋區 (5, 11, 12)
        col_s, col_c, col_r = st.columns([6, 1.2, 1.2], vertical_alignment="bottom")
        if "q_text" not in st.session_state: st.session_state.q_text = ""
        with col_s:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="請輸入關鍵字...", label_visibility="collapsed")
            st.session_state.q_text = q_input
        with col_c:
            if st.button("🗑️ 清除條件", use_container_width=True): 
                st.session_state.q_text = ""; st.rerun()
        with col_r:
            if st.button("🔎 重新查詢", use_container_width=True): 
                st.rerun()

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_pattern = r'!\[\]\(index\.php\?/attachments/get/\d+\)'

            for c in all_cases:
                title = str(c.get('title', ''))
                cid = str(c.get('id'))
                f_path = path_map.get(c.get('section_id'), "")
                is_match = True
                for t in terms:
                    exp = multi_lang_search(t, SEARCH_DICTIONARY)
                    if not (any(w in (title.lower() + f_path.lower()) for w in exp) or any(w == cid for w in exp)):
                        is_match = False; break
                if is_match:
                    steps_raw = c.get('custom_steps') or c.get('custom_steps_separated')
                    clean_content = re.sub(img_pattern, '', str(steps_raw)).strip()
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    final_score = (10000 + u.get("weight", 0)) if len(clean_content) > 5 else -500000
                    results.append((final_score, c, u))

            results.sort(key=lambda x: x[0], reverse=True) 

            for _, item, u in results:
                cid = str(item.get('id'))
                st.markdown(f'<div style="font-size:14px; color:#adb5bd; margin-top:25px;">📁 {path_map.get(item.get("section_id"), "")}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns([8, 1.5], vertical_alignment="center")
                tag_html = f'<span class="author-tag status-{"active" if u.get("is_active") else "inactive"}">{"🟢" if u.get("is_active") else "🔴"} {u["name"]}</span>'
                c1.markdown(f'<div style="display:flex; align-items:center;"><span style="font-size:18px; font-weight:bold; color:white;">{item.get("title")} (#{cid})</span>{tag_html}</div>', unsafe_allow_html=True)
                c2.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                
                with st.expander("查閱測試步驟", expanded=False):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    # 🔥 核心修正：強制斷行處理器
                    def final_line_fix(text):
                        if not text: return ""
                        # 移除圖片代碼
                        text = re.sub(img_pattern, '', text).strip()
                        # 1. 處理已經存在的換行符號
                        text = text.replace('\n', '<br>')
                        # 2. 針對妳貼出的那種沒點點的「用户名驗證...」內容進行正則補強
                        # 如果文字中出現「用户名」，但在它前面不是換行，就幫它加換行
                        text = re.sub(r'(?<!<br>)(用户名)', r'<br>• \1', text)
                        return text

                    if isinstance(steps, list):
                        v_idx = 1
                        for s in steps:
                            c_html = final_line_fix(s.get('content', ''))
                            e_html = final_line_fix(s.get('expected', ''))
                            if not c_html and not e_html: continue
                            
                            # 🔥 使用 inline-style 確保綠線長出來並連貫
                            st.markdown(f'''
                                <div style="border-left: 4px solid #4CAF50 !important; padding-left: 20px; margin-left: 5px; margin-bottom: 25px;">
                                    <div style="color:white; font-weight:bold; margin-bottom:8px;">Step {v_idx}:</div>
                                    <div style="background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:15px 20px; color:#c9d1d9; font-size:14px; line-height:1.8; margin-bottom:15px;">{c_html}</div>
                                    <div style="color:white; font-weight:bold; margin-bottom:8px;">Expected:</div>
                                    <div style="background:#1c2128; border:1px solid #30363d; border-radius:12px; padding:15px 20px; color:#c9d1d9; font-size:14px; line-height:1.8;">{e_html}</div>
                                </div>
                            ''', unsafe_allow_html=True)
                            v_idx += 1
                st.markdown("---")

    st.markdown('<a href="#top-anchor" class="scroll-to-top">🚀</a>', unsafe_allow_html=True)
