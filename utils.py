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
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects}
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        
        # 🛡️ 修正：防止 string indices must be integers 錯誤
        cases_list = resp if isinstance(resp, list) else resp.get('cases', [])
        return cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
