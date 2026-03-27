import re, time, streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    """
    絕對鎖死比對：
    1. 移除所有 HTML 標籤。
    2. 如果關鍵字是英文/數字，使用 \b 確保「全字匹配」，防止 CNY 搜到 currency。
    """
    if not text or not keyword: return False
    
    # 物理剥皮：還原 HTML 並移除所有 <...> 標籤
    clean = unescape(str(text))import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    """
    🔒 鋼鐵鎖死邏輯：
    使用 \b (Word Boundary) 確保 "CNY" 絕對不會抓到 "currency"。
    """
    if not text or not keyword: return False
    
    # 徹底清除 HTML 標籤，只留肉眼看到的文字
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean)
    clean = " ".join(clean.split()).lower()
    
    kw = str(keyword).lower().strip()
    
    # 🛡️ 核心判定：如果搜尋詞是英文或數字
    if kw.isalnum() and not re.search(r'[\u4e00-\u9fff]', kw):
        # \b 確保 cny 兩邊必須是空白或標點符號
        pattern = rf'\b{re.escape(kw)}\b'
        return re.search(pattern, clean) is not None
    else:
        # 中文沒有單字邊界，維持原本的包含匹配
        return kw in clean

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 幣別隔離：3 碼英文不准查字典，避免意外關聯
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        all_sects = api.sections.get_sections(project_id=pid)
        id_to_name = {s['id']: s['name'] for s in all_sects}
        id_to_parent = {s['id']: s.get('parent_id') for s in all_sects}
        path_map = {}
        for s_id in id_to_name:
            parts, curr = [], s_id
            while curr in id_to_name:
                parts.insert(0, id_to_name[curr])
                curr = id_to_parent.get(curr)
            path_map[s_id] = " › ".join(parts)
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        return resp['cases'], path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except:
        return None, None, None, None
    clean = re.sub(r'<[^>]*>', ' ', clean) 
    clean = " ".join(clean.split()).lower()
    
    kw = str(keyword).lower().strip()
    
    # 🛡️ 核心：全字匹配鎖死
    # 如果是英文或數字，且不含中文
    if kw.isalnum() and not re.search(r'[\u4e00-\u9fff]', kw):
        # \b 代表單字邊界。cny 不會匹配到 currency
        pattern = rf'\b{re.escape(kw)}\b'
        return re.search(pattern, clean) is not None
    else:
        # 中文則維持包含匹配（因為中文沒有空格邊界）
        return kw in clean

def smart_format(text):
    """將 TestRail 的 HTML 內容轉化為乾淨的換行文字"""
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    """字典聯想邏輯"""
    t_lower = text.lower().strip()
    # 幣別隔離：3 碼英文不准查字典，避免意外關連
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    """API 抓取數據"""
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        
        # 抓取路徑 (Section)
        all_sects = []
        offset = 0
        while True:
            sects = api.sections.get_sections(project_id=pid, offset=offset)
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
            
        # 抓取案例 (Case)
        all_cases = []
        offset = 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            if not resp['cases']: break
            all_cases.extend(resp['cases'])
            if len(resp['cases']) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None
