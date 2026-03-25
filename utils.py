import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    
    text = str(raw_html)
    # 🚀 處理 TestRail 的分離步驟 (Separated Steps) 格式
    if (text.startswith('[') and 'content' in text) or (text.startswith('[') and 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                combined_steps = []
                for i, item in enumerate(parsed_data, 1):
                    c = item.get('content', '').strip()
                    e = item.get('expected', '').strip()
                    c = re.sub(r'<.*?>', '', c).replace('&nbsp;', ' ')
                    e = re.sub(r'<.*?>', '', e).replace('&nbsp;', ' ')
                    
                    step_str = f"{i}. {c}"
                    if e:
                        step_str += f"\n   <span class='expected-text'>👉 [預期]: {e}</span>"
                    combined_steps.append(step_str)
                return "\n".join(combined_steps)
        except Exception:
            pass

    # 🚀 處理普通文字格式
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    for i, line in enumerate(lines, 1):
        if re.match(r'^\d+[\.\、\:\s]', line):
            final_output.append(line)
        else:
            final_output.append(f"{i}. {line}")
    return "\n".join(final_output)

def multi_lang_search(text, dictionary):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in dictionary:
        group_lower = [str(word).lower() for word in group]
        if text_lower in group_lower:
            related_words.update(group_lower)
    return list(related_words)

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
            parent_id = curr.get('parent_id')
            return f"{get_path(parent_id)} > {curr['name']}" if parent_id else curr['name']
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
        return None, None, str(e), None
