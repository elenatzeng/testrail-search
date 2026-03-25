import streamlit as st
from style import apply_custom_style
from utils import clean_html, fetch_data_from_tr, multi_lang_search
from users import USER_CONFIG, DEFAULT_CONFIG
from keywords import SEARCH_DICTIONARY

st.set_page_config(page_title="TestRail AI Search", layout="wide", page_icon="🧪")
apply_custom_style()

st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    
    text = str(raw_html)
    
    # 🚀 1. 處理 TestRail 分離步驟 (Separated Steps)
    if (text.startswith('[') and 'content' in text) or (text.startswith('[') and 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                combined_steps = []
                for i, item in enumerate(parsed_data, 1):
                    c = item.get('content', '').strip()
                    e = item.get('expected', '').strip()
                    # 清理標籤
                    c = re.sub(r'<.*?>', '', c).replace('&nbsp;', ' ')
                    e = re.sub(r'<.*?>', '', e).replace('&nbsp;', ' ')
                    
                    # 修正編號疊加：如果內容開頭已經有 1. 2. 就不再加大編號
                    has_manual_num = re.match(r'^\d+[\.\、\:\s]', c)
                    step_prefix = "" if has_manual_num else f"{i}. "
                    
                    step_str = f"{step_prefix}{c}"
                    if e:
                        step_str += f"\n   <span class='expected-text'>👉 [預期]: {e}</span>"
                    combined_steps.append(step_str)
                return "\n\n".join(combined_steps)
        except:
            pass

    # 🚀 2. 處理普通格式
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^\d+[\.\、\:\s]', line):
            final_output.append(line)
        else:
            final_output.append(f"{i}. {line}")
    return "\n".join(final_output)

def multi_lang_search(text, dictionary):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in dictionary:
        group_lower = [str(word).lower() for word in group]
        if text_lower in group_lower:
            related_words.update(group_lower)
    return list(related_words)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        sections_data = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in sections_data['sections']}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            parent_id = curr.get('parent_id')
            return f"{get_path(parent_id)} > {curr['name']}" if parent_id else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        all_cases_list, offset = [], 0
        while True:
            response = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = response['cases']
            if not cases: break
            all_cases_list.extend(cases)
            if len(cases) < 250: break
            offset += 250
        return all_cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name')
    except Exception as e:
        return None, None, str(e), None
def get_val(key, default=""):
    return st.query_params.get(key, st.session_state.get(f"store_{key}", default))

with st.sidebar:
    st.header("🔐 連線設定")
    tr_url = st.text_input("TestRail URL", value=get_val("url"))
    tr_user = st.text_input("帳號 Email", value=get_val("user"))
    tr_pw = st.text_input("API Key", type="password", value=get_val("pw"))
    project_id = st.number_input("Project ID", value=int(get_val("pid", "10")))
    suite_id = st.number_input("Suite ID", value=int(get_val("sid", "10")))

    if st.button("💾 儲存資訊至網址", use_container_width=True):
        st.query_params.update(url=tr_url, user=tr_user, pw=tr_pw, pid=project_id, sid=suite_id)
        st.success("✅ 已儲存")
    if st.button("🔄 強制刷新數據", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.title("🧪 TestRail 智能檢索中心")

if tr_url and tr_user and tr_pw:
    all_cases, path_map, sync_time, p_name = fetch_data_from_tr(tr_url, tr_user, tr_pw, project_id, suite_id)
    
    if all_cases is not None:
        st.markdown(f'<div style="color:#8b949e; font-size:14px;">📍 Project：{p_name} | Suite：#{suite_id}</div>', unsafe_allow_html=True)
        
        col_search, col_clear, col_run = st.columns([6, 1.2, 1.2])
        if "q_text" not in st.session_state: st.session_state.q_text = ""

        with col_search:
            st.markdown('<div style="font-size:13px; color:#8b949e; margin-bottom:5px;">● 搜尋內容:</div>', unsafe_allow_html=True)
            q_input = st.text_input("", value=st.session_state.q_text, placeholder="輸入關鍵字...", label_visibility="collapsed")
            st.session_state.q_text = q_input

        with col_clear:
            if st.button("🗑️ 清除條件", use_container_width=True):
                st.session_state.q_text = "" 
                st.rerun()

        with col_run:
            if st.button("🔎 重新查詢", use_container_width=True): st.rerun()

        final_query = st.session_state.q_text
        if final_query:
            st.caption(f"⚡ 最後同步：{sync_time} (共 {len(all_cases)} 筆案例)")
            raw_input_terms = [t.lower() for t in final_query.strip().split() if len(t) > 0]
            scored_results = []

            for c in all_cases:
                cid = str(c.get('id', '')).strip()
                title = str(c.get('title', '')).lower()
                section_path = str(path_map.get(c.get('section_id', ""), "")).lower()
                
                raw_c_body = str(c.get('custom_steps', '')) + str(c.get('custom_steps_separated', ''))
                clean_c_body = clean_html(raw_c_body).lower()
                
                searchable_pool = title + section_path + clean_c_body
                
                is_all_match = True
                total_score = 0
                for term in raw_input_terms:
                    expanded = multi_lang_search(term, SEARCH_DICTIONARY)
                    text_hit = any(word in searchable_pool for word in expanded)
                    id_hit = any(word == cid for word in expanded)
                    
                    # 🚀 括號與邏輯已經完全修正
                    if not (text_hit or id_hit):
                        is_all_match = False
                        break
                    else:
                        if any(word in title for word in expanded): total_score += 1000
                
                if is_all_match:
                    u_info = USER_CONFIG.get(c.get('created_by'), DEFAULT_CONFIG)
                    total_score += u_info.get("weight", 0)
                    
                    if not clean_c_body.strip() or len(clean_c_body) < 10: 
                        total_score -= 500000 
                        
                    scored_results.append((total_score, c, u_info))

            scored_results.sort(key=lambda x: x[0], reverse=True)
            st.markdown(f"### 🎯 找到 {len(scored_results)} 個案例")

            for _, item, u_info in scored_results:
                cid = str(item.get('id'))
                status_emoji = "🟢" if u_info.get("is_active") else "🔴"
                author_style = "color: #4CAF50; background: rgba(76,175,80,0.15); border: 1.5px solid #4CAF50;" if u_info.get("is_active") else "color: #ff4b4b; background: rgba(255,75,75,0.15); border: 1.5px solid #ff4b4b;"
                
                st.markdown(f'<div class="case-path-text">{path_map.get(item.get("section_id"), "Unknown")}</div>', unsafe_allow_html=True)
                c_title, c_btn = st.columns([7, 1.5])
                with c_title:
                    st.markdown(f'<div style="font-size:16px; font-weight:bold;">{item.get("title")} <small>(#{cid})</small> <span class="author-tag" style="{author_style}">{status_emoji} {u_info["name"]}</span></div>', unsafe_allow_html=True)
                with c_btn:
                    st.markdown(f'<div style="text-align:right;"><a href="{tr_url.strip("/")}/index.php?/cases/view/{cid}" target="_blank" class="view-btn">📖 Open Case</a></div>', unsafe_allow_html=True)
                with st.expander("🔽 查看測試步驟"):
                    body = clean_html(item.get('custom_steps') or item.get('custom_steps_separated'))
                    st.markdown(f'<div class="step-content-box">{body if body else "（無詳細步驟）"}</div>', unsafe_allow_html=True)
                st.markdown("---")

    st.markdown("""<a href="#top-anchor" class="scroll-to-top" title="回到頂部">▲</a>""", unsafe_allow_html=True)
else:
    st.info("👈 請在左側輸入資料後開始查詢。")
