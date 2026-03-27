import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def smart_format(text):
    """將 TestRail 的內容轉化為乾淨的文字"""
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    """最基礎的資料抓取邏輯"""
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        # 抓取 Section 路徑
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects}
        
        # 抓取 Cases
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        return resp['cases'], path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None
