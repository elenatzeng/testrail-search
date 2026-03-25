import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 移除圖片網址與 HTML 標籤
    text = re.sub(r'!\[\]\(index\.php\?/attachments/get/\d+\)', '', text)
    text = text.replace('<br />', '\n').replace('<br>', '\n').replace('&nbsp;', ' ')
    
    # 處理分離步驟 (Separated Steps)
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    for key in ['content', 'expected']:
                        val = str(item.get(key, ''))
                        val = re.sub(r'<.*?>', '', val)
                        # 💡 強制拆解關鍵字換行
                        split_keys = ["路徑", "選擇", "URL", "點擊", "点击", "登入", "查看", "成功"]
                        for word in split_keys:
                            val = re.sub(f'(?<!\\n)({word})', r'\n\1', val)
                        item[key] = val.strip()
                return parsed_data 
        except:
            pass

    text = re.sub(r'<.*?>', '', text)
    return text.strip()

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
