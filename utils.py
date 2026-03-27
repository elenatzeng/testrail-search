import re, time, streamlit as st
from testrail_api import TestRailAPI
from html import unescape

def match_visual_only(text, keyword):
    if not text or not keyword: return (False, "")
    # 徹底物理剥皮：將內容還原為「肉眼純文字」
    clean = unescape(str(text))
    clean = re.sub(r'<[^>]*>', ' ', clean) # 移除所有 HTML 標籤
    clean = " ".join(clean.split()).lower()
    
    kw = str(keyword).lower().strip()
    
    # 鋼鐵鎖死：全字匹配 (防止 cny 搜到 currency)
    if kw.isalnum() and not re.search(r'[\u4e00-\u9fff]', kw):
        pattern = rf'\b{re.escape(kw)}\b'
        match = re.search(pattern, clean)
        if match:
            # 回傳命中位置的前後文字，幫妳抓鬼
            start, end = match.span()
            snippet = clean[max(0, start-10):min(len(clean), end+10)]
            return (True, f"找到關鍵字: '...{snippet}...'")
    else:
        if kw in clean:
            return (True, f"包含關鍵字: '{kw}'")
    return (False, "")

def smart_format(text):
    if not text: return ""
    t = unescape(str(text))
    t = t.replace('<br />', '\n').replace('<br>', '\n').replace('</div>', '\n')
    t = re.sub(r'<[^>]*>', '', t)
    return t.strip()

def multi_lang_search(text, dictionary):
    t_lower = text.lower().strip()
    # 🛡️ 幣別鎖死：搜尋 3 碼英文不准查字典
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
        # 獲取路徑與案例
        all_sects = api.sections.get_sections(project_id=pid)
        path_map = {s['id']: s['name'] for s in all_sects} # 簡化版路徑
        resp = api.cases.get_cases(project_id=pid, suite_id=sid, limit=1000)
        return resp['cases'], path_map, time.strftime("%H:%M:%S"), p_info.get('name', 'Project')
    except: return None, None, None, None
