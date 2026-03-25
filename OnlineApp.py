import streamlit as st
import re
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()
st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)

def get_val(key): return st.query_params.get(key, st.session_state.get(f"store_{key}", ""))

# 側邊欄與搜尋設定 (略，保持不變)
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
        st.markdown(f"📍 Project：{p_name} | Suite：#{sid}")
        q_input = st.text_input("搜尋內容", value=st.session_state.get("q_text", ""))
        st.session_state.q_text = q_input

        if st.session_state.q_text:
            terms = [t.lower() for t in st.session_state.q_text.strip().split() if t]
            results = []
            img_pattern = r'!\[\]\(index\.php\?/attachments/get/\d+\)'

            for c in all_cases:
                title = str(c.get('title', ''))
                cid = str(c.get('id'))
                is_match = any(all(multi_lang_search(t, SEARCH_DICTIONARY)[0] in title.lower() for t in terms) for _ in [0])
                if is_match:
                    u = USER_CONFIG.get(int(c.get('created_by', 0)), DEFAULT_CONFIG)
                    results.append((c, u))

            for item, u in results:
                cid = str(item.get('id'))
                st.markdown(f"📁 {path_map.get(item.get('section_id'), '')}")
                
                # 標題與按鈕
                c1, c2 = st.columns([8, 2])
                status_emoji = "🟢" if u.get("is_active") else "🔴"
                c1.markdown(f"### {item.get('title')} (#{cid}) <span class='author-tag'> {status_emoji} {u['name']}</span>", unsafe_allow_html=True)
                c2.write(f"[📖 Open Case]({tr_url.strip('/')}/index.php?/cases/view/{cid})")

                with st.expander("查閱測試步驟"):
                    steps = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    
                    def to_html_logic(text):
                        if not text: return ""
                        text = re.sub(img_pattern, '', text).strip()
                        # 把換行轉成真正的 HTML 標籤
                        lines = text.split('\n')
                        res = []
                        for line in lines:
                            if line.strip().startswith(('*', '-', '•')):
                                res.append(f"<li>{line.strip()[1:].strip()}</li>")
                            else:
                                res.append(f"<div>{line}</div>")
                        final = "".join(res)
                        if "<li>" in final: final = f"<ul>{final}</ul>"
                        return final

                    if isinstance(steps, list):
                        v_idx = 1
                        for s in steps:
                            c_html = to_html_logic(s.get('content', ''))
                            e_html = to_html_logic(s.get('expected', ''))
                            if not c_html and not e_html: continue
                            
                            # 🔥 核心修正：直接注入一整塊 HTML 結構
                            full_step_html = f"""
                            <div class="custom-step-container">
                                <div class="custom-label">Step {v_idx}:</div>
                                <div class="custom-box">{c_html}</div>
                                <div class="custom-label">Expected:</div>
                                <div class="custom-box">{e_html}</div>
                            </div>
                            """
                            st.markdown(full_step_html, unsafe_allow_html=True)
                            v_idx += 1
                    elif steps:
                        st.markdown(f'<div class="custom-step-container"><div class="custom-box">{to_html_logic(steps)}</div></div>', unsafe_allow_html=True)
                st.markdown("---")
