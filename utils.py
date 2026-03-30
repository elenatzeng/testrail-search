import re, time, streamlit as st, ast
from testrail_api import TestRailAPI

def smart_format(text):
    """
    精準格式化：
    1. 識別實心點 (●) 與空心點 (○)
    2. 強制還原 TestRail 的清單換行
    3. 移除 HTML 但保留排版結構
    """
    if not text: return ""
    
    t = str(text)

    # 🎯 處理「清單點」的核心邏輯
    # 將 <li> 標籤替換成點點符號，並確保前面有換行
    # 我們先處理嵌套清單，讓它有層次感
    t = t.replace('<li><li>', '\n    ○ ')  # 處理二級清單 (空心點)
    t = t.replace('<li>', '\n ● ')         # 處理一級清單 (實心點)
    t = t.replace('</li>', '')
    
    # 🎯 處理「編號清單」
    # <ol> 代表有序清單，我們確保它上下都有空行
    t = t.replace('<ol>', '\n').replace('</ol>', '\n')
    t = t.replace('<ul>', '\n').replace('</ul>', '\n')

    # 🎯 處理「一般斷行」與「段落」
    t = t.replace('<br />', '\n').replace('<br>', '\n')
    t = t.replace('</div>', '\n').replace('<div>', '')
    t = t.replace('</p>', '\n').replace('<p>', '\n')
    t = t.replace('&nbsp;', ' ')
    
    # 🎯 移除其餘所有 HTML 標籤
    t = re.sub(r'<.*?>', '', t)
    
    # 🎯 重新整理：移除每行末尾空白，並過濾掉因為標籤替換產生的過多空行
    lines = []
    for line in t.split('\n'):
        clean_line = line.rstrip()
        if clean_line: # 只保留有內容的行，或是妳可以根據需求保留空行
            lines.append(clean_line)
            
    return "\n".join(lines).strip()

def clean_html(raw_html):
    """判斷是分步 Case 還是純文字 Case 並處理"""
    if not raw_html: return ""
    text = str(raw_html).strip()
    
    # 如果內容是 TestRail 的「分步步驟」JSON 格式
    if text.startswith('[') and ('content' in text or 'expected' in text):
        try:
            parsed_data = ast.literal_eval(text)
            if isinstance(parsed_data, list):
                for item in parsed_data:
                    # 分別處理「步驟內容」與「預期結果」的斷行與點點
                    item['content'] = smart_format(item.get('content', ''))
                    item['expected'] = smart_format(item.get('expected', ''))
                return parsed_data 
        except: pass
    
    # 如果是普通的標題或前置條件欄位
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
    """聯想詞搜尋 (確保 CNY, 充值 等關鍵字能互相命中)"""
    t_lower = text.lower().strip()
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
    return list(res)
