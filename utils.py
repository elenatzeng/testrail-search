import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    # 清理 HTML 並處理轉義
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 🚀 強制拆分邏輯：針對黏在一起的關鍵字與數字
    keywords = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功"]
    for word in keywords:
        text = re.sub(f'(?<!\\n)({word})', r'\n\1', text)
    text = re.sub(r'(?<!\\n)(\d+[\.\、])', r'\n\1', text)

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
        if any(text_lower == word for word in group_lower):
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
        return None, None, str(e), None
