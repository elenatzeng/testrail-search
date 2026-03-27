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
        
        # 抓取目錄並分頁處理
        all_sects = []
        offset = 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        
        path_map = {s['id']: s['name'] for s in all_sects}
        
        # 抓取案例並分頁處理 (改為 500 筆上限)
        all_cases, offset = [], 0
        while len(all_cases) < 500:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases'] if isinstance(resp, dict) else resp
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
        
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    if not text: return []
    t_lower = text.lower().strip()
    
    # 🌟 徹底保底：搜尋清單初始就包含搜尋詞自己
    res = {t_lower}
    if dictionary:
        for group in dictionary:
            g_lower = [str(w).lower() for w in group]
            if t_lower in g_lower: 
                res.update(g_lower)
                break
    return list(res)
