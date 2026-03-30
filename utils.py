import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """
    精準還原版：
    1. 只有真正的 Unordered List (ul) 才補實心點。
    2. Ordered List (ol) 只換行，不補點，確保 1.2.3.4 原樣呈現。
    3. 保留所有斷行，不吃掉空格。
    """
    if not text: return ""
    
    t = str(text)

    # 🎯 處理「實心點清單」(Unordered List)
    # 這裡只針對被 <ul> 包起來的項目補上 ●
    def replace_ul(match):
        content = match.group(1)
        return content.replace('<li>', '\n ● ').replace('</li>', '')
    t = re.sub(r'<ul>(.*?)</ul>', replace_ul, t, flags=re.DOTALL)

    # 🎯 處理「序號清單」(Ordered List)
    # 這裡只換行，不補任何點，讓內容原本的 1. 2. 3. 自己排隊
    def replace_ol(match):
        content = match.group(1)
        return content.replace('<li>', '\n ').replace('</li>', '')
    t = re.sub(r'<ol>(.*?)</ol>', replace_ol, t, flags=re.DOTALL)

    # 🎯 處理一般 HTML 換行，確保像圖 11 那種擠在一起的情況不會發生
    t = t.replace('<br />', '\n').replace('<br>', '\n')
    t = t.replace('</div>', '\n').replace('<div>', '')
    t = t.replace('</p>', '\n').replace('<p>', '\n')
    t = t.replace('&nbsp;', ' ')
    
    # 🎯 移除其餘殘留 HTML 標籤 (如 <span>)
    t = re.sub(r'<.*?>', '', t)
    
    # 🎯 整理格式：移除每行末尾空白，保留結構
    lines = [l.rstrip() for l in t.split('\n')]
    
    return "\n".join(lines).strip()

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 處理分步步驟 (JSON 格式)
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
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        all_sects = []
        offset = 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, suite_id=sid, offset=offset)
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
            cases = resp['cases'] if isinstance(resp, dict) and 'cases' in resp else resp
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
    return list(res)
