import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 🚀 1. 核心修正：刪除 TestRail 圖片標記 (index.php?/attachments/get/...)
    # 包含 Markdown 格式 ![](...) 或 HTML 格式 <img ...>
    text = re.sub(r'!\[\]\(index\.php\?/attachments/get/\d+\)', '', text)
    text = re.sub(r'<img[^>]*index\.php\?/attachments/get/\d+[^>]*>', '', text)
    
    # 清除 HTML style (解決白背景問題)
    text = re.sub(r'style="[^"]*"', '', text, flags=re.IGNORECASE)
    
    # 🚀 2. 處理分離步驟 (Separated Steps)
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    for key in ['content', 'expected']:
                        val = str(item.get(key, ''))
                        # 分離步驟內也要濾掉圖片網址
                        val = re.sub(r'!\[\]\(index\.php\?/attachments/get/\d+\)', '', val)
                        val = val.replace('<br />', '\n').replace('<br>', '\n')
                        val = re.sub(r'<.*?>', '', val)
                        item[key] = val.replace('&nbsp;', ' ').strip()
                return parsed_data 
        except:
            pass

    # 🚀 3. 處理普通文字
    text = text.replace('&nbsp;', ' ').replace('<br />', '\n').replace('<br>', '\n')
    text = re.sub(r'<.*?>', '', text)
    return text.strip()

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
            if not curr: return "Unknown"
            p_id = curr.get('parent_id')
            return f"{get_path(p_id)} > {curr['name']}" if p_id else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name')
    except Exception as e:
        return None, None, str(e), None
