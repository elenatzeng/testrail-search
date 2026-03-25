import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_split_and_number(text):
    if not text: return ""
    # 清理 HTML 標籤
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = re.sub(r'<.*?>', '', t).replace('&nbsp;', ' ')
    
    # 🚀 強制拆分關鍵字：遇到動作詞就換行，保證 123 編號能抓到
    keys = ["路徑", "內容管理", "選擇", "URL", "點擊", "点击", "登入", "登錄", "進入", "查看", "確認", "正確"]
    for key in keys:
        t = re.sub(f'({key})', r'\n\1', t)
    
    raw_lines = [l.strip() for l in t.split('\n') if l.strip()]
    final_lines = []
    count = 1
    for line in raw_lines:
        if not line: continue
        # 如果這一行還沒有編號，就幫它加上
        if not re.match(r'^\d+[\.\s]', line):
            final_lines.append(f"{count}. {line}")
            count += 1
        else:
            final_lines.append(line)
    return "\n".join(final_lines)

def clean_html(raw_html):
    if not raw_html: return ""
    text = str(raw_html).strip()
    # 處理分離步驟 (Separated Steps)
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    item['content'] = smart_split_and_number(item.get('content', ''))
                    item['expected'] = smart_split_and_number(item.get('expected', ''))
                return parsed_data 
        except: pass
    # 處理通用文字
    return smart_split_and_number(text)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        
        # 🚀 1. 抓取專案內「所有」Section，不限 Suite，確保地圖完整
        all_sections = api.sections.get_sections(project_id=pid)['sections']
        sect_dict = {s['id']: s for s in all_sections}
        
        # 🚀 2. 建立递归路徑地圖
        def get_full_path(s_id):
            if s_id not in sect_dict: return ""
            curr = sect_dict[s_id]
            parent_id = curr.get('parent_id')
            name = curr.get('name', '')
            if parent_id and parent_id in sect_dict:
                return f"{get_full_path(parent_id)} > {name}"
            return name

        path_map = {s_id: get_full_path(s_id) for s_id in sect_dict}
        
        # 🚀 3. 抓取案例
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

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: res.update(g_lower)
    return list(res)
