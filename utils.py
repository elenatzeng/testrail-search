import re, time, streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    if not text or not keyword: return False
    
    # 1. 物理剥皮：還原 HTML 並移除所有 <...> 標籤，防止隱藏屬性干擾
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean) 
    clean = " ".join(clean.split()).lower()
    
    kw = str(keyword).lower()
    
    # 2. 鋼鐵鎖死：如果是英文/數字，使用 \b 確保「全字匹配」
    # 這樣搜尋 "cny" 就不會抓到 "currency" 或 "cny_123"
    if kw.isalnum() and not re.search(r'[\u4e00-\u9fff]', kw):
        pattern = rf'\b{re.escape(kw)}\b'
        return re.search(pattern, clean) is not None
    else:
        # 中文則維持包含匹配
        return kw in clean

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 🛡️ 幣別隔離：搜尋 3 碼英文時不准聯想，直接鎖死，斷絕與 USDT 的任何字典關連
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
        
        # 獲取所有目錄名稱
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
            
        # 獲取所有案例
        all_cases = []
        offset = 0
        while True:
            resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=250, offset=offset)
            cases = resp['cases']
            if not cases: break
            all_cases.extend(cases)
            if len(cases) < 250: break
            offset += 250
            
        return all_cases, path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except Exception as e:
        return None, None, str(e), None
