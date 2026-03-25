import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def add_numbering_and_breaks(text):
    if not text: return ""
    # 1. 先清理 HTML
    text = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    text = re.sub(r'<.*?>', '', text)
    
    # 2. 🚀 強制斷行邏輯：遇到這類符號，如果後面跟著很長的字，就幫它補換行
    # 針對妳截圖中的「路徑：內容管理 > Banner管理」
    text = text.replace(' > ', '\n> ')
    text = text.replace('：', '：\n')
    
    # 3. 重新拆分行並補編號
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    new_lines = []
    count = 1
    for line in lines:
        if not line: continue
        # 如果是路徑開頭，不加編號，但加個縮進
        if line.startswith('>'):
            new_lines.append(f"   {line}")
        elif not re.match(r'^\d+[\.\s]', line):
            new_lines.append(f"{count}. {line}")
            count += 1
        else:
            new_lines.append(line)
            
    return "\n".join(new_lines)

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 移除圖片
    text = re.sub(r'!\[\]\(index\.php\?/attachments/get/\d+\)', '', text)
    
    # 分離步驟格式
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = add_numbering_and_breaks(item.get('content', ''))
                    item['expected'] = add_numbering_and_breaks(item.get('expected', ''))
                return parsed_data 
        except: pass

    return add_numbering_and_breaks(text)

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
        # 🚀 這裡修正路徑抓取：確保抓到所有層級的 Section
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
    except Exception as e:
        return None, None, str(e), None
