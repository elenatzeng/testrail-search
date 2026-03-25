import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    
    # 🚀 關鍵修復：如果是 list 或 dict 格式（JSON 亂碼），先提取文字
    text = str(raw_html)
    if text.startswith('[') or text.startswith('{'):
        try:
            # 嘗試解析 TestRail 的步驟格式
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                text = "\n".join([f"{i+1}. {item.get('content', '')} {item.get('expected', '')}" for i, item in enumerate(parsed_data)])
        except:
            pass

    # 原有的清理邏輯
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    split_keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功", "Request", "Expected"]
    for word in split_keys:
        text = re.sub(f'(?<!\\n)({word})', r'\n\1', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    for i, line in enumerate(lines, 1):
        clean_line = re.sub(r'^\d+[\.\、\:\s]*', '', line)
        if clean_line: final_output.append(f"{i}. {clean_line}")
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
            p_id = curr.get('parent_id')
            return f"{get_path(p_id)} > {curr['name']}" if p_id else curr['name']
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
