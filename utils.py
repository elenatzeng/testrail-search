import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

# 💡 核心修正：實裝妳要求的 match_keyword，確保搜尋的是「獨立單字」
def match_keyword(text, keyword):
    if not text or not keyword:
        return False
    # \b 確保 keyword 是一個完整的單字，前後不能接英文字母
    # 使用 re.IGNORECASE 確保搜尋時不分大小寫
    return re.search(rf'\b{re.escape(str(keyword).lower())}\b', str(text).lower())

def smart_format(text):
    if not text: return ""
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = t.replace('&nbsp;', ' ')
    t = re.sub(r'<.*?>', '', t)
    return t

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = smart_format(item.get('content', ''))
                    item['expected'] = smart_format(item.get('expected', ''))
                return parsed_data 
        except: pass
    return smart_format(text)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        all_sects, offset = [], 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        path_map = {}
        for s_id in id_to_name:
            parts, curr = [], s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    """
    根據關鍵字找出字典中的同義詞。
    """
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
