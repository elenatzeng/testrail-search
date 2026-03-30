import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """
    最純粹的斷行修復：
    1. 把 HTML 標籤換成真正的換行符號。
    2. 絕對不自動補 1. 2. 3.，完全尊重 TestRail 原始內容。
    """
    if not text: return ""
    
    # 將所有可能代表「換行」的 HTML 標籤替換成真正的 \n
    t = str(text)
    t = t.replace('<br />', '\n').replace('<br>', '\n')
    t = t.replace('</div>', '\n').replace('<div>', '')
    t = t.replace('</p>', '\n').replace('<p>', '')
    t = t.replace('</li>', '\n').replace('<li>', '• ')
    t = t.replace('&nbsp;', ' ')
    
    # 移除剩下的殘留標籤 (如 <span>, <strong> 等)
    t = re.sub(r'<.*?>', '', t)
    
    # 整理格式：移除每行末尾多餘的空白，但保留換行結構
    lines = [l.rstrip() for l in t.split('\n')]
    
    # 重新合併成純文字，交給 Streamlit 渲染
    return "\n".join(lines).strip()

def clean_html(raw_html):
    """判斷內容格式，處理分步步驟或純文字內容"""
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 如果是 TestRail 的分步格式 (JSON String)
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    # 這裡調用上面的 smart_format 來處理每個步驟的斷行
                    item['content'] = smart_format(item.get('content', ''))
                    item['expected'] = smart_format(item.get('expected', ''))
                return parsed_data 
        except: pass
    
    # 如果是普通的 Text 欄位
    return smart_format(text)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    """從 TestRail 抓取全量資料 (包含分頁處理)"""
    try:
        base_url = url.split('/index.php')[0].strip('/')
        api = TestRailAPI(base_url, user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        # 抓取目錄 (Sections)
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
            
        # 抓取案例 (Cases)
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
    """聯想詞搜尋 (CNY/充值 等)"""
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
    return list(res)
