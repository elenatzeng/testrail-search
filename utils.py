import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 🚀 核心優化：如果妳的文字是 "1.xxx 2.xxx"，強制在數字前加上換行
    # 我們找尋前面是空白或是起始位置，後面跟著數字+點號的情況
    text = re.sub(r'(\s+)(\d+\.)', r'\n\2', text)  # 在 " 2." 這種格式前補換行
    text = re.sub(r'(?<!\n)(\d+\.)', r'\n\1', text) # 確保數字點號前面一定有換行
    
    # 處理常見 HTML 標籤換行
    text = text.replace('<li>', '\n- ').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text) 
    
    # 清除所有 HTML 標籤
    cleanr = re.compile('<.*?>')
    text = re.sub(cleanr, '', text)
    
    # 轉義字元處理
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")
    
    # 最終修整：移除多餘空行，並確保每一行都乾乾淨淨
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return "\n".join(lines)

def multi_lang_search(text, dictionary):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in dictionary:
        group_lower = [str(word).lower() for word in group]
        if any(text_lower in word for word in group_lower) or any(word in text_lower for word in group_lower):
            related_words.update(group_lower)
    return list(related_words)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        all_sects = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in all_sects['sections']}
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            return f"{get_path(curr.get('parent_id'))} > {curr['name']}" if curr.get('parent_id') else curr['name']
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}
        
        # 分頁抓取
        all_cases_list = []
        offset = 0
        while True:
            response = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = response['cases']
            if not cases: break
            all_cases_list.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases_list, path_map, time.strftime("%H:%M:%S"), p_info.get('name')
    except Exception as e:
        return None, None, None, str(e)
