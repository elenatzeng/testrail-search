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
        # 自動修正網址
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        
        # 1. 抓取專案
        p_info = api.projects.get_project(project_id=pid)
        p_name = p_info.get('name', 'Project')

        # 🛡️ 2. 抓取目錄 (修正點：處理分頁包裹)
        sect_resp = api.sections.get_sections(project_id=pid)
        # 如果回傳是包裹(dict)，就拿裡面的 'sections'；否則就當它是清單
        sects_list = sect_resp.get('sections', []) if isinstance(sect_resp, dict) else sect_resp
        
        if not isinstance(sects_list, list):
            raise ValueError("無法解析目錄列表格式")
            
        path_map = {s['id']: s['name'] for s in sects_list}
        
        # 🛡️ 3. 抓取案例 (同樣處理分頁包裹)
        case_resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        cases_list = case_resp.get('cases', []) if isinstance(case_resp, dict) else case_resp
        
        return cases_list, path_map, time.strftime("%H:%M:%S"), p_name

    except Exception as e:
        # 發生異常時回傳具體訊息
        return None, None, f"連連異常: {str(e)}", None

def multi_lang_search(text, dictionary):
    if not text: return []
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
