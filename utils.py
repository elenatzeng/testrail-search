import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    # 清理 HTML
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 強制在數字前換行
    text = re.sub(r'(\d+[\.\、])', r'\n\1', text)
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # 確保每一行都有正確的編號
    final_output = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^\d+[\.\、]', line):
            # 如果已有編號，去除舊的重新排號 (避免 1. 1. 重複)
            clean_line = re.sub(r'^\d+[\.\、]\s*', '', line)
            final_output.append(f"{i}. {clean_line}")
        else:
            final_output.append(f"{i}. {line}")
    return "\n".join(final_output)

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
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
            
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
        return None, None, None, str(e)
