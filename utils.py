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
        # 🛡️ 自動修復網址，確保結尾乾淨
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        
        # 🛡️ 檢查點 1：抓取專案
        p_info = api.projects.get_project(project_id=pid)
        if isinstance(p_info, str): raise ValueError(f"專案連線失敗: {p_info}")
        p_name = p_info.get('name', 'Project')

        # 🛡️ 檢查點 2：抓取目錄 (這裡就是妳紅字噴出的地方)
        all_sects = api.sections.get_sections(project_id=pid)
        if not isinstance(all_sects, list): raise ValueError(f"目錄抓取失敗: {all_sects}")
        path_map = {s['id']: s['name'] for s in all_sects}
        
        # 🛡️ 檢查點 3：抓取案例
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        if isinstance(resp, str): raise ValueError(f"案例抓取失敗: {resp}")
        
        cases_list = resp if isinstance(resp, list) else resp.get('cases', [])
        return cases_list, path_map, time.strftime("%H:%M:%S"), p_name

    except Exception as e:
        # 如果出錯，回傳具體的錯誤訊息，不要讓它噴紅字當機
        return None, None, f"連線異常: {str(e)}", None

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
