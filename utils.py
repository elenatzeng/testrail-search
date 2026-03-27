import re, time, streamlit as st, ast
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    if not text or not keyword: return False
    # 物理剥皮：只看純文字，不看 HTML 標籤屬性
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean) 
    clean = " ".join(clean.split()).lower()
    # \b 鎖死邊界
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', clean)

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    if len(t_lower) == 3 and t_lower.isalpha(): # 幣別鎖死
        return [t_lower]
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        all_sects = api.sections.get_sections(project_id=pid)
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        path_map = {}
        for s_id in id_to_name:
            parts, curr = [], s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
        all_cases = api.cases.get_cases(project_id=pid, suite_id=sid)
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except: return None, None, None, None
