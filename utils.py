import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    """
    🔒 最終鎖死邏輯：使用 \b 確保單字獨立，cny 不會抓到 currency。
    """
    if not text or not keyword: return False
    
    # 物理去汙：還原 HTML 並移除所有標籤
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean)
    clean = " ".join(clean.split()).lower()
    
    kw = str(keyword).lower().strip()
    
    # 如果是英文或數字，使用 \b 鎖死單字邊界
    if kw.isalnum() and not re.search(r'[\u4e00-\u9fff]', kw):
        pattern = rf'\b{re.escape(kw)}\b'
        return re.search(pattern, clean) is not None
    else:
        # 中文則維持包含比對
        return kw in clean

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 幣別鎖定：3 碼英文不查字典
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
        path_map = {s['id']: s['name'] for s in all_sects}
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        return resp['cases'], path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except:
        return None, None, None, None
