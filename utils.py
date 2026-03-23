import re, time, streamlit as st
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return "（無詳細步驟）"
    text = str(raw_html)
    
    # 處理 HTML 標籤
    text = text.replace('<li>', '\n').replace('</li>', '')
    text = re.sub(r'<(br\s*/?|/div|/p)>', '\n', text)
    text = re.sub(r'<.*?>', '', text) # 清除所有剩餘標籤
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'")

    # 🚀 強制換行術：只要看到「空格+數字.」或「文字+數字.」就換行
    text = re.sub(r'(\d+[\.\、])', r'\n\1', text)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    final_output = []
    for line in lines:
        if re.match(r'^\d+[\.\、]', line):
            final_output.append(line)
        else:
            # 沒編號的行如果前面沒數字，就不補數字（避免亂跳號），保持原樣
            final_output.append(line)
    return "\n".join(final_output)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        
        # 🚀 確保正確抓取 Section (路徑)
        sections_data = api.sections.get_sections(project_id=pid, suite_id=sid)
        sect_dict = {s['id']: s for s in sections_data['sections']}
        
        def get_path(sid_in):
            curr = sect_dict.get(sid_in)
            if not curr: return "Unknown"
            parent_id = curr.get('parent_id')
            if parent_id:
                return f"{get_path(parent_id)} > {curr['name']}"
            return curr['name']
            
        path_map = {s_id: get_path(s_id) for s_id in sect_dict}

        # 🚀 分頁抓取 Case (確保抓到 5000 筆以上)
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

def multi_lang_search(text, dictionary):
    text_lower = text.lower().strip()
    related_words = {text_lower}
    for group in dictionary:
        group_lower = [str(word).lower() for word in group]
        if any(text_lower in word for word in group_lower) or any(word in text_lower for word in group_lower):
            related_words.update(group_lower)
    return list(related_words)
