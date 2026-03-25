import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    # 移除圖片網址
    text = re.sub(r'!\[\]\(index\.php\?/attachments/get/\d+\)', '', text)
    
    def process(t):
        # 轉換換行標籤為 Python 換行，不增加額外邏輯
        t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
        t = t.replace('&nbsp;', ' ')
        return re.sub(r'<.*?>', '', t).strip()

    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = process(item.get('content', ''))
                    item['expected'] = process(item.get('expected', ''))
                return parsed_data 
        except: pass
    return process(text)

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: res.update(g_lower)
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        sections = api.sections.get_sections(project_id=pid, suite_id=sid)['sections']
        sect_dict = {s['id']: s for s in sections}
        def get_path(s_id):
            curr = sect_dict.get(s_id)
            if not curr: return ""
            p_id = curr.get('parent_id')
            return f"{get_path(p_id)} > {curr.get('name', '')}" if p_id else curr.get('name', '')
        path_map = {s_id: get_path(s_id).strip(' > ') for s_id in sect_dict}
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name')
    except Exception as e: return None, None, str(e), None
