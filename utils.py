import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_split_and_number(text):
    if not text: return ""
    # 先清理 HTML
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = re.sub(r'<.*?>', '', t).replace('&nbsp;', ' ')
    
    # 🚀 魔術拆解：遇到關鍵動作詞，強制在前面加換行
    keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "登錄", "進入", "查看", "確認", "正確"]
    for key in keys:
        t = re.sub(f'({key})', r'\n\1', t)
    
    # 重新拆分並加上 1. 2. 3.
    raw_lines = [l.strip() for l in t.split('\n') if l.strip()]
    final_lines = []
    count = 1
    for line in raw_lines:
        # 如果已經有數字編號就不重複加，沒有就幫它加
        if not re.match(r'^\d+[\.\s]', line):
            final_lines.append(f"{count}. {line}")
            count += 1
        else:
            final_lines.append(line)
    return "\n".join(final_lines)

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = smart_split_and_number(item.get('content', ''))
                    item['expected'] = smart_split_and_number(item.get('expected', ''))
                return parsed_data 
        except: pass
    return smart_split_and_number(text)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        # 🚀 抓取所有 Section 建立路徑地圖
        sections = api.sections.get_sections(project_id=pid, suite_id=sid)['sections']
        sect_dict = {s['id']: s for s in sections}
        def get_path(s_id):
            curr = sect_dict.get(s_id)
            if not curr: return ""
            p_id = curr.get('parent_id')
            name = curr.get('name', '')
            return f"{get_path(p_id)} > {name}" if p_id else name
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

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: res.update(g_lower)
    return list(res)
