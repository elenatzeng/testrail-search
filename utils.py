import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def clean_html(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        sect_resp = api.sections.get_sections(project_id=pid)
        sects_list = sect_resp.get('sections', []) if isinstance(sect_resp, dict) else sect_resp
        path_map = {s['id']: s['name'] for s in sects_list}
        
        # 🛡️ 限制改為 250，避免 400 Bad Request
        case_resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250)
        cases_list = case_resp.get('cases', []) if isinstance(case_resp, dict) else case_resp
        
        return cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    if not text: return []
    t_lower = text.lower().strip()
    # 🌟 核心：初始集合包含原文，確保字典沒對到時也能搜原文
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
