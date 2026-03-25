import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html)
    
    # 🚀 處理分離步驟 (JSON 格式)
    if (text.startswith('[') and 'content' in text) or (text.startswith('[') and 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                combined_steps = []
                for i, item in enumerate(parsed_data, 1):
                    c = re.sub(r'<.*?>', '', item.get('content', '')).strip()
                    e = re.sub(r'<.*?>', '', item.get('expected', '')).strip()
                    
                    # 避免編號疊加
                    has_num = re.match(r'^\d+[\.\、]', c)
                    step_prefix = "" if has_num else f"{i}. "
                    
                    res = f"{step_prefix}{c}"
                    if e:
                        res += f"\n<span class='expected-text'>💡 [預期結果]: {e}</span>"
                    combined_steps.append(res)
                return "\n\n".join(combined_steps)
        except:
            pass

    # 🚀 處理普通文字
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&')
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^\d+[\.\、]', line): final.append(line)
        else: final.append(f"{i}. {line}")
    return "\n".join(final)

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
