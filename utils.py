import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    if not text: return ""
    # 1. 徹底清理 HTML
    t = text.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n').replace('<div>', '')
    t = t.replace('&nbsp;', ' ')
    t = re.sub(r'<.*?>', '', t)
    
    # 2. 🚀 動作拆解：只要看到動作關鍵字，強制在前面加換行，確保 1. 2. 3. 抓得到
    keys = ["路徑", "內容管理", "選擇", "URL", "點擊", "点击", "登入", "進入", "查看", "確認", "正確"]
    for key in keys:
        t = re.sub(f'({key})', r'\n\1', t)
    
    # 3. 補上編號，並把 > 換成漂亮符號
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    final_lines = []
    count = 1
    for line in lines:
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
                    item['content'] = smart_format(item.get('content', ''))
                    item['expected'] = smart_format(item.get('expected', ''))
                return parsed_data 
        except: pass
    return smart_format(text)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(_url, _user, _pw, pid, sid):
    try:
        api = TestRailAPI(_url.split('/index.php')[0].strip('/'), _user, _pw)
        p_info = api.projects.get_project(project_id=pid)
        
        # 🚀 關鍵修正：抓取 Project 下「所有」Sections，打破 Suite 的限制
        all_sects = api.sections.get_sections(project_id=pid)['sections']
        sect_dict = {s['id']: s for s in all_sects}
        
        # 🚀 向上溯源邏輯：從自己開始，一路抓到最頂層
        def get_full_chain(s_id):
            parts = []
            curr_id = s_id
            while curr_id in sect_dict:
                curr_sect = sect_dict[curr_id]
                parts.insert(0, curr_sect['name'])
                curr_id = curr_sect.get('parent_id') # 往上抓爸爸的 ID
            # 用妳要的 › 符號串起來
            return " › ".join(parts) if parts else "GoGaming"

        path_map = {s_id: get_full_path for s_id in sect_dict if (get_full_path := get_full_chain(s_id))}
        
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
