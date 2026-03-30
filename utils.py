import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """
    精準還原格式：
    - Unordered List (ul): 轉化為 ●
    - Ordered List (ol): 保持純文字換行 (不加點，保留原始 1. 2. 3.)
    - 確保斷行與 TestRail 一致
    """
    if not text: return ""
    
    t = str(text)

    # 1. 處理 Unordered List (實心點清單)
    # 只有被 <ul> 包起來的 <li> 才會被補上「●」
    def replace_ul_dots(match):
        content = match.group(1)
        # 在每個項目處換行並補點
        items = content.replace('<li>', '\n ● ').replace('</li>', '')
        return items
    
    t = re.sub(r'<ul>(.*?)</ul>', replace_ul_dots, t, flags=re.DOTALL)

    # 2. 處理 Ordered List (數字序號清單)
    # <ol> 內部的 <li> 只換行，不補點，這樣文字裡的 1. 2. 3. 就不會被干擾
    def replace_ol_lines(match):
        content = match.group(1)
        # 只換行，不加任何符號
        items = content.replace('<li>', '\n ').replace('</li>', '')
        return items
    
    t = re.sub(r'<ol>(.*?)</ol>', replace_ol_lines, t, flags=re.DOTALL)

    # 3. 處理一般的換行標籤
    t = t.replace('<br />', '\n').replace('<br>', '\n')
    t = t.replace('</div>', '\n').replace('<div>', '')
    t = t.replace('</p>', '\n').replace('<p>', '\n')
    t = t.replace('&nbsp;', ' ')
    
    # 4. 移除殘留的所有 HTML 標籤
    t = re.sub(r'<.*?>', '', t)
    
    # 5. 清理每行末尾空白，並過濾掉因為標籤替換產生的過多空行
    lines = []
    for line in t.split('\n'):
        s = line.rstrip()
        if s:
            lines.append(s)
            
    return "\n".join(lines).strip()

def clean_html(raw_html):
    """判斷內容格式，處理分步步驟或純文字內容"""
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 如果是分步步驟 (JSON 格式)
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
def fetch_data_from_tr(url, user, key, pid, sid):
    """從 TestRail 抓取全量目錄與案例"""
    try:
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        # 抓取目錄
        all_sects = []
        offset = 0
        while True:
            sect_resp = api.sections.get_sections(project_id=pid, suite_id=sid, offset=offset)
            sects = sect_resp['sections'] if isinstance(sect_resp, dict) else sect_resp
            if not sects: break
            all_sects.extend(sects)
            if len(sects) < 250: break
            offset += 250
        
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        
        path_map = {}
        for s_id in id_to_name:
            parts, curr = [], s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
            
        # 抓取案例
        all_cases, offset = [], 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases'] if isinstance(resp, dict) and 'cases' in resp else resp
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None

def multi_lang_search(text, dictionary):
    """聯想詞搜尋 (CNY, 充值等)"""
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
    return list(res)
