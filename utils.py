import re
import time
import streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def clean_html(text):
    """清理 HTML 標籤，並處理換行"""
    if not text: return ""
    t = unescape(str(text))
    # 將常見換行標籤轉為真正的換行
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    # 移除剩餘所有標籤
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def match_visual_only(text, keyword):
    """🔒 鋼鐵鎖死：確保單字獨立，cny 不會匹配到 currency"""
    if not text or not keyword: return False
    
    # 清理成純文字以供比對
    clean = clean_html(text).lower()
    kw = str(keyword).lower().strip()
    
    # 如果是 3 碼英文(幣別)，鎖死邊界
    if kw.isalnum() and len(kw) == 3 and not re.search(r'[\u4e00-\u9fff]', kw):
        pattern = rf'\b{re.escape(kw)}\b'
        return re.search(pattern, clean) is not None
    return kw in clean

@st.cache_data(show_spinner=False, ttl=600)
def fetch_data_from_tr(url, user, key, pid, sid):
    """從 TestRail 抓取資料"""
    try:
        api = TestRailAPI(url.split('/index.php')[0].strip('/'), user, key)
        p_info = api.projects.get_project(project_id=pid)
        # 抓取路徑
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects}
        # 抓取案例
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        return resp['cases'], path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except:
        return None, None, None, "連線失敗"

def multi_lang_search(text, dictionary):
    """字典聯想邏輯"""
    t_lower = text.lower().strip()
    # 幣別隔離：3碼英文不查字典
    if len(t_lower) == 3 and t_lower.isalpha():
        return [t_lower]
    
    res = {t_lower}
    for group in dictionary:
        g_lower = [str(w).lower() for w in group]
        if t_lower in g_lower: 
            res.update(g_lower)
            break
    return list(res)
